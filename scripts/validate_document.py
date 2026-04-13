"""
validate_document.py — Utility module for validating expanded_research_document.md.

Exposes:
  word_count(text)          -> int
  count_mermaid_blocks(text) -> int
  find_forbidden_terms(text) -> list
  find_apa_citations(text)   -> list
  main()                     -> prints a summary report
"""

import re
from pathlib import Path

DOCUMENT_PATH = Path(__file__).parent.parent / "Documents" / "expanded_research_document.md"

FORBIDDEN_TERMS = [
    "Flask", "Django", "Laravel", "React", "Vue", "Angular",
    "Bootstrap", "Tailwind", "MySQL", "MongoDB", "AWS",
]

APA_CITATION_PATTERN = re.compile(
    r'\([A-Z][a-z]+(?:\s+et\s+al\.)?,\s+\d{4}\)'
)


def word_count(text: str) -> int:
    """Return the number of whitespace-delimited words in text."""
    return len(text.split())


def count_mermaid_blocks(text: str) -> int:
    """Count the number of fenced ```mermaid blocks in text."""
    return len(re.findall(r'```mermaid', text))


def find_forbidden_terms(text: str) -> list:
    """Return forbidden tech terms found as positive technology claims (not negations)."""
    found = []
    for term in FORBIDDEN_TERMS:
        # Only flag if used as a positive claim (not in "not X", "no X", "without X" etc.)
        positive_pattern = re.compile(
            r'(?:using|built with|implemented in|powered by|based on|'
            r'framework is|library is|backend is|frontend is|we use)\s+'
            + re.escape(term),
            re.IGNORECASE,
        )
        if positive_pattern.search(text):
            found.append(term)
    return found


def find_apa_citations(text: str) -> list:
    """Return a list of APA citation matches using the standard (Author, Year) pattern."""
    return APA_CITATION_PATTERN.findall(text)


def main():
    """Load the master document and print a validation summary report."""
    if not DOCUMENT_PATH.exists():
        print(f"ERROR: Document not found at {DOCUMENT_PATH}")
        return

    text = DOCUMENT_PATH.read_text(encoding="utf-8")

    wc = word_count(text)
    mermaid = count_mermaid_blocks(text)
    forbidden = find_forbidden_terms(text)
    citations = find_apa_citations(text)

    print("=" * 60)
    print("DOCUMENT VALIDATION REPORT")
    print("=" * 60)
    print(f"File          : {DOCUMENT_PATH}")
    print(f"Word count    : {wc:,}  (target: ≥75,000)")
    print(f"Mermaid blocks: {mermaid}  (target: ≥11)")
    print(f"APA citations : {len(citations)}")
    print(f"Forbidden terms found: {forbidden if forbidden else 'None'}")
    print("=" * 60)

    if wc < 75000:
        print(f"  [WARN] Word count {wc:,} is below the 75,000-word target.")
    if mermaid < 11:
        print(f"  [WARN] Only {mermaid} Mermaid block(s) found; need ≥11.")
    if forbidden:
        print(f"  [WARN] Forbidden terms detected: {', '.join(forbidden)}")
    if not forbidden and wc >= 75000 and mermaid >= 11:
        print("  [OK] All checks passed.")


if __name__ == "__main__":
    main()
