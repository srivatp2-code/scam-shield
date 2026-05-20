import { useEffect, useState } from "react";
import Layout from "./components/Layout";
import PrivacyNote from "./components/PrivacyNote";
import ApiKeySetup from "./components/ApiKeySetup";
import ScanInput from "./components/ScanInput";
import ResultCard from "./components/ResultCard";
import HistoryList from "./components/HistoryList";
import { scanMessage, ScanError } from "./lib/claude";
import type { ScanInput as ScanInputType } from "./lib/claude";
import {
  addToHistory,
  clearApiKey,
  clearHistory,
  getApiKey,
  getHistory,
  setApiKey as storeApiKey,
} from "./lib/storage";
import { loadPatterns } from "./lib/patterns";
import type { ScamPattern, ScanHistoryItem, ScanResult } from "./types";

type View =
  | "loading"
  | "needs-key"
  | "idle"
  | "scanning"
  | "result"
  | "settings";

function newId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

export default function App() {
  const [view, setView] = useState<View>("loading");
  const [apiKey, setApiKeyState] = useState<string | null>(null);
  const [patterns, setPatterns] = useState<ScamPattern[]>([]);
  const [history, setHistory] = useState<ScanHistoryItem[]>([]);
  const [currentResult, setCurrentResult] = useState<ScanResult | null>(null);
  const [scanError, setScanError] = useState<string | null>(null);

  useEffect(() => {
    const key = getApiKey();
    setApiKeyState(key);
    setHistory(getHistory());
    loadPatterns().then(setPatterns).catch(() => setPatterns([]));
    setView(key ? "idle" : "needs-key");
  }, []);

  const handleSaveKey = (key: string) => {
    storeApiKey(key);
    setApiKeyState(key);
    setScanError(null);
    setView("idle");
  };

  const handleClearKey = () => {
    clearApiKey();
    setApiKeyState(null);
    setView("needs-key");
  };

  const handleCancelSettings = () => {
    setView(currentResult ? "result" : "idle");
  };

  const handleScan = async (input: ScanInputType, preview: string) => {
    if (!apiKey) {
      setView("needs-key");
      return;
    }
    setScanError(null);
    setView("scanning");
    try {
      const result = await scanMessage(input, apiKey, patterns);
      const historyItem: ScanHistoryItem = {
        id: newId(),
        timestamp: Date.now(),
        input_preview: preview,
        result,
      };
      addToHistory(historyItem);
      setHistory(getHistory());
      setCurrentResult(result);
      setView("result");
    } catch (err) {
      const message =
        err instanceof ScanError
          ? err.message
          : "Something went wrong. Try again.";
      setScanError(message);
      setView("idle");
    }
  };

  const handleSelectHistoryItem = (item: ScanHistoryItem) => {
    setCurrentResult(item.result);
    setView("result");
  };

  const handleCheckAnother = () => {
    setCurrentResult(null);
    setScanError(null);
    setView("idle");
  };

  const handleClearHistory = () => {
    clearHistory();
    setHistory([]);
  };

  const openSettings = () => {
    setView("settings");
  };

  return (
    <Layout
      onSettingsClick={openSettings}
      showSettings={view !== "loading" && view !== "needs-key"}
    >
      {view === "loading" && (
        <p className="text-base text-gray-600">Loading…</p>
      )}

      {view === "needs-key" && (
        <ApiKeySetup mode="onboarding" onSave={handleSaveKey} />
      )}

      {view === "settings" && (
        <ApiKeySetup
          mode="settings"
          onSave={handleSaveKey}
          onClear={handleClearKey}
          onCancel={handleCancelSettings}
          existingKey={apiKey}
        />
      )}

      {(view === "idle" || view === "scanning") && (
        <>
          <PrivacyNote />
          <ScanInput
            onScan={handleScan}
            scanning={view === "scanning"}
            error={scanError}
            onDismissError={() => setScanError(null)}
          />
          <HistoryList
            items={history}
            onSelect={handleSelectHistoryItem}
            onClear={handleClearHistory}
          />
        </>
      )}

      {view === "result" && currentResult && (
        <ResultCard
          result={currentResult}
          onCheckAnother={handleCheckAnother}
        />
      )}
    </Layout>
  );
}
