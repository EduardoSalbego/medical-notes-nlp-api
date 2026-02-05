<?php

namespace App\Services;

use App\Models\AuditLog;
use Illuminate\Support\Facades\Log;

/**
 * Audit Log Service for HIPAA-like compliance
 * Logs all access to sensitive medical data
 */
class AuditLogService
{
    /**
     * Log an audit event
     *
     * @param array $data
     * @return AuditLog
     */
    public function log(array $data): AuditLog
    {
        try {
            return AuditLog::create([
                'user_id' => $data['user_id'] ?? auth()->id(),
                'action' => $data['action'] ?? 'unknown',
                'ip_address' => $data['ip_address'] ?? request()->ip(),
                'user_agent' => $data['user_agent'] ?? request()->userAgent(),
                'data' => $data['data'] ?? [],
                'created_at' => now(),
            ]);
        } catch (\Exception $e) {
            Log::channel('audit')->error('Audit log failed', [
                'error' => $e->getMessage(),
                'data' => $data
            ]);
            throw $e;
        }
    }

    /**
     * Get audit logs for a user
     *
     * @param int $userId
     * @param int $limit
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getUserLogs(int $userId, int $limit = 100)
    {
        return AuditLog::where('user_id', $userId)
            ->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get();
    }

    /**
     * Get audit logs by action
     *
     * @param string $action
     * @param int $limit
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getLogsByAction(string $action, int $limit = 100)
    {
        return AuditLog::where('action', $action)
            ->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get();
    }
}