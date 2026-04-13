# Implementation Plan: Research Documentation Expansion

## Overview

Generate the complete 150+ page academic project document by executing a sequential, section-by-section content pass through all preliminary pages, Chapters 1–6, References, and Appendices. Each task produces a concrete file or appends a well-defined section to the master output file `Documents/expanded_research_document.md`. Property-based tests (hypothesis) and validation scripts are included as optional sub-tasks to verify structural correctness at each milestone.

---

## Tasks

- [x] 1. Set up document generation environment and output file
  - Create `Documents/expanded_research_document.md` as the single master output file with a top-level heading and a generation metadata comment block
  - Create `scripts/` directory with `validate_document.py` — a utility module exposing `word_count(text)`, `count_mermaid_blocks(text)`, `find_forbidden_terms(text)`, and `find_apa_citations(text)` helper functions used by all later validation and test tasks
  - Create `scripts/requirements_test.txt` listing `pytest` and `hypothesis` as test dependencies
  - Verify the project's `requirements.txt` does not already include these; add them if absent
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 10.1_

- [x] 2. Generate all preliminary pages
  - [x] 2.1 Write Cover Page, Blank Page, and Declaration & Approval page
    - Append to `expanded_research_document.md`: Cover Page (title, student name IGNATIUS ETHENS CIT-221-048/2022, supervisor DR. ISHMAEL NICK, Faculty of Computing and Information Technology, year), a blank page marker, and the Declaration & Approval page with three signature blocks (Student, University Supervisor, Head of Department)
    - _Requirements: 1.5, 9.6_

  - [x] 2.2 Write Dedication and Acknowledgements
    - Append Dedication (~0.5 page) and Acknowledgements (~0.5 page) consistent with the existing document's tone
    - _Requirements: 1.6_

  - [x] 2.3 Write Abstract
    - Append the Abstract (150–300 words, wrapped in blockquote to signal single-spaced italic formatting) covering: research title, problem and objectives, mixed-methods + Agile Scrum methodology, Pure Python / Vanilla HTML5/CSS3/JS / SQLite/PostgreSQL tech stack, key results, and conclusion
    - _Requirements: 1.1_

  - [ ]* 2.4 Write unit test: Abstract word count
    - In `scripts/test_document.py`, write a pytest test that loads `expanded_research_document.md`, extracts the Abstract section, and asserts `150 <= word_count(abstract_text) <= 300`
    - _Requirements: 1.1_

  - [x] 2.5 Write Table of Contents, List of Figures, and List of Tables
    - Append a Table of Contents listing all chapters, sections, and sub-sections with `[p. X]` placeholders; a List of Figures referencing all Figure X.Y captions; and a List of Tables referencing all Table X.Y captions
    - _Requirements: 1.2, 1.3_

  - [x] 2.6 Write Definition of Key Terms
    - Append the Definition of Key Terms section with ≥13 terms: CBC, KUCCPS, Form Four Leavers, Career Guidance, Scholarship Portal, NEET, TVET, HELB/HEFoND, Educational Pathways, RIASEC, TAM, SCCT, MTI
    - _Requirements: 1.4_

  - [ ]* 2.7 Write unit test: Declaration page content
    - In `scripts/test_document.py`, assert that the Declaration section contains the exact strings `IGNATIUS ETHENS CIT-221-048/2022` and `DR. ISHMAEL NICK`
    - _Requirements: 1.5_

