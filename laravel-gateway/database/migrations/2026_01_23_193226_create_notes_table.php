<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('notes', function (Blueprint $blueprint) {
            $blueprint->id();
            $blueprint->text('original_content');
            $blueprint->text('masked_content');
            $blueprint->json('metadata')->nullable();
            $blueprint->string('risk_score')->default('Low');
            $blueprint->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('notes');
    }
};