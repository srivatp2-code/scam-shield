import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import type { ScanHistoryItem, Verdict } from "../types";

interface HistoryListProps {
  items: ScanHistoryItem[];
  onSelect: (item: ScanHistoryItem) => void;
  onClear: () => void;
}

const VERDICT_DOT: Record<Verdict, string> = {
  scam: "bg-red-600",
  suspicious: "bg-yellow-500",
  safe: "bg-green-600",
};

const VERDICT_LABEL: Record<Verdict, string> = {
  scam: "Scam",
  suspicious: "Suspicious",
  safe: "Safe",
};

function relativeTime(ts: number): string {
  const diffMs = Date.now() - ts;
  const sec = Math.round(diffMs / 1000);
  if (sec < 60) return "Just now";
  const min = Math.round(sec / 60);
  if (min < 60) return min === 1 ? "1 min ago" : `${min} min ago`;
  const hr = Math.round(min / 60);
  if (hr < 24) return hr === 1 ? "1 hour ago" : `${hr} hours ago`;
  const day = Math.round(hr / 24);
  if (day < 7) return day === 1 ? "Yesterday" : `${day} days ago`;
  return new Date(ts).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

export default function HistoryList({
  items,
  onSelect,
  onClear,
}: HistoryListProps) {
  const [open, setOpen] = useState(false);

  if (items.length === 0) return null;

  return (
    <section className="rounded-2xl border border-gray-200">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="w-full flex items-center justify-between min-h-11 px-4 py-3 text-lg font-semibold text-gray-900 text-left"
      >
        <span>
          Recent scans{" "}
          <span className="text-gray-500 font-normal">({items.length})</span>
        </span>
        {open ? (
          <ChevronUp className="w-5 h-5" aria-hidden="true" />
        ) : (
          <ChevronDown className="w-5 h-5" aria-hidden="true" />
        )}
      </button>

      {open && (
        <div className="border-t border-gray-200">
          <ul className="divide-y divide-gray-200">
            {items.map((item) => (
              <li key={item.id}>
                <button
                  type="button"
                  onClick={() => onSelect(item)}
                  className="w-full flex items-center gap-3 px-4 py-3 min-h-11 text-left hover:bg-gray-50 focus:outline-none focus:bg-gray-50"
                >
                  <span
                    className={`flex-shrink-0 w-3 h-3 rounded-full ${VERDICT_DOT[item.result.verdict]}`}
                    aria-label={VERDICT_LABEL[item.result.verdict]}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-base text-gray-900 truncate">
                      {item.input_preview || "(empty)"}
                    </p>
                    <p className="text-sm text-gray-500">
                      {relativeTime(item.timestamp)}
                    </p>
                  </div>
                </button>
              </li>
            ))}
          </ul>
          <div className="px-4 py-3 border-t border-gray-200">
            <button
              type="button"
              onClick={onClear}
              className="text-base text-red-700 underline hover:text-red-900 min-h-11"
            >
              Clear history
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
