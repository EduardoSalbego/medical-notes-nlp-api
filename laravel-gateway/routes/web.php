<?php

use App\Http\Controllers\NoteViewController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/notes', [NoteViewController::class, 'index']);
