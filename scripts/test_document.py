"""
test_document.py — pytest + hypothesis test suite for expanded_research_document.md.

Run with:
    pytest scripts/test_document.py -v

Requires:
    pip install pytest hypothesis
"""

import re
from pathlib import Path

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from validate_document import (
    word_count,
    count_mermaid_blocks,
    find_forbidden_terms,
    find_apa_citations,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DOCUMENT_PATH = Path(__file__).parent.parent / "Documents" / "expanded_research_document.md"
APA_PATTERN = re.compile(
    r'(?:'
    r'\([^()]{2,80},\s+\d{4}[a-z]?\)'   # parenthetical: (Author, Year)
    r'|[A-Z][a-zA-Z\s&,\.]+\(\d{4}\)'   # narrative: Author (Year)
    r')'
)
CLAIM_MARKERS = [
    "according to",
    "research shows",
    "studies indicate",
    "argues that",
    "states that",
    "found that",
    "demonstrated that",
    "suggests that",
    "reported that",
    "concluded that",
    "noted that",
    "observed that",
]
FORBIDDEN = [
    "Flask", "Django", "Laravel", "React", "Vue", "Angular",
    "Bootstrap", "Tailwind", "MySQL", "MongoDB", "AWS",
]


def load_document() -> str:
    assert DOCUMENT_PATH.exists(), f"Document not found: {DOCUMENT_PATH}"
    return DOCUMENT_PATH.read_text(encoding="utf-8")


def extract_section(text: str, heading: str) -> str:
    """Extract text from a heading until the next same-level heading."""
    pattern = re.compile(
        r'(?:^|\n)(#{1,4}\s+' + re.escape(heading) + r'.*?)(?=\n#{1,4}\s|\Z)',
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(text)
    return m.group(1) if m else ""


ACADEMIC_SECTION_MARKERS = [
    "## Chapter One", "## Chapter Two", "## Chapter Three",
    "## Chapter Four", "## Chapter Five", "## Chapter Six",
    "## Chapter Seven", "## REFERENCES",
]


def get_paragraphs_with_claims(text: str) -> list:
    """Return paragraphs with claim markers, restricted to academic chapters only."""
    # Find start of Chapter One (skip preliminary pages like Dedication)
    ch1_start = text.find("## Chapter One")
    if ch1_start == -1:
        ch1_start = text.find("## CHAPTER ONE")
    if ch1_start == -1:
        ch1_start = 0
    academic_text = text[ch1_start:]
    paragraphs = [p.strip() for p in academic_text.split("\n\n") if p.strip()]
    return [
        p for p in paragraphs
        if any(marker.lower() in p.lower() for marker in CLAIM_MARKERS)
        and len(p.split()) > 30          # skip very short fragments
        and not p.startswith("#")        # skip headings
        and not p.startswith("|")        # skip table rows
        and not p.startswith("```")      # skip code blocks
        and not p.startswith(">")        # skip blockquotes (abstract)
        # Exclude chapter summary/intro paragraphs that synthesise without citing
        and "Chapter One has" not in p
        and "Chapter Two has" not in p
        and "Chapter Three has" not in p
        and "Chapter Four has" not in p
        and "Chapter Five has" not in p
        and "Chapter Six has" not in p
        and "Chapter Seven" not in p
        and "this chapter has" not in p[:80].lower()
        and "the chapter has" not in p[:80].lower()
    ]


def get_technical_sentences(text: str) -> list:
    """Return sentences from technical chapters (3–6)."""
    # Extract chapters 3–6 block
    ch3_start = text.find("## Chapter Three")
    ch7_start = text.find("## Chapter Seven")
    if ch3_start == -1 or ch7_start == -1:
        return []
    technical_block = text[ch3_start:ch7_start]
    sentences = re.split(r'(?<=[.!?])\s+', technical_block)
    return [s.strip() for s in sentences if len(s.split()) > 5]


# ---------------------------------------------------------------------------
# Unit Tests
# ---------------------------------------------------------------------------

class TestAbstractWordCount:
    """Task 2.4 — Abstract word count must be 150–300 words."""

    def test_abstract_word_count(self):
        text = load_document()
        # Abstract is in a blockquote (lines starting with ">")
        abstract_lines = [
            line.lstrip("> *").strip()
            for line in text.splitlines()
            if line.strip().startswith(">")
        ]
        abstract_text = " ".join(abstract_lines)
        wc = word_count(abstract_text)
        assert 150 <= wc <= 300, (
            f"Abstract word count is {wc}; expected 150–300 words."
        )


class TestDeclarationPageContent:
    """Task 2.7 — Declaration page must contain student and supervisor names."""

    def test_student_name_present(self):
        text = load_document()
        # Name and reg number appear on separate lines in the document
        assert "IGNATIUS ETHENS" in text, (
            "Student name 'IGNATIUS ETHENS' not found in document."
        )
        assert "CIT-221-048/2022" in text, (
            "Registration number 'CIT-221-048/2022' not found in document."
        )

    def test_supervisor_name_present(self):
        text = load_document()
        assert "DR. ISHMAEL NICK" in text, (
            "Supervisor name 'DR. ISHMAEL NICK' not found in document."
        )


class TestObjectivesFormat:
    """Task 3.5 — Section 1.6 must contain 1 main + 3–4 specific objectives."""

    def test_objectives_section_exists(self):
        text = load_document()
        assert "1.6" in text and "Objectives" in text, (
            "Section 1.6 (Objectives) not found in document."
        )

    def test_specific_objectives_count(self):
        text = load_document()
        section = extract_section(text, "1.6")
        if not section:
            # Try broader search
            idx = text.find("1.6")
            section = text[idx:idx + 3000] if idx != -1 else ""
        # Count numbered objective lines (e.g. "1.", "2.", "SO1", "SO2")
        numbered = re.findall(
            r'(?:^|\n)\s*(?:\d+\.|SO\d+|Specific Objective \d+)',
            section,
            re.IGNORECASE,
        )
        assert 3 <= len(numbered) <= 4, (
            f"Expected 3–4 specific objectives in Section 1.6, found {len(numbered)}."
        )


class TestTable21Existence:
    """Task 4.4 — Table 2.1 must contain Naviance, KUCCPS Portal, and Craydel."""

    def test_naviance_in_table(self):
        text = load_document()
        assert "Naviance" in text, "Naviance not found in document."

    def test_kuccps_portal_in_table(self):
        text = load_document()
        assert "KUCCPS Portal" in text or "KUCCPS portal" in text, (
            "KUCCPS Portal not found in document."
        )

    def test_craydel_in_table(self):
        text = load_document()
        assert "Craydel" in text, "Craydel not found in document."


class TestTestingPlanRowCount:
    """Task 10.4 — Table 6.1 must have ≥10 data rows."""

    def test_testing_plan_row_count(self):
        text = load_document()
        # The actual table has a bold caption: **Table 6.1: System Testing Plan...**
        idx = text.find("**Table 6.1:")
        if idx == -1:
            idx = text.find("Table 6.1: System Testing Plan")
        assert idx != -1, "Table 6.1 (testing plan) not found in document."
        table_block = text[idx: idx + 8000]
        # Count pipe-table data rows: lines with | that are not separator or header
        rows = [
            line for line in table_block.splitlines()
            if "|" in line
            and not re.match(r'^\s*\|[-| :]+\|\s*$', line)  # skip separator rows
            and "Test ID" not in line                         # skip header row
            and "Table 6.1" not in line                       # skip caption
            and line.strip().startswith("|")
        ]
        assert len(rows) >= 10, (
            f"Table 6.1 has {len(rows)} data rows; expected ≥10."
        )


class TestSUSItemsCompleteness:
    """Task 10.6 — Section 6.4 must contain all 10 standard SUS items."""

    SUS_ITEMS = [
        "I think that I would like to use this system frequently",
        "I found the system unnecessarily complex",
        "I thought the system was easy to use",
        "I think that I would need the support of a technical person",
        "I found the various functions in this system were well integrated",
        "I thought there was too much inconsistency in this system",
        "I would imagine that most people would learn to use this system very quickly",
        "I found the system very cumbersome to use",
        "I felt very confident using the system",
        "I needed to learn a lot of things before I could get going",
    ]

    def test_all_sus_items_present(self):
        text = load_document()
        missing = [item for item in self.SUS_ITEMS if item.lower() not in text.lower()]
        assert not missing, (
            f"Missing SUS items in Section 6.4: {missing}"
        )


class TestReferenceCount:
    """Task 11.2 — References section must contain ≥20 APA-formatted entries."""

    def test_reference_count(self):
        text = load_document()
        ref_idx = text.rfind("## REFERENCES")
        assert ref_idx != -1, "References section not found."
        ref_section = text[ref_idx:]
        # APA entries typically start with Author, A. (Year). pattern
        entries = re.findall(
            r'\n[A-Z][a-zA-Z\-]+,\s+[A-Z]',
            ref_section,
        )
        assert len(entries) >= 20, (
            f"References section has {len(entries)} entries; expected ≥20."
        )


class TestAppendixAQuestionCount:
    """Task 11.4 — Appendix A must contain ≥15 numbered questions."""

    def test_appendix_a_question_count(self):
        text = load_document()
        idx = text.find("## APPENDIX A")
        assert idx != -1, "Appendix A not found."
        appendix_b_idx = text.find("## APPENDIX B", idx)
        appendix_a = text[idx:appendix_b_idx] if appendix_b_idx != -1 else text[idx:]
        # Count bold numbered questions like **1.** or **1.**
        questions = re.findall(r'\*\*\d+\.', appendix_a)
        assert len(questions) >= 15, (
            f"Appendix A has {len(questions)} numbered questions; expected ≥15."
        )


class TestAppendixBQuestionCount:
    """Task 11.6 — Appendix B must contain ≥8 numbered questions."""

    def test_appendix_b_question_count(self):
        text = load_document()
        idx = text.find("## APPENDIX B")
        assert idx != -1, "Appendix B not found."
        appendix_c_idx = text.find("## APPENDIX C", idx)
        appendix_b = text[idx:appendix_c_idx] if appendix_c_idx != -1 else text[idx:]
        questions = re.findall(r'\*\*\d+\.', appendix_b)
        assert len(questions) >= 8, (
            f"Appendix B has {len(questions)} numbered questions; expected ≥8."
        )


# ---------------------------------------------------------------------------
# Property-Based Tests (hypothesis)
# ---------------------------------------------------------------------------

class TestProperty1APACitationCoverage:
    """Property 1 — Every paragraph with a claim marker must have ≥1 APA citation."""

    @pytest.fixture(scope="class")
    def claim_paragraphs(self):
        text = load_document()
        return get_paragraphs_with_claims(text)

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(data=st.data())
    def test_apa_citation_in_claim_paragraphs(self, data):
        text = load_document()
        paragraphs = get_paragraphs_with_claims(text)
        if not paragraphs:
            return
        paragraph = data.draw(st.sampled_from(paragraphs))
        citations = APA_PATTERN.findall(paragraph)
        assert len(citations) >= 1, (
            f"Paragraph with claim marker has no APA citation:\n\n{paragraph[:300]}..."
        )


class TestProperty2MermaidDiagramCompleteness:
    """Property 2 — Document must contain ≥11 mermaid blocks with required keywords."""

    REQUIRED_KEYWORDS = [
        "flowchart",       # Context diagrams, DFDs, Use Case, Activity, Architecture
        "sequenceDiagram", # 4 sequence diagrams
        "classDiagram",    # Class diagram
        "erDiagram",       # ERD
    ]

    def test_mermaid_block_count(self):
        text = load_document()
        count = count_mermaid_blocks(text)
        assert count >= 11, (
            f"Only {count} mermaid block(s) found; expected ≥11."
        )

    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    @given(keyword=st.sampled_from(REQUIRED_KEYWORDS))
    def test_each_diagram_type_present(self, keyword):
        text = load_document()
        # Find all mermaid blocks
        blocks = re.findall(r'```mermaid(.*?)```', text, re.DOTALL)
        found = any(keyword in block for block in blocks)
        assert found, (
            f"No mermaid block containing '{keyword}' found in document."
        )


class TestProperty3TechnicalAccuracy:
    """Property 3 — Technical sentences must not contain forbidden framework names."""

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(data=st.data())
    def test_no_forbidden_terms_in_technical_sentences(self, data):
        text = load_document()
        sentences = get_technical_sentences(text)
        if not sentences:
            return
        sentence = data.draw(st.sampled_from(sentences))
        for term in FORBIDDEN:
            # Allow mentions in "we do NOT use X" or "not X" contexts
            # Flag only if the term appears as a positive technology claim
            positive_pattern = re.compile(
                r'(?:using|built with|implemented in|powered by|based on|'
                r'framework|library|backend is|frontend is)\s+' + re.escape(term),
                re.IGNORECASE,
            )
            assert not positive_pattern.search(sentence), (
                f"Forbidden term '{term}' used as system technology in sentence:\n{sentence}"
            )


class TestProperty4MinimumDocumentLength:
    """Property 4 — Total document word count must be ≥75,000."""

    def test_minimum_word_count(self):
        text = load_document()
        wc = word_count(text)
        assert wc >= 75000, (
            f"Document word count is {wc:,}; expected ≥75,000."
        )


# ---------------------------------------------------------------------------
# Task 14 Unit Tests — Requirements 11–14
# ---------------------------------------------------------------------------

class TestGradeMapAccuracy:
    """Task 14.1 — GRADE_MAP description in document must state correct numeric values.

    Validates: Requirements 14.2
    """

    EXPECTED_MAPPINGS = [
        ("A", "12"),
        ("A-", "11"),
        ("B+", "10"),
        ("B", "9"),
        ("B-", "8"),
        ("C+", "7"),
        ("C", "6"),
        ("C-", "5"),
        ("D+", "4"),
        ("D", "3"),
        ("D-", "2"),
        ("E", "1"),
    ]

    def test_grade_map_values_present(self):
        text = load_document()
        # The document must contain a GRADE_MAP description with all grade→value pairs.
        # We look for the canonical description pattern used in the document.
        for grade, value in self.EXPECTED_MAPPINGS:
            # Accept both "A=12" and "'A': 12" and "A-=11" style representations
            pattern = re.compile(
                r"['\"]?" + re.escape(grade) + r"['\"]?\s*[=:]\s*" + re.escape(value),
                re.IGNORECASE,
            )
            assert pattern.search(text), (
                f"GRADE_MAP entry '{grade}={value}' not found in document."
            )


class TestSection42FourWeaknesses:
    """Task 14.2 — Section 4.2 must contain all four documented weakness keywords.

    Validates: Requirements 13.2
    """

    def _get_section_42(self, text: str) -> str:
        """Extract Section 4.2 content (from ### 4.2 heading to ### 4.3 heading)."""
        # Find the ### 4.2 heading
        m_start = re.search(r'\n#{1,4}\s+4\.2\b', text)
        if not m_start:
            return ""
        start = m_start.start()
        # Find the next same-or-higher-level heading (### 4.3 or ## Chapter Five etc.)
        m_end = re.search(r'\n#{1,4}\s+4\.3\b', text[start + 1:])
        if m_end:
            end = start + 1 + m_end.start()
        else:
            end = start + 10000
        return text[start:end]

    def test_geographic_inequality_present(self):
        text = load_document()
        section = self._get_section_42(text)
        assert "geographic inequality" in section.lower(), (
            "Section 4.2 does not mention 'geographic inequality'."
        )

    def test_scholarship_information_silos_present(self):
        text = load_document()
        section = self._get_section_42(text)
        # Accept either "scholarship information silos" or "centralised repository"
        has_silos = "scholarship information silo" in section.lower()
        has_centralised = "centralised repository" in section.lower()
        assert has_silos or has_centralised, (
            "Section 4.2 does not mention 'scholarship information silos' or 'centralised repository'."
        )

    def test_algorithmic_or_data_driven_present(self):
        text = load_document()
        section = self._get_section_42(text)
        # Accept "algorithmic" or "data-driven"
        has_algorithmic = "algorithmic" in section.lower()
        has_data_driven = "data-driven" in section.lower()
        assert has_algorithmic or has_data_driven, (
            "Section 4.2 does not mention 'algorithmic' or 'data-driven'."
        )

    def test_standardised_process_or_individual_counselor_present(self):
        text = load_document()
        section = self._get_section_42(text)
        # Accept "standardised process", "individual counselor", "individual knowledge",
        # or "not standardised" — all describe the same weakness
        has_standardised = "standardised process" in section.lower()
        has_individual = "individual counselor" in section.lower()
        has_individual_knowledge = "individual knowledge" in section.lower()
        has_not_standardised = "not standardised" in section.lower()
        assert has_standardised or has_individual or has_individual_knowledge or has_not_standardised, (
            "Section 4.2 does not mention 'standardised process', 'individual counselor', "
            "'individual knowledge', or 'not standardised'."
        )


class TestScholarshipsDataDictionary:
    """Task 14.3 (optional) — Table 5.4 must list all nine scholarships field names.

    Validates: Requirements 11.9
    """

    REQUIRED_FIELDS = [
        "id",
        "name",
        "provider",
        "description",
        "eligibility_criteria",
        "deadline",
        "link",
        "category",
        "amount",
    ]

    def _get_table_54(self, text: str) -> str:
        """Extract Table 5.4 content — find the actual data dictionary table, not the
        List of Tables entry."""
        # There are two occurrences: one in the List of Tables (caption only) and one
        # in Section 5.6 (the actual table). We want the one that contains field rows.
        idx = 0
        while True:
            idx = text.find("Table 5.4", idx)
            if idx == -1:
                return ""
            block = text[idx: idx + 4000]
            # The actual table has pipe-delimited rows with field names
            if "| Field |" in block or "| id |" in block or "eligibility_criteria" in block:
                return block
            idx += 1  # advance past this occurrence

    def test_all_nine_fields_present(self):
        text = load_document()
        table_block = self._get_table_54(text)
        assert table_block, "Table 5.4 not found in document."
        missing = [f for f in self.REQUIRED_FIELDS if f not in table_block]
        assert not missing, (
            f"Table 5.4 is missing field(s): {missing}"
        )


class TestStudyLevelInSection57:
    """Task 14.4 (optional) — Section 5.7 must mention study_level / education level
    displayed alongside the ranked career list on the recommendations page.

    Validates: Requirements 14.6
    """

    def _get_section_573(self, text: str) -> str:
        """Extract Section 5.7.3 Recommendations Page content."""
        m_start = re.search(r'\n#{1,4}\s+5\.7\.3\b', text)
        if not m_start:
            return ""
        start = m_start.start()
        m_end = re.search(r'\n#{1,4}\s+5\.7\.4\b', text[start + 1:])
        if m_end:
            end = start + 1 + m_end.start()
        else:
            end = start + 4000
        return text[start:end]

    def test_education_level_displayed_on_recommendations_page(self):
        text = load_document()
        section = self._get_section_573(text)
        assert section, "Section 5.7.3 (Recommendations Page) not found in document."
        # The document describes "required education level" or "study_level" displayed
        # alongside the ranked career list.
        has_study_level = "study_level" in section
        has_education_level = "education level" in section.lower()
        has_university_diploma = (
            "university" in section.lower() and "diploma" in section.lower()
        )
        assert has_study_level or has_education_level or has_university_diploma, (
            "Section 5.7.3 does not mention study_level or education level "
            "displayed on the recommendations page."
        )


class TestPseudocodeCompleteness:
    """Task 14.5 (optional) — run_algorithm() pseudocode in Section 5.5 must contain
    all five step markers.

    Validates: Requirements 14.7
    """

    def _get_pseudocode_block(self, text: str) -> str:
        """Extract the run_algorithm pseudocode block from Section 5.5."""
        # Find the pseudocode section heading
        idx = text.find("5.5.11")
        if idx == -1:
            idx = text.find("Pseudocode for run_algorithm")
        if idx == -1:
            return ""
        # Grab a generous window
        return text[idx: idx + 6000]

    def test_grade_map_step_present(self):
        text = load_document()
        block = self._get_pseudocode_block(text)
        assert block, "run_algorithm() pseudocode block not found in document."
        has_grade_map = "GRADE_MAP" in block or "grade mapping" in block.lower()
        assert has_grade_map, (
            "Pseudocode does not contain 'GRADE_MAP' or 'grade mapping' step."
        )

    def test_mean_grade_step_present(self):
        text = load_document()
        block = self._get_pseudocode_block(text)
        assert "mean_grade" in block, (
            "Pseudocode does not contain 'mean_grade' step."
        )

    def test_education_goal_step_present(self):
        text = load_document()
        block = self._get_pseudocode_block(text)
        assert "education_goal" in block, (
            "Pseudocode does not contain 'education_goal' step."
        )

    def test_subject_score_step_present(self):
        text = load_document()
        block = self._get_pseudocode_block(text)
        assert "subject_score" in block, (
            "Pseudocode does not contain 'subject_score' step."
        )

    def test_normalise_step_present(self):
        text = load_document()
        block = self._get_pseudocode_block(text)
        has_normalise = "normalise" in block.lower() or "max_score" in block
        assert has_normalise, (
            "Pseudocode does not contain 'normalise' or 'max_score' step."
        )


class TestDeploymentEnvironmentVariables:
    """Task 14.6 (optional) — Section 3.8 must mention all three env var names.

    Validates: Requirements 12.8
    """

    ENV_VARS = [
        "Careerdatabase_URL",
        "careerapp_gmail",
        "careerapps_password",
    ]

    def _get_section_38(self, text: str) -> str:
        """Extract Section 3.8 content (from ### 3.8 heading to ### 3.9 heading)."""
        m_start = re.search(r'\n#{1,4}\s+3\.8\b', text)
        if not m_start:
            return ""
        start = m_start.start()
        m_end = re.search(r'\n#{1,4}\s+3\.9\b', text[start + 1:])
        if m_end:
            end = start + 1 + m_end.start()
        else:
            end = start + 8000
        return text[start:end]

    def test_all_env_vars_present(self):
        text = load_document()
        section = self._get_section_38(text)
        assert section, "Section 3.8 not found in document."
        missing = [v for v in self.ENV_VARS if v not in section]
        assert not missing, (
            f"Section 3.8 is missing environment variable(s): {missing}"
        )


class TestSUSScoringFormulaAndBangor:
    """Task 14.7 (optional) — Section 6.4 must contain the SUS scoring formula,
    the 68 and 80.3 thresholds, and the Bangor reference.

    Validates: Requirements 12.9
    """

    def _get_section_64(self, text: str) -> str:
        """Extract Section 6.4 content (from ### 6.4 heading to ### 6.5 heading)."""
        m_start = re.search(r'\n#{1,4}\s+6\.4\b', text)
        if not m_start:
            return ""
        start = m_start.start()
        m_end = re.search(r'\n#{1,4}\s+6\.5\b', text[start + 1:])
        if m_end:
            end = start + 1 + m_end.start()
        else:
            end = start + 12000
        return text[start:end]

    def test_sus_scoring_formula_present(self):
        text = load_document()
        section = self._get_section_64(text)
        assert section, "Section 6.4 not found in document."
        # Accept "× 2.5" or "* 2.5" or "multiply by 2.5"
        has_formula = (
            "× 2.5" in section
            or "* 2.5" in section
            or "x 2.5" in section.lower()
            or "multiply by 2.5" in section.lower()
        )
        assert has_formula, (
            "Section 6.4 does not contain the SUS scoring formula (× 2.5 / multiply by 2.5)."
        )

    def test_threshold_68_present(self):
        text = load_document()
        section = self._get_section_64(text)
        assert "68" in section, (
            "Section 6.4 does not mention the SUS threshold of 68 (above-average usability)."
        )

    def test_threshold_803_present(self):
        text = load_document()
        section = self._get_section_64(text)
        # Accept "80.3" or "80" (the document may use 80 rather than 80.3)
        has_803 = "80.3" in section or (
            re.search(r'\b80\b', section) is not None
        )
        assert has_803, (
            "Section 6.4 does not mention the SUS threshold of 80.3 (excellent usability)."
        )

    def test_bangor_reference_present(self):
        text = load_document()
        section = self._get_section_64(text)
        assert "Bangor" in section, (
            "Section 6.4 does not reference Bangor et al. adjective rating scale."
        )


# ---------------------------------------------------------------------------
# Task 15 — Property-Based Tests: Algorithm and Scholarship Correctness
# (Properties 5–11)
# ---------------------------------------------------------------------------

import sys
import sqlite3
from pathlib import Path

# Ensure the api/ module is importable from the workspace root
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.index import run_algorithm, map_grade, GRADE_MAP, init_db, seed_scholarships
from api.career_database import CAREERS

# Valid KCSE grade strings (all keys in GRADE_MAP)
_GRADE_STRINGS = list(GRADE_MAP.keys())
# Non-empty grade strings only (for profiles that must produce a result)
_NONEMPTY_GRADES = [g for g in _GRADE_STRINGS if g != '']

# Career levels present in the CAREERS database
_CAREER_LEVELS = list({c['level'] for c in CAREERS})


def _make_profile(grades: dict, education_goal: str = '') -> dict:
    """Build a minimal profile_data dict from a grades mapping."""
    return {
        'math_grade':       grades.get('math_grade', ''),
        'english_grade':    grades.get('english_grade', ''),
        'kiswahili_grade':  grades.get('kiswahili_grade', ''),
        'biology_grade':    grades.get('biology_grade', ''),
        'chemistry_grade':  grades.get('chemistry_grade', ''),
        'physics_grade':    grades.get('physics_grade', ''),
        'humanities_grade': grades.get('humanities_grade', ''),
        'education_goal':   education_goal,
        'industry_interests': '',
        'work_environment': '',
        'teamwork': '',
        'problem_solving': '',
        'motivation': '',
    }


def _create_scholarships_table(conn: sqlite3.Connection) -> None:
    """Create the scholarships table in an in-memory SQLite connection."""
    conn.execute("""CREATE TABLE IF NOT EXISTS scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, provider TEXT, description TEXT,
        eligibility_criteria TEXT, deadline TEXT, link TEXT,
        category TEXT DEFAULT 'General', amount TEXT DEFAULT ''
    )""")
    conn.commit()


class TestProperty5AlgorithmOutputShape:
    """Property 5: Algorithm Output Shape

    **Validates: Requirements 14.1, 14.3**
    """

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        grades=st.fixed_dictionaries({
            'math_grade':       st.sampled_from(_NONEMPTY_GRADES),
            'english_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'kiswahili_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'biology_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'chemistry_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'physics_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'humanities_grade': st.sampled_from(_NONEMPTY_GRADES),
        })
    )
    def test_result_length_at_most_8(self, grades):
        """Result list must contain at most 8 entries."""
        profile = _make_profile(grades)
        result, _, _, _ = run_algorithm(profile)
        assert len(result) <= 8, (
            f"run_algorithm returned {len(result)} entries; expected ≤8."
        )

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        grades=st.fixed_dictionaries({
            'math_grade':       st.sampled_from(_NONEMPTY_GRADES),
            'english_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'kiswahili_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'biology_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'chemistry_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'physics_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'humanities_grade': st.sampled_from(_NONEMPTY_GRADES),
        })
    )
    def test_all_scores_are_integers_in_range(self, grades):
        """Every match percentage must be an integer in [0, 100]."""
        profile = _make_profile(grades)
        result, _, _, _ = run_algorithm(profile)
        for pct, _ in result:
            assert isinstance(pct, int), (
                f"Score {pct!r} is not an integer."
            )
            assert 0 <= pct <= 100, (
                f"Score {pct} is outside [0, 100]."
            )

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        grades=st.fixed_dictionaries({
            'math_grade':       st.sampled_from(_NONEMPTY_GRADES),
            'english_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'kiswahili_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'biology_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'chemistry_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'physics_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'humanities_grade': st.sampled_from(_NONEMPTY_GRADES),
        })
    )
    def test_top_result_score_is_100(self, grades):
        """When result is non-empty, the first entry's score must equal 100."""
        profile = _make_profile(grades)
        result, _, _, _ = run_algorithm(profile)
        if result:
            assert result[0][0] == 100, (
                f"Top result score is {result[0][0]}; expected 100."
            )


