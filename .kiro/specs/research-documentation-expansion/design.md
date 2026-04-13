# Design Document: Research Documentation Expansion

## Overview

This design describes the strategy for expanding the existing 46-page academic research document — *"WEB-BASED CAREER GUIDANCE AND SCHOLARSHIP INFORMATION PORTAL: A CASE OF KENYAN FORM FOUR LEAVERS"* — into a complete, submission-ready academic project document of 150+ pages. The expansion covers all preliminary pages, Chapters 1–6, References, and Appendices, conforming to the formatting and academic standards prescribed by Dr. Ishmael Nick.

The Document_Generator (this AI system) will produce structured Markdown content that maps directly to Microsoft Word formatting. Every technical claim will be grounded in the actual codebase: a Pure Python `http.server` backend (`api/index.py`), Vanilla HTML5/CSS3/JavaScript frontend, SQLite (development) / PostgreSQL via Neon (production), and deployment on Vercel.

---

## Architecture

### Document Generation Strategy

The document is generated in a single, sequential pass through all sections, in the order they appear in the final submission. This ensures cross-references (figure numbers, table numbers, page references) are consistent and the narrative flows coherently from chapter to chapter.

The generation follows a **layered expansion model**:

1. **Skeleton pass** — establish all headings and sub-headings with correct numbering.
2. **Content pass** — fill each section with full academic prose, meeting minimum length requirements.
3. **Artifact pass** — insert all Mermaid diagrams, tables, pseudocode blocks, and data dictionaries.
4. **Citation pass** — verify every paragraph containing a theory or external fact carries an APA in-text citation.
5. **Consistency pass** — verify figure/table captions follow the `Figure X.Y:` / `Table X.Y:` convention and all cross-references are correct.

### Output Format

