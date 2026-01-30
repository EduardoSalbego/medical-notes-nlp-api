<?php

namespace App\Services;

use App\Models\MedicalNote;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Crypt;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Cache;

class MedicalNoteService
{
    public function __construct(
        private EncryptionService $encryptionService,
        private DataMaskingService $dataMaskingService
    ) {}

    /**
     * Process medical note through AI Engine
     *
     * @param array $data
     * @return array
     */
    public function process(array $data): array
    {
        $medicalNote = $data['medical_note'];
        $skipMasking = $data['skip_masking'] ?? false;

        if (!$skipMasking) {
            $maskingResult = $this->dataMaskingService->mask($medicalNote);
            $maskedNote = $maskingResult['masked_text'];
            $removedEntities = $maskingResult['removed_entities'];
        } else {
            $maskedNote = $medicalNote;
            $removedEntities = [];
        }

        $aiEngineUrl = config('services.ai_engine.url');
        
        try {
            $response = Http::timeout(30)->post("{$aiEngineUrl}/api/v1/process", [
                'medical_note' => $maskedNote,
                'skip_masking' => true,
            ]);

            if (!$response->successful()) {
                throw new \Exception("AI Engine error: " . $response->body());
            }

            $aiResult = $response->json();

            $encryptedNote = $this->encryptionService->encrypt($medicalNote);

            $note = MedicalNote::create([
                'user_id' => auth()->id(),
                'original_note_encrypted' => $encryptedNote,
                'note_hash' => $aiResult['data']['note_hash'] ?? null,
                'entities' => $aiResult['data']['entities'] ?? [],
                'risk_classification' => $aiResult['data']['risk_classification'] ?? 'unknown',
                'confidence_score' => $aiResult['data']['confidence_score'] ?? [],
                'processing_time_ms' => $aiResult['data']['processing_time_ms'] ?? 0,
                'language_detected' => $aiResult['data']['language_detected'] ?? 'unknown',
                'removed_entities' => $removedEntities,
                'processed_at' => now(),
            ]);

            return [
                'id' => $note->id,
                'entities' => $aiResult['data']['entities'],
                'risk_classification' => $aiResult['data']['risk_classification'],
                'confidence_score' => $aiResult['data']['confidence_score'],
                'processing_time_ms' => $aiResult['data']['processing_time_ms'],
                'language_detected' => $aiResult['data']['language_detected'],
                'note_hash' => $aiResult['data']['note_hash'],
                'masking_applied' => !$skipMasking,
                'removed_entities' => $removedEntities,
                'processed_at' => $note->processed_at->toISOString(),
            ];

        } catch (\Exception $e) {
            Log::error('Error in MedicalNoteService::process', [
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            throw $e;
        }
    }

    /**
     * Get user's processing history
     *
     * @param int $userId
     * @return array
     */
    public function getUserHistory(int $userId): array
    {
        $notes = MedicalNote::where('user_id', $userId)
            ->orderBy('processed_at', 'desc')
            ->limit(50)
            ->get();

        return $notes->map(function ($note) {
            return [
                'id' => $note->id,
                'note_hash' => $note->note_hash,
                'entities' => $note->entities,
                'risk_classification' => $note->risk_classification,
                'confidence_score' => $note->confidence_score,
                'language_detected' => $note->language_detected,
                'processed_at' => $note->processed_at->toISOString(),
            ];
        })->toArray();
    }

    /**
     * Get processing statistics
     *
     * @param int $userId
     * @return array
     */
    public function getStatistics(int $userId): array
    {
        return Cache::remember("user_stats_{$userId}", 3600, function () use ($userId) {
            $notes = MedicalNote::where('user_id', $userId)->get();

            $total = $notes->count();
            $byRisk = $notes->groupBy('risk_classification')->map->count();
            
            $avgProcessingTime = $notes->avg('processing_time_ms');
            
            return [
                'total_processed' => $total,
                'by_risk_classification' => $byRisk,
                'average_processing_time_ms' => round($avgProcessingTime, 2),
                'last_processed_at' => $notes->max('processed_at')?->toISOString(),
            ];
        });
    }
}