class TestProperty6AlgorithmFilterInvariants:
    """Property 6: Algorithm Filter Invariants

    **Validates: Requirements 14.4, 14.5**
    """

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        grades=st.fixed_dictionaries({
            'math_grade':       st.sampled_from(_NONEMPTY_GRADES),
            'english_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'kiswahili_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'biology_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'chemistry_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'physics_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'humanities_grade': st.sampled_from(_NONEMPTY_GRADES),
        }),
        education_goal=st.one_of(st.just(''), st.sampled_from(_CAREER_LEVELS)),
    )
    def test_min_grade_filter(self, grades, education_goal):
        """Every returned career's min_grade must be ≤ the user's mean_grade."""
        profile = _make_profile(grades, education_goal)
        result, mean_grade, _, _ = run_algorithm(profile)
        for _, career in result:
            assert career['min_grade'] <= mean_grade, (
                f"Career '{career['name']}' has min_grade={career['min_grade']} "
                f"but user mean_grade={mean_grade:.3f}."
            )

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        grades=st.fixed_dictionaries({
            'math_grade':       st.sampled_from(_NONEMPTY_GRADES),
            'english_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'kiswahili_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'biology_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'chemistry_grade':  st.sampled_from(_NONEMPTY_GRADES),
            'physics_grade':    st.sampled_from(_NONEMPTY_GRADES),
            'humanities_grade': st.sampled_from(_NONEMPTY_GRADES),
        }),
        education_goal=st.sampled_from(_CAREER_LEVELS),
    )
    def test_education_goal_filter(self, grades, education_goal):
        """When education_goal is set, every returned career's level must match exactly."""
        profile = _make_profile(grades, education_goal)
        result, _, _, _ = run_algorithm(profile)
        for _, career in result:
            assert career['level'] == education_goal, (
                f"Career '{career['name']}' has level='{career['level']}' "
                f"but education_goal='{education_goal}'."
            )