- [x] 3. Generate Chapter 1 — Introduction
  - [x] 3.1 Write Sections 1.1 and 1.2
    - Append Section 1.1 (Chapter Introduction, ≥1 page, listing all sub-sections) and Section 1.2 (Motivation and Background, ≥1.5 pages, first-person narrative covering personal and societal motivations)
    - _Requirements: 2.1, 2.2_

  - [x] 3.2 Write Section 1.3 — Background of the Study
    - Append Section 1.3 (≥3 pages) covering: global education-to-employment context, Kenya's 7-4-2-3 system, 8-4-4 system and its limitations, CBC paradigm shift, HELB/HEFoND/MTI/NG-CDF financing landscape, and information asymmetry problem; include APA citations in every paragraph
    - _Requirements: 2.3, 9.10_

  - [x] 3.3 Write Section 1.4 — Problem Statement
    - Append Section 1.4 (≥1 page) in continuous prose (no bullet points), addressing the five Ws, with ≥2 APA citations
    - _Requirements: 2.4, 9.7_

  - [x] 3.4 Write Sections 1.5 and 1.6 — Aim and Objectives
    - Append Section 1.5 (single broad action-verb statement, ≤1 paragraph) and Section 1.6 (one main objective restating the research title + 3–4 SMART specific objectives as functional system specifications, avoiding "user-friendly" or "efficient")
    - _Requirements: 2.5, 2.6_

  - [ ]* 3.5 Write unit test: Objectives format
    - In `scripts/test_document.py`, extract Section 1.6 and assert it contains exactly one main objective and between 3 and 4 specific objectives (by counting numbered objective lines)
    - _Requirements: 2.6_

  - [x] 3.6 Write Sections 1.7, 1.8, 1.9, and 1.10
    - Append Section 1.7 (Justification, ≥1.5 pages, anchored on published research covering policy alignment, equity, economic optimisation, tech advancement), Section 1.8 (Scope, specifying target org, features, and explicit limitations), Section 1.9 (Research Organisation, one paragraph per chapter for all 7 chapters), and Section 1.10 (Chapter Summary)
    - _Requirements: 2.7, 2.8, 2.9, 2.10, 9.8, 9.9_

- [x] 4. Generate Chapter 2 — Literature Review
  - [x] 4.1 Write Sections 2.1 and 2.2
    - Append Section 2.1 (Chapter Introduction, listing all sub-sections) and Section 2.2 (Theoretical Framework, ≥3 pages) covering: Holland's RIASEC Model (1997) with explicit CBC pathway mapping, SCCT (Lent et al., 1994) with Kenyan socio-economic context, and TAM (Davis, 1989) with mobile-first/low-bandwidth application; APA citation in every paragraph
    - _Requirements: 3.1, 3.2, 3.9_

  - [x] 4.2 Write Sections 2.3 and 2.4
    - Append Section 2.3 (History of the Research Topic, ≥3 pages) tracing post-independence 7-4-2-3 → 8-4-4 → CBC chronology, and Section 2.4 (Scholarship & Financing Landscape, ≥1.5 pages) covering HEF model, MTI bands, HELB/HEFoND, Equity Wings to Fly, KCB Foundation, NG-CDF
    - _Requirements: 3.3, 3.4, 3.9_

  - [x] 4.3 Write Section 2.5 — Review of Related Systems
    - Append Section 2.5 (≥2 pages) reviewing Naviance (global), KUCCPS Portal (local government), and Craydel (local commercial), each with Core Features / Strengths / Limitations sub-sections; include Table 2.1 (comparative analysis table, caption above) with Markdown pipe syntax
    - _Requirements: 3.5_

  - [ ]* 4.4 Write unit test: Table 2.1 existence
    - In `scripts/test_document.py`, assert the document contains a table row with all three system names: Naviance, KUCCPS Portal, and Craydel
    - _Requirements: 3.5_

  - [x] 4.5 Write Sections 2.6, 2.7, and 2.8
    - Append Section 2.6 (Emerging Trends, ≥2 pages: AI/ML in EdTech, one-stop-shop integration, PWA/mobile-first in Sub-Saharan Africa, data privacy), Section 2.7 (Research Gap, ≥1.5 pages: Contextual Gap, Integration Gap, Accessibility Gap), and Section 2.8 (Chapter Summary bridging to Chapter Three)
    - _Requirements: 3.6, 3.7, 3.8, 3.9_

