import { useRef, useState } from "react";
import { Upload, X, AlertCircle } from "lucide-react";
import type { ScanInput as ScanInputType } from "../lib/claude";

interface ScanInputProps {
  onScan: (input: ScanInputType, preview: string) => void;
  scanning: boolean;
  error: string | null;
  onDismissError: () => void;
}

interface PendingImage {
  base64: string;
  mediaType: string;
  fileName: string;
  dataUrl: string;
}

const PLACEHOLDER =
  'Example: "USPS: Your package is being held. Pay a $2.99 redelivery fee here: usps-redelivery.com/pay"';

function readFileAsDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = () => reject(new Error("Couldn't read that file."));
    reader.readAsDataURL(file);
  });
}

export default function ScanInput({
  onScan,
  scanning,
  error,
  onDismissError,
}: ScanInputProps) {
  const [text, setText] = useState("");
  const [image, setImage] = useState<PendingImage | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const hasInput = text.trim().length > 0 || image !== null;
  const canSubmit = hasInput && !scanning;

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    if (e.target.value.length > 0 && image) {
      setImage(null);
    }
    if (error) onDismissError();
  };

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setFileError(null);
    if (error) onDismissError();
    if (!file.type.startsWith("image/")) {
      setFileError("Please choose an image file (JPEG, PNG, GIF, or WebP).");
      return;
    }
    try {
      const dataUrl = await readFileAsDataUrl(file);
      const commaIdx = dataUrl.indexOf(",");
      const mediaMatch = dataUrl.slice(0, commaIdx).match(/data:(.*?);base64/);
      const mediaType = mediaMatch?.[1] ?? file.type;
      const base64 = dataUrl.slice(commaIdx + 1);
      setImage({ base64, mediaType, fileName: file.name, dataUrl });
      setText("");
    } catch {
      setFileError("Couldn't read that image. Try a different file.");
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    if (image) {
      onScan(
        { imageBase64: image.base64, imageMediaType: image.mediaType },
        "[image]",
      );
    } else {
      onScan({ text }, text.slice(0, 120));
    }
  };

  const clearImage = () => {
    setImage(null);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" noValidate>
      <div>
        <label
          htmlFor="scan-text"
          className="block text-2xl font-bold text-gray-900"
        >
          Paste the message here
        </label>
        <p className="mt-1 text-base text-gray-600">
          A text, email, or anything that looks suspicious.
        </p>
      </div>

      <textarea
        id="scan-text"
        value={text}
        onChange={handleTextChange}
        disabled={scanning || image !== null}
        placeholder={PLACEHOLDER}
        rows={6}
        className="w-full px-4 py-3 text-base rounded-2xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-gray-900 disabled:bg-gray-100 disabled:cursor-not-allowed resize-y"
      />

      {image ? (
        <div className="rounded-2xl border border-gray-200 p-4 flex items-start gap-4">
          <img
            src={image.dataUrl}
            alt="Selected screenshot preview"
            className="w-20 h-20 object-cover rounded-xl border border-gray-200 flex-shrink-0"
          />
          <div className="flex-1 min-w-0">
            <p className="text-base font-medium text-gray-900 truncate">
              {image.fileName}
            </p>
            <p className="text-sm text-gray-600 mt-1">
              We'll analyze this screenshot.
            </p>
          </div>
          <button
            type="button"
            onClick={clearImage}
            disabled={scanning}
            aria-label="Remove selected image"
            className="min-w-11 min-h-11 w-11 h-11 flex items-center justify-center rounded-xl text-gray-700 hover:bg-gray-100 disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-gray-900"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>
      ) : (
        <div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFile}
            className="hidden"
            id="scan-file"
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={scanning}
            className="w-full min-h-11 rounded-xl px-6 py-3 text-lg font-semibold border-2 border-gray-300 text-gray-900 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
          >
            <Upload className="w-5 h-5" aria-hidden="true" />
            <span>Or upload a screenshot</span>
          </button>
        </div>
      )}

      {fileError && (
        <div
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 p-3 text-base text-red-800 flex items-start gap-2"
        >
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <span>{fileError}</span>
        </div>
      )}

      {error && (
        <div
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 p-3 text-base text-red-800 flex items-start gap-2"
        >
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <span>{error}</span>
        </div>
      )}

      <button
        type="submit"
        disabled={!canSubmit}
        className="w-full min-h-11 rounded-xl px-6 py-3 text-lg font-semibold bg-gray-900 text-white hover:bg-black disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
      >
        {scanning ? "Reading the message…" : "Check this message"}
      </button>
    </form>
  );
}
