<?php

namespace App\Services;

class DataMaskingService
{
    public function mask(string $text, array $entities): string
    {
        $maskedText = $text;
        
        usort($entities, function ($a, $b) {
            return $b['start'] <=> $a['start'];
        });

        foreach ($entities as $entity) {
            if (str_starts_with($entity['label'], 'PII_')) {
                $replacement = "[MASCARADO]";
                
                $maskedText = substr_replace(
                    $maskedText,
                    $replacement,
                    $entity['start'],
                    $entity['end'] - $entity['start']
                );
            }
        }

        return $maskedText;
    }
}