- [x] 5. Checkpoint — Verify Chapters 1–2 quality
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Generate Chapter 3 — Research Methodology
  - [x] 6.1 Write Sections 3.1, 3.2, and 3.3
    - Append Section 3.1 (Chapter Introduction), Section 3.2 (Methodology for Literature Review, ≥1.5 pages: mixed-methods rationale, 6 generic steps, databases and search terms), and Section 3.3 (Methodology for Requirement Specification, ≥3 pages: mixed-methods design, target population, stratified random sampling, purposive sampling, KII, digital questionnaires, document analysis)
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 6.2 Write Sections 3.4 and 3.5
    - Append Section 3.4 (Methodology for System Analysis — Current System, ≥1.5 pages: System Analysis definition, Context Diagram description, DFD description, Flowchart description) and Section 3.5 (Methodology for System Design — Proposed System, ≥4 pages: DFDs, Flowcharts, 4 Sequence Diagrams, Collaboration Diagrams, Use Case Diagrams, Pseudocode for `run_algorithm()`, I/O design, UI principles, ERD, normalisation, data dictionary)
    - _Requirements: 4.4, 4.5_

  - [x] 6.3 Write Sections 3.6, 3.7, 3.8, and 3.9
    - Append Section 3.6 (Methodology for System Implementation, ≥2 pages: Agile Scrum + Sprint structure, Pure Python `http.server` / `sqlite3` / `hashlib` / `uuid` / `smtplib` / `json`, Vanilla HTML5/CSS3/JS ES6+, SQLite dev + PostgreSQL/Neon prod, `pg8000`), Section 3.7 (Methodology for System Testing, ≥1.5 pages: testing plan, functional vs non-functional, unit/integration/system/UAT/SUS), Section 3.8 (Methodology for System Deployment, ≥1 page: deployment pipeline, local SQLite dev, Vercel cloud), and Section 3.9 (Chapter Summary)
    - _Requirements: 4.6, 4.7, 4.8, 4.9, 10.1, 10.2, 10.3, 10.4_

