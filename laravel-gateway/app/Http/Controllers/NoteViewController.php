<?php

namespace App\Http\Controllers;

use App\Models\Note;
use Illuminate\View\View;

class NoteViewController extends Controller
{
    public function index(): View
    {
        $notes = Note::latest()->get();
        return view('notes.index', compact('notes'));
    }
}