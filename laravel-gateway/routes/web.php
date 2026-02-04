<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()->json([
        'service' => 'Medical Notes NLP API - Laravel Gateway',
        'version' => '1.0.0',
        'status' => 'operational',
        'docs' => '/api/documentation'
    ]);
});