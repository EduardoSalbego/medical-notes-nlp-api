<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Note;
use App\Services\AIService;
use App\Services\DataMaskingService;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class NoteController extends Controller
{
    public function __construct(
        protected AIService $aiService,
        protected DataMaskingService $maskingService
    ) {}

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'text' => 'required|string|min:10'
        ]);

        $aiResult = $this->aiService->analyzeText($validated['text']);
        
        $entities = $aiResult['entities'] ?? [];
        
        $maskedText = $this->maskingService->mask($validated['text'], $entities);

        $note = Note::create([
            'original_content' => $validated['text'],
            'masked_content' => $maskedText,
            'metadata' => $entities,
            'risk_score' => $aiResult['risk_score'] ?? 'Low'
        ]);

        return response()->json([
            'message' => 'Note processed successfully',
            'data' => [
                'id' => $note->id,
                'masked_content' => $note->masked_content,
                'entities_found' => count($entities)
            ]
        ], 201);
    }
}