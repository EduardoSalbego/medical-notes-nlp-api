<?php

use App\Http\Controllers\Api\NoteController;
use Illuminate\Support\Facades\Route;

Route::post('/notes', [NoteController::class, 'store']);
