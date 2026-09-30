from __future__ import annotations

from google import genai
from google.genai import types


class GeminiDocumentGenerator:
    """Generate legal-document drafts with Google's current Gemini SDK."""

    def __init__(self, api_key: str | None, model: str) -> None:
        self.model = model
        self.demo_mode = not bool(api_key)
        self._client = genai.Client(api_key=api_key) if api_key else None

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        if self.demo_mode:
            return self._demo_document(document_type, parties, terms, dates)

        prompt = self._build_prompt(document_type, parties, terms, dates)

        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.25,
                max_output_tokens=8000,
                system_instruction=(
                    "You are a legal-document drafting assistant. "
                    "Create a clear, structured draft from the supplied facts. "
                    "Never invent names, dates, amounts, addresses, laws, or facts. "
                    "If a necessary fact is missing, use a clearly marked placeholder "
                    "such as [MISSING INFORMATION]. "
                    "This is a drafting tool, not a lawyer."
                ),
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    @staticmethod
    def _build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        return f"""
Draft a professional legal document using ONLY the supplied information.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{dates}

Required structure:
1. Document title
2. Introductory/recital section
3. Parties
4. Definitions where useful
5. Main clauses appropriate to the document type
6. Terms and obligations
7. Term/termination where applicable
8. Confidentiality/intellectual property clauses only when relevant
9. Dispute/governing-law section only as a placeholder if jurisdiction is not supplied
10. Signatures

Use numbered headings and readable paragraphs.
Do not claim that the document is legally valid in a particular jurisdiction.
Do not cite laws unless the user supplied the jurisdiction and the law.
Do not add fictional details.
"""

    @staticmethod
    def _demo_document(
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        term_lines = [t.strip() for t in terms.split(";") if t.strip()]
        numbered_terms = "\n".join(
            f"{i}. {term}" for i, term in enumerate(term_lines, 1)
        )

        return f"""{document_type.upper()}

Effective Date: {dates}

1. PARTIES

{parties}

2. PURPOSE

This draft records the principal terms supplied by the user for the above
{document_type}.

3. TERMS AND CONDITIONS

{numbered_terms or "[MISSING INFORMATION]"}

4. GENERAL PROVISIONS

The parties should review any provisions required by the applicable
jurisdiction, including governing law, notices, dispute resolution,
termination, and statutory requirements.

5. SIGNATURES

Party 1: ______________________________
Name: _________________________________
Date: __________________________________

Party 2: ______________________________
Name: _________________________________
Date: __________________________________

DRAFTING NOTICE

This is a demonstration draft generated without a live Gemini API key.
Replace the placeholder content with the live AI-generated version before
using the application for actual drafting.
"""