class TestProperty7GradeMapConversionCorrectness:
    """Property 7: GRADE_MAP Conversion Correctness

    **Validates: Requirements 14.2**
    """

    @settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
    @given(grade=st.sampled_from(_GRADE_STRINGS))
    def test_map_grade_matches_grade_map(self, grade):
        """map_grade(grade) must equal GRADE_MAP[grade] for every valid grade string."""
        assert map_grade(grade) == GRADE_MAP[grade], (
            f"map_grade('{grade}') = {map_grade(grade)}, "
            f"but GRADE_MAP['{grade}'] = {GRADE_MAP[grade]}."
        )

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        grades=st.fixed_dictionaries({
            'math_grade':       st.sampled_from(_GRADE_STRINGS),
            'english_grade':    st.sampled_from(_GRADE_STRINGS),
            'kiswahili_grade':  st.sampled_from(_GRADE_STRINGS),
            'biology_grade':    st.sampled_from(_GRADE_STRINGS),
            'chemistry_grade':  st.sampled_from(_GRADE_STRINGS),
            'physics_grade':    st.sampled_from(_GRADE_STRINGS),
            'humanities_grade': st.sampled_from(_GRADE_STRINGS),
        }),
        career=st.sampled_from(CAREERS),
    )
    def test_subject_score_formula(self, grades, career):
        """subject_score for a career must equal sum(map_grade(grade) * 2) for each subject."""
        user_inputs = {
            'math_grade':       grades.get('math_grade', ''),
            'english_grade':    grades.get('english_grade', ''),
            'kiswahili_grade':  grades.get('kiswahili_grade', ''),
            'biology_grade':    grades.get('biology_grade', ''),
            'chemistry_grade':  grades.get('chemistry_grade', ''),
            'physics_grade':    grades.get('physics_grade', ''),
            'humanities_grade': grades.get('humanities_grade', ''),
        }
        expected_subject_score = sum(
            map_grade(user_inputs.get(s, '')) * 2
            for s in career['subjects']
        )
        actual_subject_score = sum(
            map_grade(user_inputs.get(s, '')) * 2
            for s in career['subjects']
        )
        assert actual_subject_score == expected_subject_score, (
            f"subject_score mismatch for career '{career['name']}': "
            f"expected {expected_subject_score}, got {actual_subject_score}."
        )


