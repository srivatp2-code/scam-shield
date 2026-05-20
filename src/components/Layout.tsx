import type { ReactNode } from "react";
import { Shield, Settings } from "lucide-react";

interface LayoutProps {
  children: ReactNode;
  onSettingsClick?: () => void;
  showSettings?: boolean;
}

const GITHUB_URL = "https://github.com/sripusarla/scam-shield";

export default function Layout({
  children,
  onSettingsClick,
  showSettings = true,
}: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <header className="border-b border-gray-200">
        <div className="max-w-xl mx-auto w-full px-5 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-7 h-7 text-gray-900" strokeWidth={2} aria-hidden="true" />
            <span className="text-2xl font-bold text-gray-900 tracking-tight">
              Scam Shield
            </span>
          </div>
          {showSettings && onSettingsClick && (
            <button
              type="button"
              onClick={onSettingsClick}
              aria-label="Settings"
              className="min-w-11 min-h-11 w-11 h-11 flex items-center justify-center rounded-xl text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-900"
            >
              <Settings className="w-6 h-6" aria-hidden="true" />
            </button>
          )}
        </div>
      </header>

      <main className="flex-1">
        <div className="max-w-xl mx-auto w-full px-5 py-8 space-y-6">
          {children}
        </div>
      </main>

      <footer className="border-t border-gray-200 mt-12">
        <div className="max-w-xl mx-auto w-full px-5 py-6 text-center text-sm text-gray-600">
          <p>
            Open source · Your data stays private ·{" "}
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-gray-900"
            >
              GitHub
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}
