# Contributing to Scam Shield

Thank you for helping make Scam Shield smarter. The most useful thing most people can contribute is a new **scam pattern** — a description of a scam you've seen so Claude can spot it more reliably for everyone else.

## Adding a new scam pattern

Each scam pattern is a single JSON file in [`src/scam-patterns/`](../src/scam-patterns/). The file shape is:

```json
{
  "id": "kebab-case-id",
  "name": "Short human name",
  "description": "One or two sentences describing how this scam works.",
  "example": "A short sanitized example of the message a victim would receive.",
  "red_flags": [
    "Specific tell #1",
    "Specific tell #2",
    "Specific tell #3"
  ],
  "category": "delivery"
}
```

### Steps

1. **Pick a unique `id`.** Use kebab-case (lowercase letters and hyphens). The id should match the filename (e.g. `id: "fake-bank-alert"` → file `fake-bank-alert.json`).
2. **Choose a `category`** from this list:
   - `delivery` — fake USPS / FedEx / Amazon delivery messages
   - `government` — IRS, Social Security, police, DMV impersonation
   - `financial` — fake refunds, account alerts, "your card was charged"
   - `romance` — wrong-number pivots, dating-app scams, "pig butchering"
   - `employment` — fake job offers, work-from-home schemes, fake checks
   - `tech-support` — virus warnings, fake Microsoft/Apple support calls
   - `other` — anything that doesn't fit above
3. **Write a sanitized `example`** — see the privacy rules below.
4. **List 3–6 `red_flags`** — concrete, observable features of the scam, not generic advice. "Asks for gift card payment" is good; "feels off" is not.
5. **Add an entry to [`index.json`](../src/scam-patterns/index.json)** with the id and category.
6. **Open a pull request** with a title like `pattern: add fake-bank-alert`.

### Privacy rules — read this before you submit

> ⚠️ **Do not include real personal information from messages you've received.** Sanitize the example before committing:
>
> - Replace real **names** with placeholder names (David, Sarah, etc.)
> - Replace real **phone numbers** with `1-888-555-0173` or similar (555-prefix isn't a real assignable range)
> - Replace real **URLs** with bracket notation: `paypal-secure[.]com` (so the link can't be clicked accidentally)
> - Replace real **dollar amounts** if they could identify a specific case, but it's fine to keep representative amounts (e.g. "$2.99 fee")
> - Replace **order/case/reference numbers** with obviously fake ones
> - Remove **email addresses** unless they're clearly fabricated examples
>
> Pull requests that include real PII will be asked to sanitize before merge.

### What makes a good pattern

- **Specific.** "Asks for payment in iTunes gift cards" beats "asks for unusual payment."
- **Observable.** Things a non-technical reader could plausibly notice — phrases, payment methods, claimed senders, urgency tactics.
- **Distinct.** If your pattern overlaps heavily with an existing one, consider improving the existing one instead of adding a duplicate.
- **Sanitized.** Worth saying twice.

## Other contributions

- **Bug reports and feature ideas:** open an issue.
- **UI / accessibility fixes:** PRs welcome. Please test in a 375 px viewport.
- **Translations:** not yet supported — but the conventions in [`CLAUDE.md`](../CLAUDE.md) about plain language apply doubly to any translated copy.

By contributing, you agree your contribution is released under the project's MIT license.