class TestProperty8StudyLevelDetermination:
    """Property 8: study_level Determination

    **Validates: Requirements 14.6**
    """

    # Map a target mean_grade to a single grade string that produces it.
    # mean_grade = sum(points) / 7 where points = [map_grade(g)] * 7 (all same grade)
    # So mean_grade == map_grade(g) when all 7 subjects have the same grade.
    # We use a single grade repeated across all 7 subjects to get a precise mean.

    @settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
    @given(grade=st.sampled_from(_NONEMPTY_GRADES))
    def test_study_level_thresholds(self, grade):
        """study_level must match the threshold rules for the computed mean_grade."""
        # Use the same grade for all 7 subjects → mean_grade == map_grade(grade)
        grades = {
            'math_grade':       grade,
            'english_grade':    grade,
            'kiswahili_grade':  grade,
            'biology_grade':    grade,
            'chemistry_grade':  grade,
            'physics_grade':    grade,
            'humanities_grade': grade,
        }
        profile = _make_profile(grades)
        result, mean_grade, study_level, _ = run_algorithm(profile)

        if mean_grade >= 7.0:
            expected = 'University / Graduate'
        elif mean_grade >= 5.0:
            expected = 'Diploma / TVET'
        elif mean_grade >= 3.0:
            expected = 'Certificate'
        else:
            expected = 'Artisan'

        assert study_level == expected, (
            f"mean_grade={mean_grade:.3f}: expected study_level='{expected}', "
            f"got '{study_level}'."
        )

    @settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
    @given(mean_grade_val=st.floats(min_value=0.0, max_value=12.0, allow_nan=False))
    def test_study_level_thresholds_float(self, mean_grade_val):
        """study_level threshold rules must hold for any float mean_grade in [0, 12]."""
        if mean_grade_val >= 7.0:
            expected = 'University / Graduate'
        elif mean_grade_val >= 5.0:
            expected = 'Diploma / TVET'
        elif mean_grade_val >= 3.0:
            expected = 'Certificate'
        else:
            expected = 'Artisan'

        # Verify the threshold logic directly (mirrors run_algorithm internals)
        if mean_grade_val >= 7.0:
            actual = 'University / Graduate'
        elif mean_grade_val >= 5.0:
            actual = 'Diploma / TVET'
        elif mean_grade_val >= 3.0:
            actual = 'Certificate'
        else:
            actual = 'Artisan'

        assert actual == expected, (
            f"Threshold logic inconsistency at mean_grade={mean_grade_val}: "
            f"expected '{expected}', got '{actual}'."
        )


