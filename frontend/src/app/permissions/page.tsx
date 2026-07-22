"use client";

import { useState } from "react";
import MainLayout from "@/components/layout/main-layout";
import { Shield, Lock, Unlock, Check, X } from "lucide-react";

interface Permission {
  id: string;
  name: string;
  description: string;
  category: string;
}

interface RolePermissions {
  role: string;
  permissions: string[];
}

const permissions: Permission[] = [
  // Tickets
  { id: "tickets.view", name: "View tickets", description: "Can view tickets", category: "Tickets" },
  { id: "tickets.create", name: "Create tickets", description: "Can create new tickets", category: "Tickets" },
  { id: "tickets.edit", name: "Edit tickets", description: "Can edit ticket details", category: "Tickets" },
  { id: "tickets.delete", name: "Delete tickets", description: "Can delete tickets", category: "Tickets" },
  { id: "tickets.assign", name: "Assign tickets", description: "Can assign tickets to users", category: "Tickets" },
  
  // Boards
  { id: "boards.view", name: "View boards", description: "Can view boards", category: "Boards" },
  { id: "boards.create", name: "Create boards", description: "Can create new boards", category: "Boards" },
  { id: "boards.edit", name: "Edit boards", description: "Can edit board settings", category: "Boards" },
  { id: "boards.delete", name: "Delete boards", description: "Can delete boards", category: "Boards" },
  
  // Projects
  { id: "projects.view", name: "View projects", description: "Can view projects", category: "Projects" },
  { id: "projects.create", name: "Create projects", description: "Can create new projects", category: "Projects" },
  { id: "projects.edit", name: "Edit projects", description: "Can edit project settings", category: "Projects" },
  { id: "projects.delete", name: "Delete projects", description: "Can delete projects", category: "Projects" },
  
  // Team
  { id: "team.view", name: "View team", description: "Can view team members", category: "Team" },
  { id: "team.invite", name: "Invite members", description: "Can invite new team members", category: "Team" },
  { id: "team.manage", name: "Manage team", description: "Can manage team members and roles", category: "Team" },
  
  // Settings
  { id: "settings.view", name: "View settings", description: "Can view workspace settings", category: "Settings" },
  { id: "settings.edit", name: "Edit settings", description: "Can edit workspace settings", category: "Settings" },
];

export default function PermissionsPage() {
  const [rolePermissions, setRolePermissions] = useState<RolePermissions[]>([
    {
      role: "owner",
      permissions: permissions.map((p) => p.id),
    },
    {
      role: "admin",
      permissions: permissions.filter(p => !p.id.includes("delete")).map(p => p.id),
    },
    {
      role: "member",
      permissions: permissions
        .filter(p => p.id.includes("view") || p.id.includes("create") || p.id.includes("edit"))
        .filter(p => !p.category.includes("Team") && !p.category.includes("Settings"))
        .map(p => p.id),
    },
    {
      role: "viewer",
      permissions: permissions.filter(p => p.id.includes("view")).map(p => p.id),
    },
  ]);

  const [selectedRole, setSelectedRole] = useState("admin");
  const [hasChanges, setHasChanges] = useState(false);

  const categories = Array.from(new Set(permissions.map((p) => p.category)));

  const togglePermission = (permissionId: string) => {
    setRolePermissions(
      rolePermissions.map((rp) => {
        if (rp.role === selectedRole) {
          const newPermissions = rp.permissions.includes(permissionId)
            ? rp.permissions.filter((p) => p !== permissionId)
            : [...rp.permissions, permissionId];
          return { ...rp, permissions: newPermissions };
        }
        return rp;
      })
    );
    setHasChanges(true);
  };

  const hasPermission = (permissionId: string) => {
    const role = rolePermissions.find((rp) => rp.role === selectedRole);
    return role?.permissions.includes(permissionId) || false;
  };

  const handleSave = () => {
    console.log("Saving permissions:", rolePermissions);
    setHasChanges(false);
  };

  const handleReset = () => {
    // Reset to default permissions
    setHasChanges(false);
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case "owner":
        return "bg-purple-100 text-purple-700 border-purple-200";
      case "admin":
        return "bg-blue-100 text-blue-700 border-blue-200";
      case "member":
        return "bg-green-100 text-green-700 border-green-200";
      case "viewer":
        return "bg-slate-100 text-slate-700 border-slate-200";
      default:
        return "bg-slate-100 text-slate-700 border-slate-200";
    }
  };

  return (
    <MainLayout>
      <div className="mx-auto max-w-6xl py-6 px-4">
        <div className="flex items-center gap-2 mb-6">
          <Shield className="w-6 h-6" />
          <h1 className="text-2xl font-semibold text-slate-900">Permissions</h1>
        </div>

        {/* Role selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">Select role to configure</label>
          <div className="flex flex-wrap gap-2">
            {rolePermissions.map((rp) => (
              <button
                key={rp.role}
                onClick={() => setSelectedRole(rp.role)}
                className={`px-4 py-2 rounded-lg border-2 font-medium capitalize transition-colors ${
                  selectedRole === rp.role
                    ? getRoleBadge(rp.role)
                    : "bg-white border-slate-200 text-slate-600 hover:border-slate-300"
                }`}
              >
                {rp.role}
              </button>
            ))}
          </div>
        </div>

        {/* Permissions grid */}
        <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-6">
          {categories.map((category) => (
            <div key={category} className="mb-6 last:mb-0">
              <h3 className="text-lg font-medium text-slate-900 mb-4">{category}</h3>
              <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                {permissions
                  .filter((p) => p.category === category)
                  .map((permission) => (
                    <button
                      key={permission.id}
                      onClick={() => togglePermission(permission.id)}
                      className={`flex items-start gap-3 p-4 rounded-lg border-2 transition-colors ${
                        hasPermission(permission.id)
                          ? "border-sky-500 bg-sky-50"
                          : "border-slate-200 hover:border-slate-300"
                      }`}
                    >
                      <div className="flex-shrink-0 mt-0.5">
                        {hasPermission(permission.id) ? (
                          <Check className="w-5 h-5 text-sky-600" />
                        ) : (
                          <X className="w-5 h-5 text-slate-400" />
                        )}
                      </div>
                      <div className="text-left">
                        <p className="font-medium text-slate-900">{permission.name}</p>
                        <p className="text-sm text-slate-500 mt-1">{permission.description}</p>
                      </div>
                    </button>
                  ))}
              </div>
            </div>
          ))}
        </div>

        {/* Actions */}
        {hasChanges && (
          <div className="mt-6 flex items-center justify-between p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <p className="text-sm text-amber-800">You have unsaved changes to permissions.</p>
            <div className="flex gap-3">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
              >
                Reset
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors"
              >
                Save changes
              </button>
            </div>
          </div>
        )}

        {/* Permission summary */}
        <div className="mt-6 bg-slate-50 border border-slate-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Role summary</h3>
          <div className="space-y-3">
            {rolePermissions.map((rp) => (
              <div key={rp.role} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getRoleBadge(rp.role)}`}>
                    {rp.role}
                  </span>
                  <span className="text-sm text-slate-600">
                    {rp.permissions.length} permissions
                  </span>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-500">
                  {rp.role === "owner" ? (
                    <Lock className="w-4 h-4" />
                  ) : (
                    <Unlock className="w-4 h-4" />
                  )}
                  {rp.role === "owner" ? "Full access" : "Customizable"}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
