import { useState } from "react";
import { Eye, EyeOff, ChevronDown, ChevronUp } from "lucide-react";

interface ApiKeySetupProps {
  onSave: (key: string) => void;
  onClear?: () => void;
  onCancel?: () => void;
  existingKey?: string | null;
  mode: "onboarding" | "settings";
}

const ANTHROPIC_KEYS_URL = "https://console.anthropic.com/settings/keys";

export default function ApiKeySetup({
  onSave,
  onClear,
  onCancel,
  existingKey,
  mode,
}: ApiKeySetupProps) {
  const [value, setValue] = useState("");
  const [show, setShow] = useState(false);
  const [whyOpen, setWhyOpen] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = value.trim();
    if (trimmed.length === 0) return;
    onSave(trimmed);
  };

  const isSettings = mode === "settings";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {isSettings ? "Settings" : "Set up Scam Shield"}
        </h1>
        <p className="mt-2 text-base text-gray-700">
          {isSettings
            ? "Update or remove your Anthropic API key. The key is stored only on this device."
            : "Three quick steps. Takes about a minute."}
        </p>
      </div>

      <ol className="space-y-5">
        <li className="flex gap-4">
          <span className="flex-shrink-0 w-9 h-9 rounded-full bg-gray-900 text-white font-semibold flex items-center justify-center">
            1
          </span>
          <div className="flex-1 pt-1">
            <p className="text-lg font-semibold text-gray-900">
              Get an Anthropic API key
            </p>
            <p className="mt-1 text-base text-gray-700">
              It's free to start. Anthropic is the company that makes Claude.
            </p>
            <a
              href={ANTHROPIC_KEYS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-2 inline-block min-h-11 leading-[44px] underline text-gray-900 font-medium"
            >
              Open Anthropic's API key page →
            </a>
          </div>
        </li>

        <li className="flex gap-4">
          <span className="flex-shrink-0 w-9 h-9 rounded-full bg-gray-900 text-white font-semibold flex items-center justify-center">
            2
          </span>
          <div className="flex-1 pt-1">
            <label
              htmlFor="api-key"
              className="block text-lg font-semibold text-gray-900"
            >
              Paste it here
            </label>
            {existingKey && (
              <p className="mt-1 text-base text-gray-700">
                A key is already saved. Paste a new one to replace it.
              </p>
            )}
            <div className="mt-2 relative">
              <input
                id="api-key"
                type={show ? "text" : "password"}
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder="sk-ant-..."
                autoComplete="off"
                spellCheck={false}
                className="w-full min-h-11 px-4 pr-12 py-3 text-base rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-gray-900"
              />
              <button
                type="button"
                onClick={() => setShow((s) => !s)}
                aria-label={show ? "Hide API key" : "Show API key"}
                className="absolute right-1 top-1/2 -translate-y-1/2 min-w-11 min-h-11 w-11 h-11 flex items-center justify-center text-gray-600 hover:text-gray-900 rounded-lg"
              >
                {show ? (
                  <EyeOff className="w-5 h-5" aria-hidden="true" />
                ) : (
                  <Eye className="w-5 h-5" aria-hidden="true" />
                )}
              </button>
            </div>
          </div>
        </li>

        <li className="flex gap-4">
          <span className="flex-shrink-0 w-9 h-9 rounded-full bg-gray-900 text-white font-semibold flex items-center justify-center">
            3
          </span>
          <div className="flex-1 pt-1 space-y-3">
            <p className="text-lg font-semibold text-gray-900">Save</p>
            <form onSubmit={handleSubmit}>
              <button
                type="submit"
                disabled={value.trim().length === 0}
                className="w-full min-h-11 rounded-xl px-6 py-3 text-lg font-semibold bg-gray-900 text-white hover:bg-black disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
              >
                {isSettings ? "Save key" : "Save and continue"}
              </button>
            </form>
            {isSettings && onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="w-full min-h-11 rounded-xl px-6 py-3 text-lg font-semibold border border-gray-300 text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
              >
                Cancel
              </button>
            )}
            {isSettings && existingKey && onClear && (
              <button
                type="button"
                onClick={onClear}
                className="w-full min-h-11 rounded-xl px-6 py-3 text-base font-medium text-red-700 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-600"
              >
                Remove key from this device
              </button>
            )}
          </div>
        </li>
      </ol>

      <div className="rounded-2xl border border-gray-200 p-4">
        <button
          type="button"
          onClick={() => setWhyOpen((o) => !o)}
          aria-expanded={whyOpen}
          className="w-full flex items-center justify-between min-h-11 text-base font-semibold text-gray-900 text-left"
        >
          <span>Why do I need a key?</span>
          {whyOpen ? (
            <ChevronUp className="w-5 h-5" aria-hidden="true" />
          ) : (
            <ChevronDown className="w-5 h-5" aria-hidden="true" />
          )}
        </button>
        {whyOpen && (
          <div className="mt-3 text-base text-gray-700 space-y-2">
            <p>
              Scam Shield doesn't have its own servers. When you ask it to check
              a message, your browser talks directly to Anthropic — the company
              that makes the Claude AI used for the check.
            </p>
            <p>
              That's a "bring your own key" setup: you sign up with Anthropic,
              get a key, and paste it here. Your key stays on this device and is
              never sent to us. We don't have any way to see your messages or
              your key.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
