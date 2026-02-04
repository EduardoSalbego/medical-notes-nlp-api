<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\V1\MedicalNoteController;
use App\Http\Controllers\Api\V1\AuthController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::prefix('v1')->group(function () {
    
    // Public routes
    Route::post('/register', [AuthController::class, 'register']);
    Route::post('/login', [AuthController::class, 'login']);

    // Protected routes
    Route::middleware(['auth:sanctum'])->group(function () {
        // Medical Notes
        Route::prefix('medical-notes')->group(function () {
            Route::post('/process', [MedicalNoteController::class, 'process']);
            Route::get('/history', [MedicalNoteController::class, 'history']);
            Route::get('/statistics', [MedicalNoteController::class, 'statistics']);
        });

        // User profile
        Route::get('/user', function (Request $request) {
            return $request->user();
        });

        // Logout
        Route::post('/logout', [AuthController::class, 'logout']);
    });
});