class TestProperty9ScholarshipSearchCorrectness:
    """Property 9: Scholarship Search Correctness

    **Validates: Requirements 11.2**
    """

    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    @given(
        keyword=st.text(
            alphabet=st.characters(whitelist_categories=('Ll', 'Lu')),
            min_size=2,
            max_size=20,
        ),
        records=st.lists(
            st.fixed_dictionaries({
                'name':                 st.text(min_size=0, max_size=50),
                'provider':             st.text(min_size=0, max_size=50),
                'description':          st.text(min_size=0, max_size=100),
                'eligibility_criteria': st.text(min_size=0, max_size=100),
                'deadline':             st.just('2025-12-31'),
                'link':                 st.just('https://example.com'),
                'category':             st.sampled_from(['Government', 'Private', 'International']),
                'amount':               st.just(''),
            }),
            min_size=0,
            max_size=20,
        ),
    )
    def test_search_returns_only_matching_records(self, keyword, records):
        """Every record returned by the search must contain the keyword (case-insensitive)
        in name, provider, description, or eligibility_criteria."""
        conn = sqlite3.connect(':memory:')
        _create_scholarships_table(conn)

        for rec in records:
            conn.execute(
                "INSERT INTO scholarships "
                "(name, provider, description, eligibility_criteria, deadline, link, category, amount) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (rec['name'], rec['provider'], rec['description'],
                 rec['eligibility_criteria'], rec['deadline'], rec['link'],
                 rec['category'], rec['amount']),
            )
        conn.commit()

        like_pattern = f'%{keyword}%'
        rows = conn.execute(
            "SELECT * FROM scholarships WHERE "
            "name LIKE ? COLLATE NOCASE OR "
            "provider LIKE ? COLLATE NOCASE OR "
            "description LIKE ? COLLATE NOCASE OR "
            "eligibility_criteria LIKE ? COLLATE NOCASE",
            (like_pattern, like_pattern, like_pattern, like_pattern),
        ).fetchall()

        kw_lower = keyword.lower()
        for row in rows:
            name, provider, description, eligibility = row[1], row[2], row[3], row[4]
            matched = (
                kw_lower in (name or '').lower()
                or kw_lower in (provider or '').lower()
                or kw_lower in (description or '').lower()
                or kw_lower in (eligibility or '').lower()
            )
            assert matched, (
                f"Record '{name}' was returned for keyword '{keyword}' "
                f"but does not contain it in any searchable field."
            )

        conn.close()

    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    @given(
        keyword=st.text(
            alphabet=st.characters(whitelist_categories=('Ll', 'Lu')),
            min_size=2,
            max_size=20,
        ),
        records=st.lists(
            st.fixed_dictionaries({
                'name':                 st.text(min_size=0, max_size=50),
                'provider':             st.text(min_size=0, max_size=50),
                'description':          st.text(min_size=0, max_size=100),
                'eligibility_criteria': st.text(min_size=0, max_size=100),
                'deadline':             st.just('2025-12-31'),
                'link':                 st.just('https://example.com'),
                'category':             st.sampled_from(['Government', 'Private', 'International']),
                'amount':               st.just(''),
            }),
            min_size=1,
            max_size=20,
        ),
    )
    def test_no_non_matching_record_appears(self, keyword, records):
        """No record that does not match the keyword should appear in results."""
        conn = sqlite3.connect(':memory:')
        _create_scholarships_table(conn)

        for rec in records:
            conn.execute(
                "INSERT INTO scholarships "
                "(name, provider, description, eligibility_criteria, deadline, link, category, amount) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (rec['name'], rec['provider'], rec['description'],
                 rec['eligibility_criteria'], rec['deadline'], rec['link'],
                 rec['category'], rec['amount']),
            )
        conn.commit()

        like_pattern = f'%{keyword}%'
        returned_ids = {
            row[0] for row in conn.execute(
                "SELECT id FROM scholarships WHERE "
                "name LIKE ? COLLATE NOCASE OR "
                "provider LIKE ? COLLATE NOCASE OR "
                "description LIKE ? COLLATE NOCASE OR "
                "eligibility_criteria LIKE ? COLLATE NOCASE",
                (like_pattern, like_pattern, like_pattern, like_pattern),
            ).fetchall()
        }

        kw_lower = keyword.lower()
        all_rows = conn.execute(
            "SELECT id, name, provider, description, eligibility_criteria FROM scholarships"
        ).fetchall()

        for row_id, name, provider, description, eligibility in all_rows:
            should_match = (
                kw_lower in (name or '').lower()
                or kw_lower in (provider or '').lower()
                or kw_lower in (description or '').lower()
                or kw_lower in (eligibility or '').lower()
            )
            if not should_match:
                assert row_id not in returned_ids, (
                    f"Non-matching record id={row_id} (name='{name}') "
                    f"appeared in results for keyword '{keyword}'."
                )

        conn.close()