- [x] 7. Generate Chapter 4 — System Analysis of the Current System
  - [x] 7.1 Write Sections 4.1, 4.2, and 4.3
    - Append Section 4.1 (Chapter Introduction listing all sub-sections), Section 4.2 (Description of Current System, ≥2 pages: manual guidance process, strengths and weaknesses), and Section 4.3 (Feasibility Study, ≥2 pages: Technical, Economic, Operational feasibility with conclusion)
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 7.2 Write Section 4.4 — Data I/O Analysis
    - Append Section 4.4 (≥1 page) covering data captured by the current system (KCSE grades, counselor notes, printed booklets), entity relationships, and outputs (verbal advice, printed career booklets)
    - _Requirements: 5.4_

  - [x] 7.3 Write Section 4.5 — Process Logic Design with Mermaid diagrams
    - Append Section 4.5 (≥2 pages) including:
      - Figure 4.1: Context Diagram (`flowchart LR`) showing Student, Counselor, KUCCPS, Scholarship Bodies as external entities — wrapped in ` ```mermaid ` fenced block, caption below
      - Figure 4.2: Level-0 DFD (`flowchart TD`) showing data flows between Student, Counselor, and manual processes — wrapped in ` ```mermaid ` fenced block, caption below
      - Figure 4.3: Flowchart (`flowchart TD`) of the current manual guidance process — wrapped in ` ```mermaid ` fenced block, caption below
    - _Requirements: 5.5, 6.9_

  - [x] 7.4 Write Section 4.6 — Chapter Summary
    - Append Section 4.6 as a concise synthesis paragraph
    - _Requirements: 5.6_

- [x] 8. Generate Chapter 5 — System Design of the Proposed System
  - [x] 8.1 Write Sections 5.1, 5.2, and 5.3
    - Append Section 5.1 (Introduction listing all sub-sections), Section 5.2 (Description of Proposed System, ≥1.5 pages: strengths and limitations), and Section 5.3 (Requirement Analysis, ≥2 pages: Functional Requirements — registration/login, OTP, multi-step profiling, recommendation engine, scholarship repository, admin dashboard; Non-Functional Requirements — 3G page load, mobile-first, SHA-256, session management; User Requirements; Usability Requirements)
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 8.2 Write Section 5.4 — Conceptual Architecture with Mermaid diagram
    - Append Section 5.4 (≥1 page) describing the three-tier architecture (Presentation: HTML/CSS/JS; Application: Pure Python `http.server`; Data: SQLite/PostgreSQL) and include Figure 5.1 System Architecture Diagram (`flowchart TD`) in a ` ```mermaid ` fenced block with caption below
    - _Requirements: 6.4_

  - [x] 8.3 Write Section 5.5 — Process Logic Design (Use Case, Activity, Sequence Diagrams)
    - Append Section 5.5 (≥6 pages) including all nine diagrams in ` ```mermaid ` fenced blocks with captions below:
      - Figure 5.2: Use Case Diagram (`flowchart LR`) — three actors (Learner, Counselor, Admin) and all use cases
      - Figure 5.3: Activity Diagram (`flowchart TD`) — four-step profiling flow through to Recommendations
      - Figure 5.4: Sequence Diagram — User Registration with OTP (`sequenceDiagram`, participants: Browser, PortalRequestHandler, Database, Gmail SMTP)
      - Figure 5.5: Sequence Diagram — Multi-Step Career Profiling (`sequenceDiagram`, participants: Browser, PortalRequestHandler, Cookie Store, run_algorithm, Database)
      - Figure 5.6: Sequence Diagram — Scholarship Search (`sequenceDiagram`, participants: Browser, PortalRequestHandler, Database)
      - Figure 5.7: Sequence Diagram — Admin Scholarship Management (`sequenceDiagram`, participants: AdminBrowser, PortalRequestHandler, Database)
      - Figure 5.8: Class Diagram (`classDiagram`) — `handler` class extending `BaseHTTPRequestHandler` with all key methods; module-level functions
      - Figure 5.9: Context Diagram Proposed System (`flowchart LR`) — Student, Counselor, Admin, Gmail SMTP, Neon PostgreSQL, Vercel
      - Figure 5.10: Level-0 DFD Proposed System (`flowchart TD`) — all actors and main processes
    - Also append Pseudocode for `run_algorithm()` in a fenced code block
    - Also append Collaboration Diagram description (text) for the scholarship matching process
    - _Requirements: 6.5, 6.9_

  - [x] 8.4 Write Section 5.6 — Database Design with ERD and Data Dictionary
    - Append Section 5.6 (≥3 pages) including:
      - Figure 5.11: ERD (`erDiagram`) showing all four tables (users, sessions, verification_tokens, scholarships) with attributes and relationships (`users ||--o{ sessions`, `users ||--o{ verification_tokens`) — wrapped in ` ```mermaid ` fenced block, caption below
      - Normalisation discussion (1NF, 2NF, 3NF)
      - Table 5.1: Data Dictionary — users (caption above, Markdown pipe table: field, type, constraints, description)
      - Table 5.2: Data Dictionary — sessions
      - Table 5.3: Data Dictionary — verification_tokens
      - Table 5.4: Data Dictionary — scholarships
    - All field names, types, and constraints must match `api/index.py` `init_db()` exactly
    - _Requirements: 6.6, 10.6_

  - [x] 8.5 Write Sections 5.7 and 5.8
    - Append Section 5.7 (I/O Design, ≥2 pages) describing four key screens: Landing Page, Multi-Step Career Profiling Form (Steps 1–4), Recommendations Page, and Scholarships Page, each with a mock-up description and Figure caption
    - Append Section 5.8 (Chapter Summary)
    - _Requirements: 6.7, 6.8_

- [x] 9. Checkpoint — Verify Chapters 3–5 and all Mermaid diagrams
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Generate Chapter 6 — System Implementation and Testing
  - [x] 10.1 Write Section 6.1 — Chapter Introduction
    - Append Section 6.1 listing all sub-sections of Chapter Six
    - _Requirements: 7.1_

  - [x] 10.2 Write Section 6.2 — System Screenshots
    - Append Section 6.2 (≥2 pages) with descriptions of four key system screenshots, each with a Figure caption below in the format `Figure 6.X: [Description]`:
      - Figure 6.1: Home/Landing Page
      - Figure 6.2: Career Profiling Step 1 — Academic Grades
      - Figure 6.3: Recommendations Page
      - Figure 6.4: Scholarships Page
    - _Requirements: 7.2_

  - [x] 10.3 Write Section 6.3 — Testing Plan table
    - Append Section 6.3 (≥3 pages) as a Markdown pipe table (Table 6.1, caption above) with columns: Test ID, Module Under Test, Test Description, Test Input, Expected Output, Actual Output, Pass/Fail — covering ≥10 test cases: user registration, OTP verification, login valid, login invalid, profile step 1, profile step 2, profile step 3, algorithm execution (STEM profile), scholarship search, admin scholarship addition
    - _Requirements: 7.3_

  - [ ]* 10.4 Write unit test: Testing plan row count
    - In `scripts/test_document.py`, extract Table 6.1 and assert it contains ≥10 data rows (excluding the header row)
    - _Requirements: 7.3_

  - [x] 10.5 Write Section 6.4 — Evaluation Plan (SUS)
    - Append Section 6.4 (≥2 pages) covering: UAT methodology using SUS, pilot group composition (Form Four students and counselors), all 10 standard SUS questionnaire items, and discussion of expected usability scores and their interpretation
    - _Requirements: 7.4_

  - [ ]* 10.6 Write unit test: SUS items completeness
    - In `scripts/test_document.py`, assert that Section 6.4 contains all 10 standard SUS questionnaire items (verify by checking for the presence of SUS item numbers 1–10 or their canonical text)
    - _Requirements: 7.4_

  - [x] 10.7 Write Section 6.5 — Chapter Summary
    - Append Section 6.5 as a concise synthesis paragraph
    - _Requirements: 7.5_

- [x] 11. Generate Chapter 7 — Conclusions, Findings and Recommendations
  - [x] 11.1 Write Section 7.1 — Chapter Introduction
    - Append Section 7.1 listing all sub-sections of Chapter Seven
    - _Requirements: 7b.1_

  - [x] 11.2 Write Section 7.2 — Conclusion
    - Append Section 7.2 (≥2 pages) summarising the key findings of the research, confirming that the aim and all objectives stated in Chapter One have been achieved, and reflecting on the portal's significance as a contribution to educational technology in Kenya
    - _Requirements: 7b.2_

  - [x] 11.3 Write Section 7.3 — Challenges Encountered
    - Append Section 7.3 (≥1 page) documenting technical challenges (Pure Python serverless constraints, pg8000 compatibility, cookie-based state management across steps), methodological challenges (sampling, data collection), and contextual challenges (digital divide, CBC transition period), with how each was addressed
    - _Requirements: 7b.3_

  - [x] 11.4 Write Section 7.4 — Future Recommendations
    - Append Section 7.4 (≥1 page) proposing specific, actionable future enhancements: live KUCCPS API integration, Kiswahili localisation, PWA offline mode, machine learning enhancements to the recommendation engine, counselor matching feature, and a dedicated mobile app
    - _Requirements: 7b.4_

  - [x] 11.5 Write Section 7.5 — Chapter Conclusion
    - Append Section 7.5 as a formal closing paragraph for the entire research document
    - _Requirements: 7b.5_

- [x] 12. Write property-based tests (hypothesis) — Properties 1–4
  - [x] 12.1 Write Property Test 1: APA Citation Coverage
    - In `scripts/test_document.py`, implement a hypothesis property test that randomly samples paragraphs from the generated document containing theory/claim marker words ("argues", "states", "found", "according to", "research shows", "studies indicate") and asserts each sampled paragraph contains ≥1 match of the regex `\([A-Z][a-z]+(?:\s+et\s+al\.)?,\s+\d{4}\)`
    - **Property 1: APA Citation Coverage**
    - **Validates: Requirements 3.9, 8.3, 9.10**

  - [x] 12.2 Write Property Test 2: Mermaid Diagram Completeness
    - In `scripts/test_document.py`, implement a hypothesis property test that iterates over the list of 11 required diagram types and asserts the document contains a ` ```mermaid ` fenced block containing the expected Mermaid keyword (`flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`) for each
    - **Property 2: Mermaid Diagram Completeness**
    - **Validates: Requirements 4.5, 5.4, 5.5, 5.6, 6.9, 13.4, 14.9**

  - [x] 12.3 Write Property Test 3: Technical Accuracy (No Forbidden Terms)
    - In `scripts/test_document.py`, implement a hypothesis property test that randomly samples sentences from technical sections (Chapters 3–6) and asserts no sampled sentence contains the forbidden terms ("Flask", "Django", "Laravel", "React", "Vue", "Angular", "Bootstrap", "Tailwind", "MySQL", "MongoDB", "AWS") as the system's own technology
    - **Property 3: Technical Accuracy**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**

  - [x] 12.4 Write Property Test 4: Minimum Document Length
    - In `scripts/test_document.py`, implement a single-execution test (not randomised) that reads the full `expanded_research_document.md` and asserts `word_count(full_text) >= 75000`
    - **Property 4: Minimum Document Length**
    - **Validates: Requirements 9.11**

- [x] 13. Generate new document sections for Requirements 11–14
  - [x] 13.1 Expand Section 2.4 — Scholarship and Tertiary Financing Landscape
    - Append or update Section 2.4 to include a dedicated sub-section describing: the HEFoND funding model (MTI bands and scholarship-to-loan ratio), the NG-CDF constituency-level bursary disbursement mechanism, and at least three named private foundation scholarships (Equity Wings to Fly, KCB Foundation, Safaricom Foundation), each with APA citations
    - _Requirements: 11.5_

  - [x] 13.2 Expand Section 5.3 — Requirement Analysis (scholarship repository + career profiling sub-sections)
    - Append or update Section 5.3 to include:
      - A scholarship repository functional requirement sub-section specifying: searchable fields (name, provider, description, eligibility_criteria), category filter (Government / Private / International), and admin CRUD operations
      - A career profiling module functional requirement sub-section specifying: the four profiling steps, the seven KCSE subjects (Step 1), the six skill ratings (Step 2), and the preference fields (Step 3: work_environment, industry_interests, motivation, relocate, budget, education_goal)
      - A description of the CAREERS database across six domains: Health Sciences, Engineering and Technology, Business and Economics, Arts Media and Law, Agriculture and Environment, Education and Social Sciences
    - _Requirements: 11.6, 14.8, 14.11_

  - [x] 13.3 Verify and update Section 4.2 — Four weaknesses of the current system
    - Confirm Section 4.2 explicitly names all four weaknesses: (a) geographic inequality in access to career information, (b) scholarship information silos with no centralised repository, (c) absence of data-driven or algorithmic career matching, (d) dependence on individual counselor knowledge with no standardised process; expand if any are missing
    - _Requirements: 13.2_

  - [x] 13.4 Verify and update Section 5.6 Table 5.4 — scholarships data dictionary completeness
    - Confirm Table 5.4 (Data Dictionary: scholarships) lists all nine fields: id, name, provider, description, eligibility_criteria, deadline, link, category, amount — with correct types, constraints, and descriptions matching `api/index.py` `init_db()`; add category and amount rows if absent
    - _Requirements: 11.9, 6.6_

  - [x] 13.5 Verify and update Section 5.5 — run_algorithm() pseudocode completeness
    - Confirm the pseudocode for `run_algorithm()` in Section 5.5 covers all five steps: (a) grade mapping via GRADE_MAP, (b) mean grade computation and study_level determination, (c) career filtering by education_goal and min_grade, (d) score computation (subject_score + trait_score + industry_score), (e) normalisation to percentage match; expand if any step is missing
    - _Requirements: 14.7_

  - [x] 13.6 Verify and update Section 3.8 — deployment environment variables
    - Confirm Section 3.8 names all three production environment variables: `Careerdatabase_URL`, `careerapp_gmail`, `careerapps_password`; add them if absent
    - _Requirements: 12.8_

- [x] 14. Write additional unit tests for Requirements 11–14
  - [x] 14.1 Write unit test: GRADE_MAP accuracy in document
    - In `scripts/test_document.py`, add a test that searches the document for the GRADE_MAP description and asserts it states A=12, A-=11, B+=10, B=9, B-=8, C+=7, C=6, C-=5, D+=4, D=3, D-=2, E=1
    - _Requirements: 14.2_

  - [x] 14.2 Write unit test: Four weaknesses in Section 4.2
    - In `scripts/test_document.py`, add a test that extracts Section 4.2 and asserts it contains all four weakness keywords: "geographic inequality", "scholarship information silos" (or "centralised repository"), "algorithmic" (or "data-driven"), "standardised process" (or "individual counselor")
    - _Requirements: 13.2_

  - [ ]* 14.3 Write unit test: scholarships data dictionary completeness
    - In `scripts/test_document.py`, add a test that extracts Table 5.4 and asserts all nine field names appear: id, name, provider, description, eligibility_criteria, deadline, link, category, amount
    - _Requirements: 11.9_

  - [ ]* 14.4 Write unit test: study_level display in Section 5.7
    - In `scripts/test_document.py`, add a test that extracts Section 5.7 and asserts it mentions `study_level` being displayed alongside the ranked career list on the recommendations page
    - _Requirements: 14.6_

  - [ ]* 14.5 Write unit test: pseudocode completeness
    - In `scripts/test_document.py`, add a test that locates the `run_algorithm()` pseudocode block in Section 5.5 and asserts it contains all five step markers: "GRADE_MAP" (or "grade mapping"), "mean_grade", "education_goal", "subject_score", "normalise" (or "max_score")
    - _Requirements: 14.7_

  - [ ]* 14.6 Write unit test: deployment environment variables
    - In `scripts/test_document.py`, add a test that searches Section 3.8 and asserts all three env var names appear: `Careerdatabase_URL`, `careerapp_gmail`, `careerapps_password`
    - _Requirements: 12.8_

  - [ ]* 14.7 Write unit test: SUS scoring formula and Bangor scale
    - In `scripts/test_document.py`, add a test that extracts Section 6.4 and asserts it contains: the SUS scoring formula ("× 2.5" or "multiply by 2.5"), the threshold "68" (above-average), the threshold "80.3" (excellent), and "Bangor"
    - _Requirements: 12.9_

- [x] 15. Write property-based tests for algorithm and scholarship correctness (Properties 5–11)
  - [x] 15.1 Write Property Test 5: Algorithm Output Shape
    - In `scripts/test_document.py`, implement a hypothesis property test that generates random `profile_data` dicts with valid KCSE grade strings and asserts: `len(result) <= 8`; all scores are integers in `[0, 100]`; if result is non-empty, `result[0][0] == 100`
    - Import `run_algorithm` from `api.index` and `CAREERS` from `api.career_database`
    - **Property 5: Algorithm Output Shape**
    - **Validates: Requirements 14.1, 14.3**

  - [x] 15.2 Write Property Test 6: Algorithm Filter Invariants
    - In `scripts/test_document.py`, implement a hypothesis property test that generates random `profile_data` dicts (with and without `education_goal`) and asserts: every returned career's `min_grade <= mean_grade`; if `education_goal` is non-empty, every returned career's `level == education_goal`
    - **Property 6: Algorithm Filter Invariants**
    - **Validates: Requirements 14.4, 14.5**

  - [x] 15.3 Write Property Test 7: GRADE_MAP Conversion Correctness
    - In `scripts/test_document.py`, implement a hypothesis property test that randomly samples grade strings from `GRADE_MAP` keys and asserts: `map_grade(grade) == GRADE_MAP[grade]`; for any career, `subject_score == sum(map_grade(user_inputs[s]) * 2 for s in career['subjects'])`
    - Import `map_grade` and `GRADE_MAP` from `api.index`
    - **Property 7: GRADE_MAP Conversion Correctness**
    - **Validates: Requirements 14.2**

  - [x] 15.4 Write Property Test 8: study_level Determination
    - In `scripts/test_document.py`, implement a hypothesis property test that generates random float values for `mean_grade` in `[0.0, 12.0]` and asserts the `study_level` returned by `run_algorithm()` matches the threshold rules exactly: ≥7.0 → "University / Graduate", ≥5.0 → "Diploma / TVET", ≥3.0 → "Certificate", <3.0 → "Artisan"
    - **Property 8: study_level Determination**
    - **Validates: Requirements 14.6**

  - [x] 15.5 Write Property Test 9: Scholarship Search Correctness
    - In `scripts/test_document.py`, implement a hypothesis property test that generates random keyword strings and a random set of scholarship record dicts and asserts: every record returned by the search logic contains the keyword (case-insensitive) in name, provider, description, or eligibility_criteria; no non-matching record appears
    - Test the search SQL logic by calling the relevant query helper directly against a temporary SQLite in-memory database
    - **Property 9: Scholarship Search Correctness**
    - **Validates: Requirements 11.2**

  - [x] 15.6 Write Property Test 10: Scholarship Category Invariant
    - In `scripts/test_document.py`, implement a hypothesis property test that samples scholarship records from the database after `seed_scholarships()` runs and asserts every record's `category` field is one of `{"Government", "Private", "International"}`
    - **Property 10: Scholarship Category Invariant**
    - **Validates: Requirements 11.4**

  - [x] 15.7 Write Property Test 11: Admin CRUD Round-Trip
    - In `scripts/test_document.py`, implement a hypothesis property test that generates random scholarship record dicts with valid field values, inserts them into a temporary in-memory SQLite database, and asserts: after INSERT, a SELECT by name returns the record with all fields intact; after DELETE, a SELECT by id returns nothing
    - **Property 11: Admin CRUD Round-Trip**
    - **Validates: Requirements 11.7**

- [x] 16. Write integration tests for OTP flow, scholarship seed, and Vercel config
  - [x] 16.1 Write integration test: OTP flow
    - In `scripts/test_document.py`, add an integration test that: creates a temporary in-memory SQLite database, calls the registration logic to insert a user, verifies a 6-digit OTP is stored in `verification_tokens` with `expires_at` approximately `now + 600`, then submits the correct OTP and asserts `is_verified` is set to 1 in the `users` table
    - _Requirements: 12.2, 12.3_

  - [x] 16.2 Write integration test: Scholarship seed coverage
    - In `scripts/test_document.py`, add an integration test that: creates a temporary in-memory SQLite database, calls `seed_scholarships()`, then queries the `scholarships` table and asserts records exist for all three categories: Government, Private, and International
    - _Requirements: 11.1_

  - [ ]* 16.3 Write integration test: Vercel configuration validity
    - In `scripts/test_document.py`, add a test that reads `vercel.json`, parses it as JSON, and asserts it contains a rewrite or route rule that maps all paths (or `"/(.*)"`) to `api/index.py`
    - _Requirements: 12.1_

- [x] 17. Generate References and Appendices
  - [x] 17.1 Write References section
    - Append the References/Bibliography section with ≥20 APA-format entries covering: Holland (1997), Davis (1989) TAM, Lent et al. (1994) SCCT, Kenya Ministry of Education CBC policy documents, KUCCPS annual reports, Naviance product documentation, Bangor et al. (2008) SUS adjective rating scale, and peer-reviewed EdTech/Sub-Saharan Africa journal articles
    - _Requirements: 8.1, 8.3_

  - [ ]* 17.2 Write unit test: Reference count
    - In `scripts/test_document.py`, extract the References section and assert it contains ≥20 APA-formatted entries (count lines matching the pattern of an APA reference)
    - _Requirements: 8.1_

  - [x] 17.3 Write Appendix A — Student Questionnaire
    - Append Appendix A with a sample student questionnaire of ≥15 numbered questions covering demographics, career awareness, scholarship awareness, and portal usability
    - _Requirements: 8.2_

  - [ ]* 17.4 Write unit test: Appendix A question count
    - In `scripts/test_document.py`, extract Appendix A and assert it contains ≥15 numbered questions
    - _Requirements: 8.2_

  - [x] 17.5 Write Appendix B — Key Informant Interview Guide
    - Append Appendix B with a sample KII guide of ≥8 numbered questions for career counselors
    - _Requirements: 8.2_

  - [ ]* 17.6 Write unit test: Appendix B question count
    - In `scripts/test_document.py`, extract Appendix B and assert it contains ≥8 numbered questions
    - _Requirements: 8.2_

  - [x] 17.7 Write Appendix C — Budget and Time Schedule
    - Append Appendix C with a budget/time schedule table (Markdown pipe table, caption above) covering project phases, activities, duration, and estimated costs
    - _Requirements: 8.2_

- [x] 18. Run all validation checks and fix any failures
  - [x] 18.1 Run all unit tests and property tests
    - Execute `pytest scripts/test_document.py -v` and review output; fix any failing assertions by expanding the relevant document sections or correcting the implementation
    - _Requirements: 9.11, 10.1–10.8, 11.1–11.9, 12.1–12.9, 13.1–13.9, 14.1–14.11_

  - [ ]* 18.2 Run word count validation
    - Execute `python scripts/validate_document.py` to confirm total word count ≥75,000; if below threshold, identify the shortest chapters and expand them
    - _Requirements: 9.11_

  - [ ]* 18.3 Run forbidden-term scan
    - Use `find_forbidden_terms()` from `validate_document.py` to scan the full document and confirm zero occurrences of Flask, Django, React, Bootstrap, Tailwind, MySQL, MongoDB, AWS as the system's own technology
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ]* 18.4 Run Mermaid block count check
    - Use `count_mermaid_blocks()` from `validate_document.py` to confirm ≥11 fenced ` ```mermaid ` blocks are present (Figures 4.1–4.3 and 5.1–5.11)
    - _Requirements: 4.5, 5.4, 5.5, 5.6, 6.9_

- [x] 19. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

---

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- All content is appended sequentially to `Documents/expanded_research_document.md` — never overwrite earlier sections
- Every technical claim must be cross-referenced against the source-of-truth table in `design.md` before writing; the codebase (`api/index.py`) takes precedence over the existing document
- Mermaid node labels containing parentheses must be quoted (e.g., `A["label (with parens)"]`); `sequenceDiagram` participant names with spaces must use aliases
- All figure captions go **below** the figure; all table captions go **above** the table
- APA in-text citations follow the `(Author, Year)` or `(Author et al., Year)` pattern throughout
- Property tests use `hypothesis` with a minimum of 100 iterations per property
- Properties 5–11 test the live Python code in `api/index.py` and `api/career_database.py` directly — import them using `sys.path` manipulation or by running pytest from the workspace root
