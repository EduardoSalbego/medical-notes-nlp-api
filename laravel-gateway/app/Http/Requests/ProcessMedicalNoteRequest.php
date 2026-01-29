<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ProcessMedicalNoteRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true; // authorization handled by middleware
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'medical_note' => [
                'required',
                'string',
                'min:10',
                'max:10000'
            ],
            'skip_masking' => [
                'sometimes',
                'boolean'
            ]
        ];
    }

    /**
     * Get custom messages for validator errors.
     *
     * @return array
     */
    public function messages(): array
    {
        return [
            'medical_note.required' => 'O texto da nota médica é obrigatório.',
            'medical_note.min' => 'A nota médica deve ter pelo menos 10 caracteres.',
            'medical_note.max' => 'A nota médica não pode exceder 10.000 caracteres.',
        ];
    }
}