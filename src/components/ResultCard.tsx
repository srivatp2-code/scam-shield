import type { ScanResult, Verdict } from "../types";

interface ResultCardProps {
  result: ScanResult;
  onCheckAnother: () => void;
}

interface VerdictStyle {
  emoji: string;
  label: string;
  headerBg: string;
  headerText: string;
  border: string;
}

const VERDICT_STYLES: Record<Verdict, VerdictStyle> = {
  scam: {
    emoji: "🔴",
    label: "Scam",
    headerBg: "bg-red-600",
    headerText: "text-white",
    border: "border-red-600",
  },
  suspicious: {
    emoji: "🟡",
    label: "Suspicious",
    headerBg: "bg-yellow-500",
    headerText: "text-gray-900",
    border: "border-yellow-500",
  },
  safe: {
    emoji: "🟢",
    label: "Looks Safe",
    headerBg: "bg-green-600",
    headerText: "text-white",
    border: "border-green-600",
  },
};

export default function ResultCard({ result, onCheckAnother }: ResultCardProps) {
  const style = VERDICT_STYLES[result.verdict];

  return (
    <div className="space-y-6">
      <div
        className={`rounded-2xl overflow-hidden border-2 ${style.border} shadow-sm`}
      >
        <div className={`${style.headerBg} ${style.headerText} px-6 py-5`}>
          <p className="text-3xl font-bold flex items-center gap-3">
            <span aria-hidden="true">{style.emoji}</span>
            <span>{style.label}</span>
          </p>
        </div>

        <div className="p-6 space-y-6 bg-white">
          <p className="text-xl text-gray-900 leading-snug">
            {result.headline}
          </p>

          {result.red_flags.length > 0 && (
            <section>
              <h2 className="text-lg font-bold text-gray-900 mb-2">
                Red flags
              </h2>
              <ul className="space-y-2 list-disc list-outside pl-5">
                {result.red_flags.map((flag, i) => (
                  <li key={i} className="text-base text-gray-800 leading-snug">
                    {flag}
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section className="rounded-xl bg-gray-50 border border-gray-200 p-4">
            <h2 className="text-lg font-bold text-gray-900 mb-2">
              What to do
            </h2>
            <p className="text-base text-gray-800 leading-snug">
              {result.what_to_do}
            </p>
          </section>

          {result.verdict === "scam" && result.if_already_clicked && (
            <section className="rounded-xl bg-red-50 border border-red-200 p-4">
              <h2 className="text-lg font-bold text-red-900 mb-2">
                If you already clicked or replied
              </h2>
              <p className="text-base text-red-900 leading-snug">
                {result.if_already_clicked}
              </p>
            </section>
          )}
        </div>
      </div>

      <button
        type="button"
        onClick={onCheckAnother}
        className="w-full min-h-11 rounded-xl px-6 py-3 text-lg font-semibold bg-gray-900 text-white hover:bg-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
      >
        Check another message
      </button>
    </div>
  );
}
