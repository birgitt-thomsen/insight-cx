import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  FileText,
  FlaskConical,
  MessageSquare,
  Settings,
  Upload as UploadIcon,
  Menu,
  X,
} from "lucide-react";
import { fetchAiSettings } from "../api/aiSettings";
import { Logo } from "../components/Logo";

const NAV_ITEMS = [
  { to: "/executive-brief", label: "Executive Brief", icon: FileText },
  { to: "/feedback-explorer", label: "Feedback Explorer", icon: MessageSquare },
  { to: "/upload", label: "Upload", icon: UploadIcon },
  { to: "/ai-evaluation", label: "AI Evaluation", icon: FlaskConical },
  { to: "/administration", label: "Administration", icon: Settings },
];

function NavContent({ onNavigate }: { onNavigate?: () => void }) {
  // Retry disabled and errors ignored on purpose: this footer chip is a
  // convenience, not core functionality, and must never block the shell
  // from rendering when the backend is unreachable.
  const { data } = useQuery({
    queryKey: ["ai-settings", "shell-footer"],
    queryFn: fetchAiSettings,
    retry: false,
    staleTime: 5 * 60 * 1000,
  });

  return (
    <>
      <div className="px-6 py-6">
        <Logo />
      </div>

      <nav aria-label="Primary" className="flex-1 space-y-1 px-3">
        {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            onClick={onNavigate}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-teal-50 text-teal-800"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`
            }
          >
            <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-slate-200 px-6 py-4 text-xs text-slate-400">
        {data?.settings ? (
          <>
            AI analysis model{" "}
            <span className="font-medium text-slate-500">{data.settings.feedback_model}</span> ·
            prompt {data.settings.feedback_prompt_version}
          </>
        ) : (
          <>Backend not connected</>
        )}
      </div>
    </>
  );
}

export function AppShell() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Mobile top bar */}
      <div className="flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 md:hidden">
        <Logo withTagline={false} size="sm" />
        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="rounded-md p-2 text-slate-500 hover:bg-slate-100"
          aria-label="Open navigation"
        >
          <Menu className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>

      {/* Mobile nav drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div className="absolute inset-0 bg-slate-900/30" onClick={() => setMobileOpen(false)} />
          <div className="absolute inset-y-0 left-0 flex w-72 flex-col bg-white shadow-xl">
            <div className="flex justify-end px-3 pt-3">
              <button
                type="button"
                onClick={() => setMobileOpen(false)}
                className="rounded-md p-2 text-slate-500 hover:bg-slate-100"
                aria-label="Close navigation"
              >
                <X className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>
            <NavContent onNavigate={() => setMobileOpen(false)} />
          </div>
        </div>
      )}

      <div className="flex">
        {/* Desktop sidebar */}
        <aside className="sticky top-0 hidden h-screen w-64 flex-col border-r border-slate-200 bg-white md:flex">
          <NavContent />
        </aside>

        <main className="min-w-0 flex-1 px-4 py-8 sm:px-8 lg:px-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