The output is a single Markdown file structured so that:
- Heading levels (`#`, `##`, `###`, `####`) map to Word Heading 1–4 styles.
- Body paragraphs are plain text (Word will apply Times New Roman 12pt, 1.5-spaced, justified).
- The Abstract is wrapped in an `> italic blockquote` to signal single-spaced italic formatting.
- Mermaid diagrams are wrapped in fenced code blocks tagged ` ```mermaid `.
- Tables use standard Markdown pipe syntax.
- Page number placeholders are written as `[p. X]` for manual replacement in Word.
- Roman numeral page sections (preliminary pages) are separated from Arabic numeral sections (main chapters) by a horizontal rule and a comment marker.

### Technical Accuracy Enforcement

All technical descriptions are derived directly from the codebase:

| Claim | Source of Truth |
|---|---|
| Backend: Pure Python `http.server` | `api/index.py` line 1: `import http.server` |
| No Flask/Django | Absence of Flask/Django imports in all `.py` files |
| SHA-256 password hashing | `api/index.py`: `hashlib.sha256(pw.encode()).hexdigest()` |
| OTP: 6-digit, Gmail SMTP port 465 | `api/index.py`: `generate_otp()`, `smtplib.SMTP_SSL('smtp.gmail.com', 465)` |
| OTP expiry: 10 minutes | `api/index.py`: `int(time.time()) + 600` |
| PostgreSQL via pg8000 | `api/index.py`: `import pg8000`, `pg8000.connect(...)` |
| Deployment: Vercel | `vercel.json`: rewrites all routes to `api/index.py` |
| GRADE_MAP A=12 to E=1 | `api/index.py`: `GRADE_MAP = {'A':12,'A-':11,...,'E':1,'':0}` |
| Four DB tables | `api/index.py`: `init_db()` creates `users`, `sessions`, `verification_tokens`, `scholarships` |
| Four profiling steps | Routes `/profile/step1` through `/profile/step4` and `/profile/submit` |
| Algorithm: weighted scoring | `run_algorithm()`: subject_score + trait_score + industry_score, normalised to % |
| scholarships.category field | `api/index.py`: `init_db()` — `category TEXT DEFAULT 'General'`; migrated via `ALTER TABLE` |
| scholarships.amount field | `api/index.py`: `init_db()` — `amount TEXT DEFAULT ''`; migrated via `ALTER TABLE` |
| study_level thresholds | `run_algorithm()`: ≥7.0 → University/Graduate; ≥5.0 → Diploma/TVET; ≥3.0 → Certificate; else → Artisan |
| education_goal filter | `run_algorithm()`: `if education_goal and c['level'] != education_goal: continue` |
| Seed data: 10 scholarships | `api/index.py`: `seed_scholarships()` — Government, Private, International categories |

---

## Components and Interfaces

### Section-by-Section Breakdown

#### Preliminary Pages

| Section | Target Length | Key Content |
|---|---|---|
| Cover Page | 1 page | Title, student name (IGNATIUS ETHENS CIT-221-048/2022), supervisor (DR. ISHMAEL NICK), Faculty of Computing and Information Technology, year |
| Blank Page | 1 page | No content, no page number |
| Declaration & Approval | 1 page | Student, University Supervisor, Head of Department signature blocks |
| Dedication | ~0.5 page | Personal dedication |
| Acknowledgements | ~0.5 page | Supervisor, family, institution |
| Abstract | 150–300 words | Single-spaced, italicised; covers problem, methodology, tech stack, results, conclusion |
| Table of Contents | 2–3 pages | All headings with page number placeholders |
| List of Figures | 1 page | All Figure X.Y captions |
| List of Tables | 1 page | All Table X.Y captions |
| Definition of Key Terms | 1–2 pages | ≥13 terms from glossary |

#### Chapter One — Introduction

| Section | Target Length | Key Content |
|---|---|---|
| 1.1 Chapter Introduction | ≥1 page | Lists all sub-sections |
| 1.2 Motivation and Background | ≥1.5 pages | First-person narrative; personal and societal motivation |
| 1.3 Background of the Study | ≥3 pages | Global context → 7-4-2-3 → 8-4-4 → CBC; HELB/HEFoND/MTI/NG-CDF; information asymmetry |
| 1.4 Problem Statement | ≥1 page | Continuous prose; five Ws; ≥2 citations |
| 1.5 Aim of the Research | ≤1 paragraph | Single broad action-verb statement |
| 1.6 Objectives | ≥0.5 page | 1 main + 3–4 SMART specific objectives |
| 1.7 Justification | ≥1.5 pages | Policy alignment, equity, economic optimisation, tech advancement; anchored on published research |
| 1.8 Scope | ≥0.5 page | Target org, features, explicit limitations |
| 1.9 Research Organisation | ≥0.5 page | One paragraph per chapter (7 chapters) |
| 1.10 Chapter Summary | ≥1 paragraph | Synthesis of Chapter One |

#### Chapter Two — Literature Review

| Section | Target Length | Key Content |
|---|---|---|
| 2.1 Chapter Introduction | ≥0.5 page | Lists all sub-sections |
| 2.2 Theoretical Framework | ≥3 pages | RIASEC (Holland, 1997) + CBC mapping; SCCT (Lent et al., 1994) + Kenyan context; TAM (Davis, 1989) + mobile-first |
| 2.3 History of the Research Topic | ≥3 pages | Post-independence 7-4-2-3 → 8-4-4 → CBC chronology |
| 2.4 Scholarship & Financing Landscape | ≥1.5 pages | HEF model, MTI bands, HELB/HEFoND, Equity Wings to Fly, KCB Foundation, NG-CDF |
| 2.5 Review of Related Systems | ≥2 pages | Naviance (global), KUCCPS Portal (local govt), Craydel (local commercial); Table 2.1 comparative analysis |
| 2.6 Emerging Trends | ≥2 pages | AI/ML in EdTech; one-stop-shop integration; PWA/mobile-first in Sub-Saharan Africa; data privacy |
| 2.7 Research Gap | ≥1.5 pages | Contextual Gap (CBC), Integration Gap (Diagnostic+Enabler), Accessibility Gap (free/lightweight) |
| 2.8 Chapter Summary | ≥1 paragraph | Synthesis; bridge to Chapter Three |

#### Chapter Three — Research Methodology

| Section | Target Length | Key Content |
|---|---|---|
| 3.1 Chapter Introduction | ≥0.5 page | Lists all sub-sections |
| 3.2 Methodology for Literature Review | ≥1.5 pages | Mixed-methods rationale; 6 generic steps; databases and search terms |
| 3.3 Methodology for Requirement Specification | ≥3 pages | Mixed-methods design; target population; stratified random sampling; purposive sampling; KII; digital questionnaires; document analysis |
| 3.4 Methodology for System Analysis (Current) | ≥1.5 pages | System Analysis definition; Context Diagram; DFD; Flowchart |
| 3.5 Methodology for System Design (Proposed) | ≥4 pages | DFDs; Flowcharts; Sequence Diagrams (4); Collaboration Diagrams; Use Case Diagrams; Pseudocode; I/O design; UI principles; ERD; normalisation; data dictionary |
| 3.6 Methodology for System Implementation | ≥2 pages | Agile Scrum + Sprint structure; Pure Python stack; SQLite/PostgreSQL; pg8000 |
| 3.7 Methodology for System Testing | ≥1.5 pages | Testing plan; functional vs non-functional; unit/integration/system/UAT/SUS |
| 3.8 Methodology for System Deployment | ≥1 page | Deployment pipeline; local SQLite dev; Vercel cloud |
| 3.9 Chapter Summary | ≥1 paragraph | Synthesis |

#### Chapter Four — System Analysis (Current System)

| Section | Target Length | Key Content |
|---|---|---|
| 4.1 Chapter Introduction | ≥0.5 page | Lists all sub-sections |
| 4.2 Description of Current System | ≥2 pages | Manual guidance process in Nairobi and peri-urban schools; role of career counselor; use of printed KUCCPS booklets and verbal advice; absence of digital tools; low counselor-to-student ratio; **four documented weaknesses**: (a) geographic inequality in access to career information, (b) scholarship information silos with no centralised repository, (c) absence of data-driven or algorithmic career matching, (d) dependence on individual counselor knowledge with no standardised process |
| 4.3 Feasibility Study | ≥2 pages | Technical, Economic, Operational feasibility; conclusion |
| 4.4 Data I/O Analysis | ≥1 page | Inputs: KCSE grade slips, counselor notes, printed booklets; entity relationships: student ↔ counselor ↔ KUCCPS ↔ scholarship bodies; outputs: verbal career advice, printed referral letters, scholarship application forms |
| 4.5 Process Logic Design (Current) | ≥2 pages | Context Diagram (`flowchart LR`, Mermaid); Level-0 DFD (`flowchart TD`, Mermaid); Flowchart of current manual guidance process (`flowchart TD`, Mermaid) |
| 4.6 Chapter Summary | ≥1 paragraph | Synthesis |

#### Chapter Five — System Design (Proposed System)

| Section | Target Length | Key Content |
|---|---|---|
| 5.1 Introduction | ≥0.5 page | Lists all sub-sections |
| 5.2 Description of Proposed System | ≥1.5 pages | Strengths and limitations |
| 5.3 Requirement Analysis | ≥2 pages | Functional, Non-Functional, User, Usability requirements |
| 5.4 Conceptual Architecture | ≥1 page | Three-tier architecture; Mermaid system architecture diagram |
| 5.5 Process Logic Design (Proposed) | ≥6 pages | Use Case Diagram; Activity Diagram; 4× Sequence Diagrams; Class Diagram; Collaboration Diagram; Context Diagram; Level-0 DFD; Pseudocode for `run_algorithm()` |
| 5.6 Database Design | ≥3 pages | ERD (Mermaid erDiagram); normalisation (1NF–3NF); data dictionary for all 4 tables — **Table 5.4 (scholarships) must list all 9 fields: id, name, provider, description, eligibility_criteria, deadline, link, category, amount** |
| 5.7 I/O Design | ≥2 pages | 4 key screen descriptions (Landing, Step 1, Recommendations, Scholarships) |
| 5.8 Chapter Summary | ≥1 paragraph | Synthesis |

#### Chapter Six — System Implementation and Testing

| Section | Target Length | Key Content |
|---|---|---|
| 6.1 Chapter Introduction | ≥0.5 page | Lists all sub-sections |
| 6.2 System Screenshots | ≥2 pages | 4 screenshot descriptions with Figure captions |
| 6.3 Testing Plan | ≥3 pages | Table with ≥10 test cases; all required columns |
| 6.4 Evaluation Plan | ≥2 pages | UAT/SUS methodology; pilot group: minimum 10 Form Four students + 5 career counselors from Nairobi-based schools; all 10 standard SUS questionnaire items; **SUS scoring formula: sum of converted scores × 2.5** (odd items: score − 1; even items: 5 − score); score interpretation: ≥68 = above-average usability, ≥80.3 = excellent usability; **Bangor et al. (2008) adjective rating scale** (Worst Imaginable → Poor → OK → Good → Excellent → Best Imaginable); discussion of expected score in low-bandwidth Kenyan school environments |
| 6.5 Chapter Summary | ≥1 paragraph | Synthesis |

#### Chapter Seven — Conclusions, Findings and Recommendations

| Section | Target Length | Key Content |
|---|---|---|
| 7.1 Introduction | ≥0.5 page | Lists all sub-sections of Chapter Seven |
| 7.2 Conclusion | ≥2 pages | Summary of key findings; confirmation that aim and objectives were achieved; significance of the portal as a contribution to EdTech in Kenya |
| 7.3 Challenges Encountered | ≥1 page | Technical challenges (Pure Python serverless constraints, pg8000 compatibility, cookie-based state management), methodological challenges (sampling, data collection), contextual challenges (digital divide, CBC transition) |
| 7.4 Future Recommendations | ≥1 page | Live KUCCPS API integration, Kiswahili localisation, PWA offline mode, ML-enhanced recommendation engine, counselor matching feature, mobile app |
| 7.5 Chapter Conclusion | ≥1 paragraph | Formal closing paragraph for the entire research document |

#### Back Matter

| Section | Target Length | Key Content |
|---|---|---|
| References | ≥3 pages | ≥20 APA-format references |
| Appendix A | ≥2 pages | Student questionnaire (≥15 questions) |
| Appendix B | ≥1 page | Key Informant Interview guide (≥8 questions) |
| Appendix C | ≥1 page | Budget and time schedule table |

---

## Data Models

### Database Schema (Actual Implementation)

The following schema is derived directly from `api/index.py` `init_db()` function and must be accurately reflected in all documentation.

**Table: users**

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER / SERIAL | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| full_name | TEXT | NULL allowed | Student's full name |
| email | TEXT | UNIQUE, NOT NULL | Login email address |
| password | TEXT | NOT NULL | SHA-256 hashed password |
| role | TEXT | DEFAULT 'student' | 'student' or 'counselor' |
| school | TEXT | NULL allowed | Student's school name |
| phone | TEXT | NULL allowed | Contact phone number |
| study_areas | TEXT | NULL allowed | Preferred study areas |
| is_verified | INTEGER | DEFAULT 0 | Email verification flag (0/1) |
| created_at | INTEGER / BIGINT | DEFAULT 0 | Unix timestamp of registration |
| profile_data | TEXT | NULL allowed | JSON blob of profiling step data |
| last_results | TEXT | NULL allowed | JSON blob of last algorithm results |

**Table: sessions**

| Field | Type | Constraints | Description |
|---|---|---|---|
| session_id | TEXT | PRIMARY KEY | UUID session token stored in cookie |
| user_id | INTEGER | Foreign key → users.id | Owning user |
| created_at | INTEGER / BIGINT | — | Unix timestamp of session creation |

**Table: verification_tokens**

| Field | Type | Constraints | Description |
|---|---|---|---|
| token | TEXT | PRIMARY KEY | 6-digit OTP (registration) or UUID (password reset) |
| user_id | INTEGER | Foreign key → users.id | Owning user |
| expires_at | INTEGER / BIGINT | — | Unix timestamp; OTP expires in 600 seconds (10 min) |

**Table: scholarships**

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INTEGER / SERIAL | PRIMARY KEY, AUTOINCREMENT | Unique scholarship identifier |
| name | TEXT | — | Scholarship name |
| provider | TEXT | — | Awarding organisation |
| description | TEXT | — | Full description |
| eligibility_criteria | TEXT | — | Eligibility requirements |
| deadline | TEXT | — | Application deadline (string) |
| link | TEXT | — | External application URL |
| category | TEXT | DEFAULT 'General' | Funding category: Government, Private, or International |
| amount | TEXT | DEFAULT '' | Funding amount or range (e.g., "Up to KES 60,000/year") |

> **Note:** The `category` and `amount` fields were added via `ALTER TABLE` migration in `init_db()` and are present in both the SQLite and PostgreSQL schemas. All documentation in Section 5.6 (Table 5.4 Data Dictionary: scholarships) must list all nine fields including `category` and `amount`.

### Career Recommendation Algorithm Data Model

The `run_algorithm(profile_data)` function in `api/index.py` operates on the following data:

**Input** (`profile_data` dict, assembled from cookies across Steps 1–3):
- Step 1 grades: `math_grade`, `english_grade`, `kiswahili_grade`, `biology_grade`, `chemistry_grade`, `physics_grade`, `humanities_grade` — each an KCSE grade string (A, A-, B+, …, E)
- Step 2 skills: `problem_solving`, `rating_analytical`, `rating_coding`, `rating_verbal`, `rating_critical`, `rating_creative`, `rating_leadership` — integer ratings 1–5
- Step 3 preferences: `work_environment`, `teamwork`, `motivation`, `industry_interests` (comma-separated), `relocate`, `budget`, `education_goal`

**Processing**:
1. Map each grade string to a numeric value via `GRADE_MAP` (A=12, A-=11, B+=10, B=9, B-=8, C+=7, C=6, C-=5, D+=4, D=3, D-=2, E=1, blank=0)
2. Compute `mean_grade` = sum of all mapped grade values / 7 (denominator is always 7, even if some subjects are blank)
3. Determine `study_level` from `mean_grade`:
   - `mean_grade ≥ 7.0` → `"University / Graduate"`
   - `mean_grade ≥ 5.0` → `"Diploma / TVET"`
   - `mean_grade ≥ 3.0` → `"Certificate"`
   - `mean_grade < 3.0` → `"Artisan"`
   - `study_level` is displayed on the recommendations page alongside the ranked career list
4. For each career in `CAREERS` database:
   - **Education goal filter**: if `education_goal` is set (non-empty), skip any career whose `level` field does not exactly match `education_goal`
   - **Grade threshold filter**: skip any career where `mean_grade < career['min_grade']`
   - `subject_score` = sum of `map_grade(user_inputs[subject]) × 2` for each subject in career's `subjects` list
   - `trait_score` = sum of `career['traits'].get(trait, 0)` for each trait string in the user's trait list
   - `industry_score` = sum of 8 for each industry in `industry_list` that appears in `career['industries']`
   - `total = subject_score + trait_score + industry_score`
5. Sort all scored careers descending by `total`
6. Normalise top 8: `match_pct = round((score / max_score) × 100)` where `max_score` is the highest total in the filtered set (minimum 1 to avoid division by zero)
7. If zero careers pass all filters, return an empty list and the portal displays a no-match message

**Output**: Tuple `(result, mean_grade, study_level, user_inputs)` where `result` is a list of `(match_pct, career_dict)` tuples, at most 8 entries

---

## Diagram Generation Strategy

All diagrams are rendered as Mermaid.js code blocks. The following diagrams are required:

### Chapter Four Diagrams

**Figure 4.1 — Context Diagram (Current System)**
Type: `flowchart LR` — shows Student, Counselor, KUCCPS, Scholarship Bodies as external entities interacting with the manual guidance process.

**Figure 4.2 — Level-0 DFD (Current System)**
Type: `flowchart TD` — shows data flows between Student, Counselor, and the manual processes (Grade Collection, Career Advice, Scholarship Referral).

**Figure 4.3 — Flowchart (Current Manual Guidance Process)**
Type: `flowchart TD` — shows the step-by-step manual process from student inquiry to career advice delivery.

### Chapter Five Diagrams

**Figure 5.1 — System Architecture Diagram (Three-Tier)**
Type: `flowchart TD` — shows Presentation Layer (HTML/CSS/JS), Application Layer (Python http.server), Data Layer (SQLite/PostgreSQL).

**Figure 5.2 — Use Case Diagram**
Type: `flowchart LR` — three actors (Learner, Counselor, Admin) with all use cases (Register, Login, Complete Profile, View Recommendations, Search Scholarships, Manage Scholarships, View Dashboard, Manage Users).

**Figure 5.3 — Activity Diagram (Career Profiling Workflow)**
Type: `flowchart TD` — shows the four-step profiling flow: Step 1 (Grades) → Step 2 (Skills) → Step 3 (Preferences) → Step 4 (Review) → Submit → Algorithm → Recommendations.

**Figure 5.4 — Sequence Diagram: User Registration with OTP**
Type: `sequenceDiagram` — participants: Browser, PortalRequestHandler, Database, Gmail SMTP. Shows POST /register → INSERT users → generate OTP → INSERT verification_tokens → send_otp_email → render verify_otp.html.

**Figure 5.5 — Sequence Diagram: Multi-Step Career Profiling**
Type: `sequenceDiagram` — participants: Browser, PortalRequestHandler, Cookie Store, run_algorithm, Database. Shows Steps 1–4 cookie accumulation → POST /profile/submit → run_algorithm() → UPDATE users → render recommendations.html.

**Figure 5.6 — Sequence Diagram: Scholarship Search**
Type: `sequenceDiagram` — participants: Browser, PortalRequestHandler, Database. Shows GET /scholarships?q=keyword → SELECT with LIKE → render scholarships.html.

**Figure 5.7 — Sequence Diagram: Admin Scholarship Management**
Type: `sequenceDiagram` — participants: AdminBrowser, PortalRequestHandler, Database. Shows POST /admin/add_scholarship → INSERT scholarships → redirect /admin?msg=added.

**Figure 5.8 — Class Diagram**
Type: `classDiagram` — shows `handler` class (extends `http.server.BaseHTTPRequestHandler`) with methods: `get_current_user()`, `render_template()`, `send_redirect()`, `send_html()`, `serve_static()`, `do_GET()`, `do_POST()`, `_handle_post()`. Shows module-level functions: `run_algorithm()`, `init_db()`, `get_db_connection()`, `hash_password()`, `send_otp_email()`, `generate_otp()`.

**Figure 5.9 — Context Diagram (Proposed System)**
Type: `flowchart LR` — shows Student, Counselor, Admin, Gmail SMTP, Neon PostgreSQL, Vercel as external entities interacting with the Portal.

**Figure 5.10 — Level-0 DFD (Proposed System)**
Type: `flowchart TD` — shows data flows between all actors and the system's main processes (Authentication, Career Profiling, Recommendation Engine, Scholarship Repository, Admin Management).

**Figure 5.11 — Entity-Relationship Diagram**
Type: `erDiagram` — shows all four tables with attributes and relationships: `users ||--o{ sessions`, `users ||--o{ verification_tokens`, `users` standalone, `scholarships` standalone.

### Diagram Naming Convention

All figures follow the format `Figure X.Y: [Description]` with the caption placed **below** the diagram code block. All tables follow `Table X.Y: [Description]` with the caption placed **above** the table.

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: APA Citation Coverage

*For any* paragraph in the generated document that contains a theory, named model, statistical claim, or reference to an external system, that paragraph SHALL contain at least one APA in-text citation matching the pattern `(Author, Year)` or `(Author et al., Year)`.

**Validates: Requirements 3.9, 8.3, 9.10**

### Property 2: Mermaid Diagram Completeness

*For any* diagram type listed in the requirements (Context Diagram current, DFD current, Flowchart current, System Architecture, Use Case, Activity, Sequence ×4, Class, Context Diagram proposed, DFD proposed, ERD), the generated document SHALL contain a fenced code block tagged with the `mermaid` language identifier containing syntactically valid Mermaid markup for that diagram type.

**Validates: Requirements 4.5, 5.4, 5.5, 5.6, 6.9, 13.4, 14.9**

### Property 3: Technical Accuracy (No Incorrect Technology Terms)

*For any* section of the generated document that describes the system's backend, frontend, or database implementation, the terms "Flask", "Django", "Laravel", "React", "Vue", "Angular", "Bootstrap", "Tailwind", "MySQL", "MongoDB", and "AWS" SHALL NOT appear as the technology used by this system. The terms "http.server", "sqlite3", "pg8000", "hashlib", "smtplib", "Vercel", "Neon", "HTML5", "CSS3", and "JavaScript" SHALL appear in the appropriate technical sections.

**Validates: Requirements 10.1, 10.2, 10.3, 10.4**

### Property 4: Minimum Document Length

*For any* complete generation of the document, the total word count of all generated content SHALL be no less than 75,000 words (equivalent to approximately 150 pages at 500 words/page with standard formatting).

**Validates: Requirements 9.11**

### Property 5: Algorithm Output Shape

*For any* valid `profile_data` dictionary passed to `run_algorithm()`, the function SHALL return a result list containing at most 8 entries, where every entry's percentage match score is an integer in the range [0, 100], and — when the result list is non-empty — the first entry's score SHALL equal 100 (the top-ranked career is always normalised to 100%).

**Validates: Requirements 14.1, 14.3**

### Property 6: Algorithm Filter Invariants

*For any* `profile_data` dictionary, every career returned by `run_algorithm()` SHALL satisfy both of the following simultaneously: (a) the career's `min_grade` is less than or equal to the user's computed `mean_grade`, and (b) if `education_goal` is non-empty, the career's `level` field exactly matches `education_goal`.

**Validates: Requirements 14.4, 14.5**

### Property 7: GRADE_MAP Conversion Correctness

*For any* KCSE grade string in the set {A, A-, B+, B, B-, C+, C, C-, D+, D, D-, E, ""}, the `map_grade()` function SHALL return the exact numeric value specified in `GRADE_MAP` (A=12, A-=11, B+=10, B=9, B-=8, C+=7, C=6, C-=5, D+=4, D=3, D-=2, E=1, blank=0), and the `subject_score` component for any career SHALL equal the sum of `map_grade(grade) × 2` for each subject in that career's `subjects` list.

**Validates: Requirements 14.2**

### Property 8: study_level Determination

*For any* mean grade value computed by `run_algorithm()`, the returned `study_level` string SHALL be determined by the following exclusive thresholds: mean_grade ≥ 7.0 → "University / Graduate"; mean_grade ≥ 5.0 → "Diploma / TVET"; mean_grade ≥ 3.0 → "Certificate"; mean_grade < 3.0 → "Artisan". No other values are permitted.

**Validates: Requirements 14.6**

### Property 9: Scholarship Search Correctness

*For any* non-empty keyword string submitted to the scholarship search endpoint, every scholarship record returned by the query SHALL contain that keyword (case-insensitively) in at least one of the following fields: `name`, `provider`, `description`, or `eligibility_criteria`. No record that does not match the keyword in any of these fields SHALL appear in the results.

**Validates: Requirements 11.2**

### Property 10: Scholarship Category Invariant

*For any* scholarship record stored in or inserted into the `scholarships` table, the `category` field SHALL contain exactly one of the three permitted values: "Government", "Private", or "International". No record with a `category` value outside this set SHALL be accepted by the system.

**Validates: Requirements 11.4**

### Property 11: Admin CRUD Round-Trip

*For any* scholarship record added via the admin dashboard, a subsequent query of the `scholarships` table SHALL return that record with all fields intact. Conversely, for any scholarship record deleted via the admin dashboard, a subsequent query SHALL not return that record.

**Validates: Requirements 11.7**

---

## Error Handling

### Content Gaps

If a section cannot be fully expanded due to insufficient source material, the Document_Generator SHALL:
1. Write the maximum available content for that section.
2. Insert a clearly marked placeholder: `[EXPAND: minimum X more words needed — topic: Y]`.
3. Continue generating subsequent sections without stopping.

### Diagram Syntax Errors

All Mermaid diagrams must be validated against Mermaid syntax rules before inclusion. Common pitfalls to avoid:
- Node labels containing parentheses must be quoted: `A["label (with parens)"]`
- `erDiagram` attribute types must be valid Mermaid types (string, int, bigint, etc.)
- `sequenceDiagram` participant names with spaces must be aliased: `participant PH as PortalRequestHandler`
- Arrow labels in `flowchart` must not contain unescaped special characters

### Citation Gaps

If a paragraph makes a claim that cannot be attributed to a specific source in the reference list, the Document_Generator SHALL use the closest available reference and note it, rather than omitting the citation entirely. Fabricated citations are not permitted — only references from the approved list (Holland 1997, Davis 1989, Lent et al. 1994, Kenya MoE CBC documents, KUCCPS reports, etc.) shall be used.

### Technical Inaccuracy Prevention

Before writing any technical section, the Document_Generator SHALL cross-reference the claim against the source-of-truth table in the Architecture section above. If a discrepancy is detected between the existing document and the actual codebase, the codebase takes precedence and the document must be corrected.

Key areas requiring special attention:
- The `scholarships` table has **nine** fields (including `category` and `amount`) — not seven. Any data dictionary or ERD that omits these fields is incorrect.
- The `run_algorithm()` function returns a **4-tuple** `(result, mean_grade, study_level, user_inputs)` — not just a list. Documentation must reflect this.
- The `study_level` string values are exactly: `"University / Graduate"`, `"Diploma / TVET"`, `"Certificate"`, `"Artisan"` — no other values.
- The `education_goal` filter uses an exact string match against `career['level']` — not a substring match.

### Zero-Match Algorithm Output

If `run_algorithm()` returns an empty result list (all careers filtered out by `education_goal` or `min_grade`), the portal SHALL display a descriptive message informing the user that no careers matched their profile and suggesting they broaden their `education_goal` filter or revisit their grade entries. This case must be documented in Section 5.5 and covered by a test case in Section 6.3.

---

## Testing Strategy

### Applicability Assessment

This feature involves generating a large structured text document. The core logic is content generation and structural compliance, not algorithmic data transformation. However, several aspects are amenable to automated verification:

- **Citation coverage** — verifiable by regex pattern matching on the output text
- **Mermaid block completeness** — verifiable by counting fenced code blocks with `mermaid` tag
- **Technical term accuracy** — verifiable by keyword search (presence/absence)
- **Word count** — verifiable by word count function

Property-based testing is applicable for the citation coverage, diagram completeness, and technical accuracy properties, since these are universal properties that should hold across all paragraphs/sections of the document.

### Unit Tests

The following specific examples should be verified:

1. **Abstract word count** — generate the abstract and assert `150 ≤ word_count ≤ 300`
2. **Declaration page content** — verify student name `IGNATIUS ETHENS CIT-221-048/2022` and supervisor `DR. ISHMAEL NICK` appear
3. **Objectives format** — verify Section 1.6 contains exactly one main objective and 3–4 specific objectives
4. **Table 2.1 existence** — verify a comparative analysis table with Naviance, KUCCPS Portal, and Craydel rows exists
5. **Testing plan row count** — verify Section 6.3 table has ≥10 data rows, including test cases for OTP generation, OTP verification with valid code, OTP rejection with expired code, and full profiling workflow execution
6. **SUS items and scoring** — verify Section 6.4 contains all 10 standard SUS questionnaire items, the scoring formula (sum of converted scores × 2.5), and the Bangor et al. (2008) adjective rating scale with score thresholds (≥68 above average, ≥80.3 excellent)
7. **Reference count** — verify the References section contains ≥20 APA-formatted entries
8. **Appendix A question count** — verify the student questionnaire has ≥15 numbered questions
9. **Appendix B question count** — verify the KII guide has ≥8 numbered questions
10. **GRADE_MAP accuracy** — verify the document states A=12, A-=11, B+=10, …, E=1 in the algorithm description
11. **Four weaknesses in Section 4.2** — verify Section 4.2 explicitly names all four weaknesses: (a) geographic inequality, (b) scholarship information silos, (c) absence of algorithmic career matching, (d) dependence on individual counselor knowledge
12. **scholarships data dictionary completeness** — verify Table 5.4 lists all nine fields: id, name, provider, description, eligibility_criteria, deadline, link, category, amount
13. **study_level display** — verify the recommendations page description in Section 5.7 mentions that `study_level` is displayed alongside the ranked career list
14. **Pseudocode completeness** — verify Section 5.5 pseudocode for `run_algorithm()` covers all five steps: grade mapping, mean grade + study_level, education_goal filter, score computation, normalisation
15. **Deployment environment variables** — verify Section 3.8 names all three production environment variables: `Careerdatabase_URL`, `careerapp_gmail`, `careerapps_password`

### Property-Based Tests

Each property test uses a property-based testing library (e.g., `hypothesis` for Python) and runs a minimum of 100 iterations.

**Property Test 1: APA Citation Coverage**
Tag: `Feature: research-documentation-expansion, Property 1: APA citation coverage`
- Generator: randomly sample paragraphs from the generated document that contain theory/claim markers (words like "argues", "states", "found", "according to", "research shows", "studies indicate")
- Assertion: each sampled paragraph contains at least one match of the regex `\([A-Z][a-z]+(?:\s+et\s+al\.)?,\s+\d{4}\)`

**Property Test 2: Mermaid Diagram Completeness**
Tag: `Feature: research-documentation-expansion, Property 2: Mermaid diagram completeness`
- Generator: for each required diagram type from the requirements list
- Assertion: the document contains a fenced code block ` ```mermaid ` followed by content that includes the expected Mermaid diagram type keyword (`flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`)

**Property Test 3: Technical Accuracy**
Tag: `Feature: research-documentation-expansion, Property 3: Technical accuracy`
- Generator: randomly sample sentences from technical description sections (Chapters 3, 4, 5, 6)
- Assertion: no sampled sentence contains the forbidden terms ("Flask", "Django", "React", "Bootstrap", "Tailwind", "MySQL", "MongoDB") as the system's own technology

**Property Test 4: Minimum Document Length**
Tag: `Feature: research-documentation-expansion, Property 4: Minimum document length`
- Single execution (not randomised): count total words in generated document
- Assertion: `word_count >= 75000`

**Property Test 5: Algorithm Output Shape**
Tag: `Feature: research-documentation-expansion, Property 5: Algorithm output shape`
- Generator: generate random `profile_data` dicts with valid KCSE grade strings and preference fields
- Assertion: `len(result) <= 8`; all scores are integers in `[0, 100]`; if `result` is non-empty, `result[0][0] == 100`

**Property Test 6: Algorithm Filter Invariants**
Tag: `Feature: research-documentation-expansion, Property 6: Algorithm filter invariants`
- Generator: generate random `profile_data` dicts, including cases with and without `education_goal` set
- Assertion: for every `(score, career)` in result — `career['min_grade'] <= mean_grade`; if `education_goal` is non-empty, `career['level'] == education_goal`

**Property Test 7: GRADE_MAP Conversion Correctness**
Tag: `Feature: research-documentation-expansion, Property 7: GRADE_MAP conversion correctness`
- Generator: randomly sample grade strings from `GRADE_MAP` keys
- Assertion: `map_grade(grade) == GRADE_MAP[grade]`; for any career, `subject_score == sum(map_grade(user_inputs[s]) * 2 for s in career['subjects'])`

**Property Test 8: study_level Determination**
Tag: `Feature: research-documentation-expansion, Property 8: study_level determination`
- Generator: generate random float values for `mean_grade` in range [0.0, 12.0]
- Assertion: the `study_level` returned matches the threshold rules exactly — no overlap, no gap, no other values

**Property Test 9: Scholarship Search Correctness**
Tag: `Feature: research-documentation-expansion, Property 9: Scholarship search correctness`
- Generator: generate random keyword strings and a random set of scholarship records (some matching, some not)
- Assertion: every record in the search result contains the keyword (case-insensitive) in `name`, `provider`, `description`, or `eligibility_criteria`; no non-matching record appears

**Property Test 10: Scholarship Category Invariant**
Tag: `Feature: research-documentation-expansion, Property 10: Scholarship category invariant`
- Generator: randomly sample scholarship records from the database after seeding
- Assertion: every record's `category` field is one of `{"Government", "Private", "International"}`

**Property Test 11: Admin CRUD Round-Trip**
Tag: `Feature: research-documentation-expansion, Property 11: Admin CRUD round-trip`
- Generator: generate random scholarship record dicts with valid field values
- Assertion: after insert, a SELECT by name returns the record; after delete, a SELECT by id returns nothing

### Integration Tests

- **Word export compatibility** — verify the Markdown output can be parsed by `python-docx` or `pandoc` without errors, confirming it is valid for Word conversion
- **Mermaid render test** — verify each Mermaid code block renders without syntax errors using the Mermaid CLI (`mmdc`) or equivalent validator
- **Cross-reference consistency** — verify every `Figure X.Y` reference in the body text has a corresponding `Figure X.Y:` caption in the document
- **OTP flow** — integration test verifying that after registration, a 6-digit OTP is stored in `verification_tokens` with `expires_at = now + 600`, and that submitting the correct OTP sets `is_verified = 1`
- **Scholarship seed coverage** — verify that after `seed_scholarships()` runs on an empty table, records exist for all three categories (Government, Private, International)
- **Vercel configuration** — verify `vercel.json` is valid JSON and contains a rewrite rule routing all paths to `api/index.py`

### Testing Configuration

- Property tests: minimum 100 iterations per property
- Test framework: `pytest` with `hypothesis` for property tests
- Mermaid validation: `@mermaid-js/mermaid-cli` (Node.js) or equivalent
- Word count: Python `len(text.split())` on the full document string
