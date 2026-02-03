<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('medical_notes', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->text('original_note_encrypted');
            $table->string('note_hash')->nullable()->index();
            $table->json('entities')->nullable();
            $table->string('risk_classification')->default('unknown');
            $table->json('confidence_score')->nullable();
            $table->float('processing_time_ms')->default(0);
            $table->string('language_detected')->nullable();
            $table->json('removed_entities')->nullable();
            $table->timestamp('processed_at');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('medical_notes');
    }
};