<?php

namespace App\Services;

use Illuminate\Support\Facades\Crypt;
use Illuminate\Support\Facades\Log;

class EncryptionService
{
    /**
     * Encrypt sensitive data
     *
     * @param string $data
     * @return string
     */
    public function encrypt(string $data): string
    {
        try {
            return Crypt::encryptString($data);
        } catch (\Exception $e) {
            Log::error('Encryption error', ['error' => $e->getMessage()]);
            throw new \RuntimeException('Failed to encrypt data');
        }
    }

    /**
     * Decrypt sensitive data
     *
     * @param string $encryptedData
     * @return string
     */
    public function decrypt(string $encryptedData): string
    {
        try {
            return Crypt::decryptString($encryptedData);
        } catch (\Exception $e) {
            Log::error('Decryption error', ['error' => $e->getMessage()]);
            throw new \RuntimeException('Failed to decrypt data');
        }
    }
}