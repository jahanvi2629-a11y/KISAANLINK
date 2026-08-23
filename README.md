# CIVICSYNC

**AI-powered Government Document Contradiction Engine** — a hackathon prototype.

CIVICSYNC accepts two government documents (circulars, acts, guidelines), extracts
their text, breaks them into statements, and flags statements that look like they
might **contradict** each other — with evidence and a confidence score, for a human
to review. It never claims a definite legal contradiction; it only flags *potential*
ones.

---

## 1. Folder Structure

```
CIVICSYNC/
│
├── app.py                     # Flask app: routes, upload handling, wiring
├── requirements.txt
├── README.md
├── .gitignore
│
├── backend/
│   ├── __init__.py
│   └── api.py                 # PDF/text extraction, cleaning, file validation
│
├── data/
│   └── sample_documents/
│       ├── policy_a.txt       # Demo mode sample document A
│       └── policy_b.txt       # Demo mode sample document B (contradicts A)
│
├── frontend/
│   ├── index.html             # Dashboard UI
│   ├── style.css              # Styling
│   └── script.js              # Upload + fetch + render logic
│
└── models/
    ├── __init__.py
    └── contradiction_engine.py  # TF-IDF similarity + rule-based contradiction logic
```

(`uploads_temp/` is created automatically at runtime to hold uploads briefly; it's
deleted right after each request and is git-ignored.)

---

## 2. Installation

```bash
# from inside the CIVICSYNC/ folder
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Run

```bash
python app.py
```

Then open: **http://127.0.0.1:5000**

---

## 4. How to Test

**Option A — Demo Mode (recommended for the hackathon demo):**
Click **"Run Demo Mode"** on the dashboard. This runs the engine on
`data/sample_documents/policy_a.txt` and `policy_b.txt`, which are written to
guarantee at least two clear contradictions (a "30 days vs 45 days" deadline
mismatch and a "mandatory vs optional" mismatch).

**Option B — Real upload:**
Upload any two `.pdf` or `.txt` files with overlapping topics using the two
upload boxes, then click **"Analyze Documents"**.

---

## 5. How the Team Divides the Work

| Member  | Role                              | Primary files to edit |
|---------|-----------------------------------|------------------------|
| Prachi  | Backend Engineer                  | `app.py`, `backend/api.py` |
| Avni    | Frontend Engineer                 | `frontend/index.html`, `frontend/style.css`, `frontend/script.js` |
| Arya    | Data Engineer                     | `backend/api.py` (extraction/cleaning), `data/sample_documents/` |
| Jahanvi | Recommendation & Contradiction Engine | `models/contradiction_engine.py` |

Everyone can read `app.py` since it's the thin glue layer — it's short on purpose
so the whole team can explain it to judges.

---

## 6. API Contract (Frontend ↔ Backend)

### Request — `POST /analyze`
`multipart/form-data` with two fields:
- `doc_a`: file (.pdf or .txt)
- `doc_b`: file (.pdf or .txt)

### Response — `200 OK`
```json
{
  "document_a": "policy_a.txt",
  "document_b": "policy_b.txt",
  "results": [
    {
      "document_a": "policy_a.txt",
      "document_b": "policy_b.txt",
      "statement_a": "Applications must be submitted within 30 days of the notification date.",
      "statement_b": "Applications must be submitted within 45 days of the notification date.",
      "similarity": 0.842,
      "is_contradiction": true,
      "confidence": 0.99,
      "reason": "Both statements refer to the same kind of measurement (day) but specify different values (30 vs 45)."
    }
  ]
}
```

### Error responses
- `400` — missing files / no file selected / disallowed file type
- `422` — text extraction produced empty text (e.g. a scanned/image-only PDF)

### Demo route — `GET /demo`
Same response shape as `/analyze`, but always runs on the bundled sample documents.
No request body needed.

---

## 7. 2-Minute Demo Script

1. **(0:00–0:20)** Open the dashboard. Explain the problem: government documents get
   amended over time, and contradictory clauses (deadlines, eligibility, fees) slip
   through unnoticed.
2. **(0:20–0:40)** Click **"Run Demo Mode"**. While it loads, explain: "This runs two
   real-looking policy circulars through our engine."
3. **(0:40–1:20)** Point at the results:
   - The **30 days vs 45 days** card — explain the "same unit, different number" rule.
   - The **mandatory vs optional** card — explain the "opposite keyword" rule.
   - Point out the confidence score and the "Potential Contradiction" label —
     emphasize this is a *flag for human review*, not a legal verdict.
4. **(1:20–1:50)** Upload two real short documents live (or the same demo files) via
   "Analyze Documents" to show the full upload → PDF extraction → TF-IDF similarity →
   rule check pipeline works end-to-end, not just canned demo data.
5. **(1:50–2:00)** Close with the vision: scale this to compare full acts/circulars
   at ministry level, with a human-in-the-loop verification workflow.

---

## 8. Key Concepts, Explained Simply

**TF-IDF (Term Frequency–Inverse Document Frequency)**
A way to turn a sentence into a list of numbers (a "vector") where words that are
distinctive to that sentence get a higher weight, and common words (like "the",
"and") get a lower weight. This lets us compare sentences mathematically.

**Cosine similarity**
Once two sentences are turned into vectors, cosine similarity measures how similar
their *direction* is — a score from 0 (completely unrelated) to 1 (near-identical
topic). We use this to find statement pairs worth comparing at all, *before* we
try to decide whether they contradict.

**Why similarity alone isn't enough**
Two statements can be highly similar in topic ("submission deadline") without
contradicting each other, or subtly related while stating opposite rules. That's
why, after finding similar statement pairs, we apply two simple explainable rules:

- **Rule 1 — Number mismatch:** if both statements mention the same kind of unit
  (days, months, rupees, %) but different numbers, it's very likely a contradiction
  (e.g. a changed deadline or fee).
- **Rule 2 — Opposite keywords:** if one statement says something is "mandatory"
  and a related statement says it's "optional" (or "must" vs "must not", etc.),
  that's flagged too.

**Why this counts as "explainable AI"**
Every flag comes with a human-readable `reason` string generated directly from the
rule that triggered it — there's no black-box scoring. A judge or teammate can
trace exactly why any card appeared.

**Confidence vs Similarity**
`similarity` is the raw TF-IDF/cosine score (topic relatedness).
`confidence` is our engine's certainty that a *contradiction* exists, which starts
from similarity and is boosted when a clear rule (number or negation mismatch)
fires. This mirrors the required data contract exactly.