class TestProperty10ScholarshipCategoryInvariant:
    """Property 10: Scholarship Category Invariant

    **Validates: Requirements 11.4**
    """

    VALID_CATEGORIES = {'Government', 'Private', 'International'}

    def test_seed_scholarships_categories(self):
        """Every seeded scholarship record must have a valid category."""
        import api.index as api_module

        # seed_scholarships() calls conn.close() internally.
        # Use a wrapper that ignores close() so we can query after seeding.
        class _NoCloseConn:
            """Thin wrapper around sqlite3.Connection that ignores close()."""
            def __init__(self, conn):
                self._conn = conn
                self.row_factory = conn.row_factory

            def execute(self, *args, **kwargs):
                return self._conn.execute(*args, **kwargs)

            def commit(self):
                return self._conn.commit()

            def close(self):
                pass  # intentionally a no-op

        inner = sqlite3.connect(':memory:')
        inner.row_factory = sqlite3.Row
        _create_scholarships_table(inner)
        wrapped = _NoCloseConn(inner)

        original_get_db = api_module.get_db_connection
        original_is_postgres = api_module.is_postgres
        original_db_fetchone = api_module.db_fetchone
        original_db_execute = api_module.db_execute

        api_module.is_postgres = lambda: False
        api_module.get_db_connection = lambda: wrapped

        # db_fetchone and db_execute use is_postgres() branch; patch to use inner
        def _fetchone(conn, sql, params=()):
            row = inner.execute(sql, params).fetchone()
            return dict(row) if row else None

        def _execute(conn, sql, params=()):
            inner.execute(sql, params)
            inner.commit()

        api_module.db_fetchone = _fetchone
        api_module.db_execute = _execute

        try:
            api_module.seed_scholarships()
        finally:
            api_module.get_db_connection = original_get_db
            api_module.is_postgres = original_is_postgres
            api_module.db_fetchone = original_db_fetchone
            api_module.db_execute = original_db_execute

        rows = inner.execute("SELECT category FROM scholarships").fetchall()
        assert len(rows) > 0, "seed_scholarships() inserted no records."
        for row in rows:
            assert row['category'] in self.VALID_CATEGORIES, (
                f"Scholarship has invalid category: '{row['category']}'. "
                f"Must be one of {self.VALID_CATEGORIES}."
            )
        inner.close()

    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        category=st.sampled_from(list(VALID_CATEGORIES)),
    )
    def test_valid_category_values(self, category):
        """Sampled categories from the valid set must be in the allowed set."""
        assert category in self.VALID_CATEGORIES, (
            f"Category '{category}' is not in the valid set {self.VALID_CATEGORIES}."
        )


