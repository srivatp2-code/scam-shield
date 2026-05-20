export default function PrivacyNote() {
  return (
    <div
      role="note"
      className="rounded-2xl border border-gray-200 bg-gray-50 p-4 text-base text-gray-700"
    >
      <p>
        <span aria-hidden="true">🔒</span>{" "}
        Your message goes from your browser directly to Anthropic. Nothing is
        sent to us or stored anywhere else.
      </p>
    </div>
  );
}
