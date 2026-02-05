<?php

namespace App\Services;

/**
 * Data Masking Service for De-identification
 * Removes PII from medical notes before processing
 */
class DataMaskingService
{
    /**
     * Mask PII from medical text
     *
     * @param string $text
     * @return array
     */
    public function mask(string $text): array
    {
        $originalText = $text;
        $removedEntities = [
            'cpfs' => [],
            'emails' => [],
            'phones' => [],
            'names' => [],
        ];

        // Mask CPFs (Brazilian format)
        $text = preg_replace_callback(
            '/\d{3}\.?\d{3}\.?\d{3}-?\d{2}/',
            function ($matches) use (&$removedEntities) {
                $removedEntities['cpfs'][] = $matches[0];
                return '[CPF]';
            },
            $text
        );

        // Mask SSNs (US format)
        $text = preg_replace_callback(
            '/\d{3}-?\d{2}-?\d{4}/',
            function ($matches) use (&$removedEntities) {
                $removedEntities['cpfs'][] = $matches[0]; // Store in cpfs array for simplicity
                return '[SSN]';
            },
            $text
        );

        // Mask emails
        $text = preg_replace_callback(
            '/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/',
            function ($matches) use (&$removedEntities) {
                $removedEntities['emails'][] = $matches[0];
                return '[EMAIL]';
            },
            $text
        );

        // Mask phone numbers (Brazilian)
        $text = preg_replace_callback(
            '/(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}/',
            function ($matches) use (&$removedEntities) {
                $removedEntities['phones'][] = $matches[0];
                return '[PHONE]';
            },
            $text
        );

        // Mask phone numbers (US)
        $text = preg_replace_callback(
            '/\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/',
            function ($matches) use (&$removedEntities) {
                $removedEntities['phones'][] = $matches[0];
                return '[PHONE]';
            },
            $text
        );

        $text = preg_replace_callback(
            '/(?:Paciente|Patient|Sr\.|Sra\.|Dr\.|Dra\.)\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+)/i',
            function ($matches) use (&$removedEntities) {
                $removedEntities['names'][] = $matches[1];
                return $matches[0][0] . '[PATIENT_NAME]';
            },
            $text
        );

        $removedEntities = array_map('array_unique', $removedEntities);
        $removedEntities = array_map('array_values', $removedEntities);

        return [
            'masked_text' => $text,
            'removed_entities' => $removedEntities,
            'original_length' => strlen($originalText),
            'masked_length' => strlen($text),
        ];
    }
}