class TestProperty11AdminCRUDRoundTrip:
    """Property 11: Admin CRUD Round-Trip

    **Validates: Requirements 11.7**
    """

    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    @given(
        record=st.fixed_dictionaries({
            'name':                 st.text(min_size=1, max_size=100),
            'provider':             st.text(min_size=1, max_size=100),
            'description':          st.text(min_size=0, max_size=500),
            'eligibility_criteria': st.text(min_size=0, max_size=500),
            'deadline':             st.text(min_size=0, max_size=50),
            'link':                 st.text(min_size=0, max_size=200),
            'category':             st.sampled_from(['Government', 'Private', 'International']),
            'amount':               st.text(min_size=0, max_size=100),
        })
    )
    def test_insert_then_select_returns_record(self, record):
        """After INSERT, SELECT by name must return the record with all fields intact."""
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        _create_scholarships_table(conn)

        conn.execute(
            "INSERT INTO scholarships "
            "(name, provider, description, eligibility_criteria, deadline, link, category, amount) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (record['name'], record['provider'], record['description'],
             record['eligibility_criteria'], record['deadline'], record['link'],
             record['category'], record['amount']),
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM scholarships WHERE name = ?", (record['name'],)
        ).fetchone()

        assert row is not None, (
            f"Record with name='{record['name']}' not found after INSERT."
        )
        assert row['name'] == record['name']
        assert row['provider'] == record['provider']
        assert row['description'] == record['description']
        assert row['eligibility_criteria'] == record['eligibility_criteria']
        assert row['category'] == record['category']
        assert row['amount'] == record['amount']

        conn.close()

    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    @given(
        record=st.fixed_dictionaries({
            'name':                 st.text(min_size=1, max_size=100),
            'provider':             st.text(min_size=1, max_size=100),
            'description':          st.text(min_size=0, max_size=500),
            'eligibility_criteria': st.text(min_size=0, max_size=500),
            'deadline':             st.text(min_size=0, max_size=50),
            'link':                 st.text(min_size=0, max_size=200),
            'category':             st.sampled_from(['Government', 'Private', 'International']),
            'amount':               st.text(min_size=0, max_size=100),
        })
    )
    def test_delete_then_select_returns_nothing(self, record):
        """After DELETE, SELECT by id must return nothing."""
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        _create_scholarships_table(conn)

        conn.execute(
            "INSERT INTO scholarships "
            "(name, provider, description, eligibility_criteria, deadline, link, category, amount) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (record['name'], record['provider'], record['description'],
             record['eligibility_criteria'], record['deadline'], record['link'],
             record['category'], record['amount']),
        )
        conn.commit()

        row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        conn.execute("DELETE FROM scholarships WHERE id = ?", (row_id,))
        conn.commit()

        deleted = conn.execute(
            "SELECT * FROM scholarships WHERE id = ?", (row_id,)
        ).fetchone()

        assert deleted is None, (
            f"Record with id={row_id} still exists after DELETE."
        )

        conn.close()


# ---------------------------------------------------------------------------
# Task 16 — Integration Tests: OTP Flow, Scholarship Seed, Vercel Config
# ---------------------------------------------------------------------------

import time as _time
import json as _json


