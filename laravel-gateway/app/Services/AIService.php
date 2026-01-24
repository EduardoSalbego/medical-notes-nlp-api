<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class AIService
{
    protected string $baseUrl;

    public function __construct()
    {
        $this->baseUrl = config('services.ai.url', 'http://ai-engine:8001');
    }

    public function analyzeText(string $text): array
    {
        try {
            $response = Http::timeout(10)->post("{$this->baseUrl}/analyze", [
                'text' => $text
            ]);

            if ($response instanceof \GuzzleHttp\Promise\PromiseInterface) {
                $response = $response->wait();
            }

            if ($response->failed()) {
                Log::error('AI Service failure', [
                    'status' => $response->status(),
                    'body' => $response->body(),
                ]);
                return [];
            }

            return $response->json();
        } catch (\Exception $e) {
            Log::error('AI Service connection error', ['message' => $e->getMessage()]);
            return [];
        }
    }
}