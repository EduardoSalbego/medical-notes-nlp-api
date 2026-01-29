<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\ProcessMedicalNoteRequest;
use App\Services\MedicalNoteService;
use App\Services\AuditLogService;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Auth;

class MedicalNoteController extends Controller
{
    public function __construct(
        private MedicalNoteService $medicalNoteService,
        private AuditLogService $auditLogService
    ) {}

    /**
     * Process a medical note
     *
     * @param ProcessMedicalNoteRequest $request
     * @return JsonResponse
     */
    public function process(ProcessMedicalNoteRequest $request): JsonResponse
    {
        try {
            $this->auditLogService->log([
                'action' => 'medical_note.process',
                'user_id' => Auth::id(),
                'ip_address' => request()->ip(),
                'user_agent' => request()->userAgent(),
                'data' => [
                    'note_length' => strlen($request->medical_note),
                    'skip_masking' => $request->skip_masking ?? false,
                ]
            ]);

            $result = $this->medicalNoteService->process($request->validated());

            return response()->json([
                'status' => 'success',
                'data' => $result,
                'processed_at' => now()->toISOString()
            ], 200);

        } catch (\Exception $e) {
            Log::error('Error processing medical note', [
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);

            return response()->json([
                'status' => 'error',
                'message' => 'Error processing medical note',
                'error' => config('app.debug') ? $e->getMessage() : 'Internal server error'
            ], 500);
        }
    }

    /**
     * Get processing history for authenticated user
     *
     * @return JsonResponse
     */
    public function history(): JsonResponse
    {
        $history = $this->medicalNoteService->getUserHistory(Auth::id());

        return response()->json([
            'status' => 'success',
            'data' => $history
        ], 200);
    }

    /**
     * Get processing statistics
     *
     * @return JsonResponse
     */
    public function statistics(): JsonResponse
    {
        $stats = $this->medicalNoteService->getStatistics(Auth::id());

        return response()->json([
            'status' => 'success',
            'data' => $stats
        ], 200);
    }
}