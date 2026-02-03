<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $adminRole = Role::firstOrCreate(['name' => 'admin']);
        $userRole = Role::firstOrCreate(['name' => 'user']);
        $doctorRole = Role::firstOrCreate(['name' => 'doctor']);

        $permissions = [
            'process_medical_notes',
            'view_medical_notes',
            'view_all_medical_notes',
            'view_audit_logs',
        ];

        foreach ($permissions as $permission) {
            Permission::firstOrCreate(['name' => $permission]);
        }

        $adminRole->givePermissionTo(Permission::all());
        $doctorRole->givePermissionTo(['process_medical_notes', 'view_medical_notes']);
        $userRole->givePermissionTo(['process_medical_notes']);

        $admin = User::firstOrCreate(
            ['email' => 'admin@medical-notes.local'],
            [
                'name' => 'Administrator',
                'password' => Hash::make('password'),
                'email_verified_at' => now(),
            ]
        );
        $admin->assignRole('admin');

        $doctor = User::firstOrCreate(
            ['email' => 'doctor@medical-notes.local'],
            [
                'name' => 'Dr. Test',
                'password' => Hash::make('password'),
                'email_verified_at' => now(),
            ]
        );
        $doctor->assignRole('doctor');

        $user = User::firstOrCreate(
            ['email' => 'user@medical-notes.local'],
            [
                'name' => 'Test User',
                'password' => Hash::make('password'),
                'email_verified_at' => now(),
            ]
        );
        $user->assignRole('user');
    }
}