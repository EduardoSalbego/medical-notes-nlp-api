<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <title>Visualização de Notas Médicas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">
    <div class="container py-5">
        <h2 class="mb-4">Notas Processadas pela IA</h2>
        <div class="row">
            @foreach($notes as $note)
                <div class="col-md-6 mb-3">
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title text-primary">Nota #{{ $note->id }}</h5>
                            <p class="card-text">{{ $note->masked_content }}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge bg-{{ $note->risk_score === 'High' ? 'danger' : 'success' }}">
                                    Risco: {{ $note->risk_score }}
                                </span>
                                <small class="text-muted">{{ $note->created_at->format('d/m/Y H:i') }}</small>
                            </div>
                        </div>
                    </div>
                </div>
            @endforeach
        </div>
    </div>
</body>

</html>