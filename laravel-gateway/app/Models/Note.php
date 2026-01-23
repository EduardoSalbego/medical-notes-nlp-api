<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Note extends Model
{
    protected $fillable = [
        'original_content',
        'masked_content',
        'metadata',
        'risk_score'
    ];

    protected $casts = [
        'metadata' => 'array',
        'original_content' => 'encrypted'
    ];
}