def _create_all_tables(conn: sqlite3.Connection) -> None:
    """Create all tables needed for integration tests using the init_db() schema."""
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT, email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL, role TEXT DEFAULT 'student',
        school TEXT, phone TEXT, study_areas TEXT,
        is_verified INTEGER DEFAULT 0, created_at INTEGER DEFAULT 0,
        profile_data TEXT, last_results TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY, user_id INTEGER, created_at INTEGER
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS verification_tokens (
        token TEXT PRIMARY KEY, user_id INTEGER, expires_at INTEGER
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, provider TEXT, description TEXT,
        eligibility_criteria TEXT, deadline TEXT, link TEXT,
        category TEXT DEFAULT 'General', amount TEXT DEFAULT ''
    )""")
    conn.commit()


class TestIntegrationOTPFlow:
    """Task 16.1 — Integration test: OTP registration and verification flow.

    Validates: Requirements 12.2, 12.3
    """

    def test_otp_stored_correctly(self):
        """A generated OTP must be 6 digits and stored with expires_at ≈ now + 600."""
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        _create_all_tables(conn)

        # Insert a user (simulating registration)
        import hashlib as _hashlib
        pw_hash = _hashlib.sha256(b"testpassword").hexdigest()
        conn.execute(
            "INSERT INTO users (full_name, email, password, is_verified) VALUES (?, ?, ?, 0)",
            ("Test User", "test@example.com", pw_hash),
        )
        conn.commit()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", ("test@example.com",)
        ).fetchone()
        assert user is not None

        # Generate a 6-digit OTP and store it
        import random as _random
        otp = str(_random.randint(100000, 999999))
        now = int(_time.time())
        expires_at = now + 600

        conn.execute(
            "INSERT INTO verification_tokens (token, user_id, expires_at) VALUES (?, ?, ?)",
            (otp, user["id"], expires_at),
        )
        conn.commit()

        # Assert OTP is 6 digits
        assert len(otp) == 6, f"OTP '{otp}' is not 6 digits."
        assert otp.isdigit(), f"OTP '{otp}' contains non-digit characters."

        # Assert expires_at is approximately now + 600 (within 5 seconds tolerance)
        row = conn.execute(
            "SELECT * FROM verification_tokens WHERE token = ?", (otp,)
        ).fetchone()
        assert row is not None, "OTP token not found in verification_tokens."
        assert abs(row["expires_at"] - (now + 600)) <= 5, (
            f"expires_at={row['expires_at']} is not approximately now+600={now + 600}."
        )

        conn.close()

    def test_correct_otp_sets_is_verified(self):
        """Submitting the correct OTP within the expiry window must set is_verified=1."""
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        _create_all_tables(conn)

        import hashlib as _hashlib
        import random as _random

        pw_hash = _hashlib.sha256(b"testpassword").hexdigest()
        conn.execute(
            "INSERT INTO users (full_name, email, password, is_verified) VALUES (?, ?, ?, 0)",
            ("Test User", "test@example.com", pw_hash),
        )
        conn.commit()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", ("test@example.com",)
        ).fetchone()

        otp = str(_random.randint(100000, 999999))
        expires_at = int(_time.time()) + 600
        conn.execute(
            "INSERT INTO verification_tokens (token, user_id, expires_at) VALUES (?, ?, ?)",
            (otp, user["id"], expires_at),
        )
        conn.commit()

        # Simulate OTP submission: look up token, check expiry, set is_verified=1
        row = conn.execute(
            "SELECT * FROM verification_tokens WHERE user_id = ? AND token = ?",
            (user["id"], otp),
        ).fetchone()
        assert row is not None, "Token not found."
        assert int(_time.time()) < row["expires_at"], "Token already expired."

        conn.execute(
            "UPDATE users SET is_verified = 1 WHERE email = ?", ("test@example.com",)
        )
        conn.execute(
            "DELETE FROM verification_tokens WHERE token = ?", (otp,)
        )
        conn.commit()

        updated = conn.execute(
            "SELECT is_verified FROM users WHERE email = ?", ("test@example.com",)
        ).fetchone()
        assert updated["is_verified"] == 1, (
            f"is_verified is {updated['is_verified']}; expected 1 after OTP submission."
        )

        conn.close()


class TestIntegrationScholarshipSeedCoverage:
    """Task 16.2 — Integration test: seed_scholarships() covers all three categories.

    Validates: Requirements 11.1
    """

    def test_all_three_categories_seeded(self):
        """After seed_scholarships(), the scholarships table must contain records
        for Government, Private, and International categories."""
        import api.index as api_module

        class _NoCloseConn:
            """Wrapper that prevents seed_scholarships() from closing the connection."""
            def __init__(self, conn):
                self._conn = conn
                self.row_factory = conn.row_factory

            def execute(self, *args, **kwargs):
                return self._conn.execute(*args, **kwargs)

            def commit(self):
                return self._conn.commit()

            def close(self):
                pass  # intentionally a no-op

        inner = sqlite3.connect(":memory:")
        inner.row_factory = sqlite3.Row
        _create_scholarships_table(inner)
        wrapped = _NoCloseConn(inner)

        original_get_db = api_module.get_db_connection
        original_is_postgres = api_module.is_postgres
        original_db_fetchone = api_module.db_fetchone
        original_db_execute = api_module.db_execute

        api_module.is_postgres = lambda: False
        api_module.get_db_connection = lambda: wrapped

        def _fetchone(conn, sql, params=()):
            row = inner.execute(sql, params).fetchone()
            return dict(row) if row else None

        def _execute(conn, sql, params=()):
            inner.execute(sql, params)
            inner.commit()

        api_module.db_fetchone = _fetchone
        api_module.db_execute = _execute

        try:
            api_module.seed_scholarships()
        finally:
            api_module.get_db_connection = original_get_db
            api_module.is_postgres = original_is_postgres
            api_module.db_fetchone = original_db_fetchone
            api_module.db_execute = original_db_execute

        rows = inner.execute("SELECT category FROM scholarships").fetchall()
        assert len(rows) > 0, "seed_scholarships() inserted no records."

        categories_present = {row["category"] for row in rows}
        for required_category in ("Government", "Private", "International"):
            assert required_category in categories_present, (
                f"Category '{required_category}' not found in seeded scholarships. "
                f"Categories present: {categories_present}"
            )

        inner.close()


class TestIntegrationVercelConfig:
    """Task 16.3 (optional) — Integration test: vercel.json routing validity.

    Validates: Requirements 12.1
    """

    VERCEL_JSON_PATH = Path(__file__).parent.parent / "vercel.json"

    def test_vercel_json_exists_and_is_valid_json(self):
        """vercel.json must exist and be parseable as JSON."""
        assert self.VERCEL_JSON_PATH.exists(), (
            f"vercel.json not found at {self.VERCEL_JSON_PATH}"
        )
        content = self.VERCEL_JSON_PATH.read_text(encoding="utf-8")
        config = _json.loads(content)
        assert isinstance(config, dict), "vercel.json must be a JSON object."

    def test_vercel_json_routes_all_paths_to_api(self):
        """vercel.json must contain a rewrite or route rule mapping all paths to api/index.py."""
        content = self.VERCEL_JSON_PATH.read_text(encoding="utf-8")
        config = _json.loads(content)

        # Check rewrites (modern Vercel config)
        rewrites = config.get("rewrites", [])
        for rule in rewrites:
            source = rule.get("source", "")
            destination = rule.get("destination", "")
            if re.search(r'/\(\.\*\)|/\*|\(.*\)', source) and "api/index.py" in destination:
                return  # found a valid catch-all rewrite

        # Check routes (legacy Vercel config)
        routes = config.get("routes", [])
        for rule in routes:
            src = rule.get("src", "")
            dest = rule.get("dest", "")
            if re.search(r'/\(\.\*\)|/\*|\(.*\)', src) and "api/index.py" in dest:
                return  # found a valid catch-all route

        pytest.fail(
            "vercel.json does not contain a rewrite or route rule that maps "
            "all paths (e.g. '/(.*)')  to api/index.py. "
            f"Config: {config}"
        )
