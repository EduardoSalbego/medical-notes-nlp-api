<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class MedicalNote extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'original_note_encrypted',
        'note_hash',
        'entities',
        'risk_classification',
        'confidence_score',
        'processing_time_ms',
        'language_detected',
        'removed_entities',
        'processed_at',
    ];

    protected $casts = [
        'entities' => 'array',
        'confidence_score' => 'array',
        'removed_entities' => 'array',
        'processed_at' => 'datetime',
        'processing_time_ms' => 'float',
    ];

    /**
     * Get the user that owns the medical note
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}