# Requirements Document

## Introduction

This feature covers the exhaustive expansion of the existing 46-page academic research document titled **"WEB-BASED CAREER GUIDANCE AND SCHOLARSHIP INFORMATION PORTAL: A CASE OF KENYAN FORM FOUR LEAVERS"** (Chapters 1–5) into a complete, high-quality, technically rigorous academic project document of a minimum of 150 pages, culminating in a full Chapter 6. The expansion must strictly conform to the documentation structure, formatting rules, and academic standards prescribed by the lecturer (Dr. Ishmael Nick) as documented in the `Documents/` folder. The final output is a single, cohesive `.docx`-compatible Markdown document (or structured text) that can be pasted into Microsoft Word and formatted to the required standard.

The web application already exists (Python/Flask backend, HTML/CSS/JS frontend, SQLite/PostgreSQL database) and its actual technical implementation details must be accurately reflected throughout the document — particularly in Chapters 3, 4, 5, and 6.

---

## Glossary

- **Document_Generator**: The AI system responsible for producing the expanded academic content.
- **Existing_Document**: The current 46-page `.docx` file at `Documents/WEB-BASED CAREER GUIDANCE AND SCHOLARSHIP INFORMATION PORTAL_ A CASE OF KENYAN FORM FOUR LEAVERS 4 (1).docx`.
- **Lecturer_Guide**: The collection of documents in `Documents/` (Documentation structure.docx, RESEARCH TALK-1.docx, MOD 1–4, MOD 6) that constitute the absolute source of truth for required sections, formatting, and academic standards.
- **Documentation_Structure**: The section-by-section outline extracted from `Documents/Documentation structure.docx` and `Documents/RESEARCH TALK-1.docx`.
- **Portal**: The web-based Career Guidance and Scholarship Information Portal that is the subject of the research.
- **CBC**: Competency-Based Curriculum — Kenya's current 2-6-3-3-3 educational framework.
- **KUCCPS**: Kenya Universities and Colleges Central Placement Service.
- **HELB/HEFoND**: Higher Education Loans Board / Higher Education Fund — Kenya's state student financing mechanisms.
- **RIASEC**: Holland's six personality typologies (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) used as the algorithmic basis for the career profiling module.
- **SCCT**: Social Cognitive Career Theory — theoretical framework addressing self-efficacy and outcome expectations in career choice.
- **TAM**: Technology Acceptance Model — framework for predicting user adoption based on Perceived Usefulness and Perceived Ease of Use.
- **TVET**: Technical and Vocational Education and Training institutions.
- **ERD**: Entity-Relationship Diagram — a database design artifact showing entities and their relationships.
- **UML**: Unified Modeling Language — the standard notation for software design diagrams.
- **Mermaid_Diagram**: A text-based diagramming syntax that renders UML and other diagrams in Markdown-compatible environments.
- **SDLC**: Software Development Life Cycle.
- **Agile_Scrum**: The iterative software development methodology used in this project.
- **UAT**: User Acceptance Testing.
- **DFD**: Data Flow Diagram.
- **KCSE**: Kenya Certificate of Secondary Education — the national secondary school exit examination.
- **NG-CDF**: National Government Constituency Development Fund — a source of localized bursaries.
- **MTI**: Means Testing Instrument — the algorithm used by HEFoND to categorize students into funding bands.
- **Funding_Repository**: The centralised scholarships table and associated admin dashboard that aggregates HEFoND, NG-CDF, private foundation, and international scholarship records.
- **Career_Profiling_Module**: The four-step algorithmic workflow (Steps 1–4) that collects KCSE grades, skill ratings, and preferences and passes them to `run_algorithm()` to produce ranked career recommendations.
- **run_algorithm**: The Python function in `api/index.py` that implements the weighted scoring algorithm, returning a ranked list of up to eight career pathways with percentage match scores.
- **CAREERS**: The static career database defined in `api/career_database.py`, containing career entries across six domains with associated grade thresholds, subject weights, trait scores, and industry tags.
- **SUS**: System Usability Scale — a standardised 10-item usability evaluation instrument; scores ≥68 indicate above-average usability and scores ≥80.3 indicate excellent usability.
- **KII**: Key Informant Interview — a semi-structured qualitative data collection method used with career counselors to evaluate the current manual guidance system.

---

## Requirements

### Requirement 1: Preliminary Pages Completeness

**User Story:** As a student researcher, I want all preliminary pages to be fully written and correctly formatted, so that the document meets the university's submission standards before the main chapters begin.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce a complete Abstract that is one paragraph, single-spaced, italicized, Times New Roman size 12, between 150 and 300 words, and contains: the research title, the research problem and objectives, the methodology (mixed-methods + Agile Scrum), the frontend and backend technologies (Pure Python, Vanilla HTML5/CSS3/JS, SQLite/PostgreSQL), the key results, and the conclusion.
2. THE Document_Generator SHALL produce a Table of Contents listing all chapters, sections, and sub-sections with correct heading numbers and page number placeholders.
3. THE Document_Generator SHALL produce a List of Figures and a List of Tables, each referencing all figures and tables in the document with their captions and page number placeholders.
4. THE Document_Generator SHALL produce a Definition of Key Terms section containing at minimum the terms: CBC, KUCCPS, Form Four Leavers, Career Guidance, Scholarship Portal, NEET, TVET, HELB/HEFoND, Educational Pathways, RIASEC, TAM, SCCT, and MTI.
5. THE Document_Generator SHALL produce a Declaration and Approval page with the correct student name (IGNATIUS ETHENS CIT-221-048/2022), supervisor name (DR. ISHMAEL NICK), and Faculty of Computing and Information Technology, with all three approvals (Student, University Supervisor, Head of Department) on one page.
6. THE Document_Generator SHALL produce Acknowledgement and Dedication sections consistent with the existing document content.

---

### Requirement 2: Chapter One — Expanded Introduction

**User Story:** As a student researcher, I want Chapter One to be deeply expanded with rich academic prose, so that it provides a thorough, well-justified foundation for the entire research project.

#### Acceptance Criteria

1. THE Document_Generator SHALL expand Section 1.1 (Chapter Introduction) to a minimum of one full page, explicitly listing all sub-sections of the chapter.
2. THE Document_Generator SHALL expand Section 1.2 (Motivation and Background) to a minimum of one and a half pages, written in first-person narrative, explaining the personal and societal motivations for the research.
3. THE Document_Generator SHALL expand Section 1.3 (Background of the Study) to a minimum of three pages, covering: the global context of education-to-employment transitions, the Kenyan 7-4-2-3 system, the 8-4-4 system and its limitations, the CBC paradigm shift, the scholarship financing landscape (HELB/HEFoND, MTI, NG-CDF), and the information asymmetry problem.
4. THE Document_Generator SHALL expand Section 1.4 (Problem Statement) to a minimum of one full page, written in continuous prose (not bullets), addressing the five Ws (who, what, where, when, why), and citing at least two supporting references.
5. THE Document_Generator SHALL expand Section 1.5 (Aim of the Research) to a clear, single broad statement using action-verb language, not exceeding one paragraph.
6. THE Document_Generator SHALL expand Section 1.6 (Objectives of the Research) to include one main objective (restating the research title) and three to four SMART specific objectives written as functional system specifications, avoiding non-functional terms like "user-friendly" or "efficient."
7. THE Document_Generator SHALL expand Section 1.7 (Justification of Research) to a minimum of one and a half pages, anchored on existing published research (not assumptions), covering: policy alignment with CBC, educational equity, economic optimization, and technological advancement.
8. THE Document_Generator SHALL expand Section 1.8 (Scope of Research) to specify the target organization (selected Nairobi and peri-urban secondary schools), the features to be implemented by the proposed system, and the explicit limitations (no live KUCCPS API integration, no clinical psychometric replacement, internet dependency).
9. THE Document_Generator SHALL produce Section 1.9 (Research Organization) describing all seven chapters in one paragraph each.
10. THE Document_Generator SHALL produce Section 1.10 (Chapter Summary) as a concise paragraph summarizing the key points established in Chapter One.

---

### Requirement 3: Chapter Two — Exhaustive Literature Review

**User Story:** As a student researcher, I want Chapter Two to be a deeply critical, well-structured literature review, so that it demonstrates mastery of the research domain and clearly establishes the research gap.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 2.1 (Chapter Introduction) listing all sub-sections of the chapter.
2. THE Document_Generator SHALL produce Section 2.2 (Theoretical Framework) with a minimum of three full pages covering: Holland's RIASEC Model (with explicit mapping to CBC pathways), Social Cognitive Career Theory (SCCT) with application to Kenyan socio-economic context, and the Technology Acceptance Model (TAM) with application to low-bandwidth mobile-first design.
3. THE Document_Generator SHALL produce Section 2.3 (History of the Research Topic) with a minimum of three pages tracing the chronological evolution of career guidance in Kenya from the post-independence 7-4-2-3 era through the 8-4-4 system to the CBC paradigm shift.
4. THE Document_Generator SHALL produce Section 2.4 (The Scholarship and Tertiary Financing Landscape) with a minimum of one and a half pages covering the HEF model, MTI bands, HELB/HEFoND, Equity Wings to Fly, KCB Foundation, and NG-CDF bursaries.
5. THE Document_Generator SHALL produce Section 2.5 (Review of Related Prototypes and Systems) covering at minimum three systems: one global (Naviance), one local government (KUCCPS Portal), and one local commercial (Craydel), each reviewed for Core Features, Strengths, and Limitations, with a comparative analysis table (Table 2.1).
6. THE Document_Generator SHALL produce Section 2.6 (Emerging Trends and Patterns) with a minimum of two pages covering: AI-driven personalization and machine learning in EdTech, the "One-Stop Shop" integration of financial aid with academic guidance, mobile-first and Progressive Web App (PWA) architecture in Sub-Saharan Africa, and data privacy considerations.
7. THE Document_Generator SHALL produce Section 2.7 (Research Gap) with a minimum of one and a half pages explicitly identifying and justifying three gaps: the Contextual Gap (CBC alignment), the Integration Gap (Diagnostic + Enabler paradigm), and the Accessibility Gap (free, lightweight, rural-accessible).
8. THE Document_Generator SHALL produce Section 2.8 (Chapter Summary) as a concise paragraph synthesizing the chapter's key findings and linking them to Chapter Three.
9. WHEN a claim or theory is stated in Chapter Two, THE Document_Generator SHALL include an in-text citation in APA format for every paragraph.

---

### Requirement 4: Chapter Three — Comprehensive Research Methodology

**User Story:** As a student researcher, I want Chapter Three to exhaustively document every methodological decision, so that the research is reproducible, academically rigorous, and aligned with the lecturer's prescribed structure.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 3.1 (Chapter Introduction) listing all sub-sections of the chapter.
2. THE Document_Generator SHALL produce Section 3.2 (Methodology for Literature Review) explaining the mixed-methods research design rationale, the six generic steps of a literature review (formulating questions, searching, screening, quality assessment, data extraction, analysis), and the specific databases and search terms used.
3. THE Document_Generator SHALL produce Section 3.3 (Methodology for Requirement Specification, Data Collection and Analysis) covering: Requirement Specification definition, the mixed-methods design, Target Population (Form Four students aged 16–21, career counselors, IT administrators), Stratified Random Sampling for students across National/Extra-County/Sub-County/Private schools in Nairobi and environs, Purposive Sampling for 15–20 counselors, semi-structured Key Informant Interviews (45-minute sessions), highly structured digital questionnaires (Google Forms with conditional logic), and exhaustive document analysis (KUCCPS matrices, HELB MTI logic).
4. THE Document_Generator SHALL produce Section 3.4 (Methodology for System Analysis — Current System) covering: the definition of System Analysis, Context Diagram description for the current analog guidance system, DFD description for the current system, and Flowchart description for the current manual process.
5. THE Document_Generator SHALL produce Section 3.5 (Methodology for System Design — Proposed System) covering: System Design definition, DFDs for the proposed system, Flowcharts for the recommendation engine logic, Sequence Diagrams (at least four scenarios), Collaboration Diagrams, Use Case Diagrams (three actors: Learner, Counselor, Admin), Pseudocodes for the career matching algorithm, Early System Prototypes (I/O design), UI Design principles (mobile-first, responsive), and Database Design (ERD, normalization to 3NF, data dictionary).
6. THE Document_Generator SHALL produce Section 3.6 (Methodology for System Implementation) covering: the Agile Scrum framework with Sprint structure, Pure Python backend (http.server, cgi, json, hashlib), Vanilla HTML5/CSS3/JavaScript (ES6+) frontend, SQLite (development) and PostgreSQL/Neon (production) database, and the pg8000 library for PostgreSQL connectivity.
7. THE Document_Generator SHALL produce Section 3.7 (Methodology for System Testing) covering: the Testing Plan definition, Functional vs. Non-Functional requirements distinction, Unit Testing, Integration Testing, System/Performance Testing, and User Acceptance Testing (UAT) using the System Usability Scale (SUS).
8. THE Document_Generator SHALL produce Section 3.8 (Methodology for System Deployment) covering: the deployment pipeline (coding, building, testing, packaging, releasing, configuring, monitoring), local SQLite development environment, and cloud deployment to Vercel (as evidenced by `vercel.json` in the project).
9. THE Document_Generator SHALL produce Section 3.9 (Chapter Summary) as a concise paragraph.

---

### Requirement 5: Chapter Four — System Analysis of the Current System

**User Story:** As a student researcher, I want Chapter Four to provide a thorough diagnostic of the current (pre-portal) system, so that the necessity and design of the proposed system is fully justified.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 4.1 (Chapter Introduction) listing all sub-sections.
2. THE Document_Generator SHALL produce Section 4.2 (Description of the Current System) covering the manual, fragmented career guidance process in Kenyan secondary schools, including its strengths (human empathy, contextual knowledge) and weaknesses (low counselor-to-student ratio, lack of data-driven tools, geographic inequality, scholarship information silos).
3. THE Document_Generator SHALL produce Section 4.3 (Feasibility Study and Conclusion) covering: Technical Feasibility (Python, SQLite/PostgreSQL, HTML/CSS/JS are proven, accessible technologies), Economic Feasibility (open-source stack, free Vercel hosting tier, no licensing costs), Operational Feasibility (mobile-first design for low-bandwidth environments), and a clear feasibility conclusion.
4. THE Document_Generator SHALL produce Section 4.4 (Data I/O Analysis) covering: data captured by the current system (KCSE grades, counselor notes, printed booklets), relationships between data entities, and outputs from the current system (verbal advice, printed career booklets).
5. THE Document_Generator SHALL produce Section 4.5 (Process Logic Design of the Current System) including: a Context Diagram (described in text and rendered as a Mermaid.js diagram) showing the student, counselor, KUCCPS, and scholarship bodies as external entities, a Level-0 DFD (described in text), and a Flowchart (described in text and rendered as a Mermaid.js diagram) of the current manual guidance process.
6. THE Document_Generator SHALL produce Section 4.6 (Chapter Summary) as a concise paragraph.

---

### Requirement 6: Chapter Five — System Design of the Proposed System

**User Story:** As a student researcher, I want Chapter Five to contain exhaustive, technically precise UML diagrams and database design artifacts, so that the proposed system's architecture is fully documented to a professional standard.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 5.1 (Introduction) listing all sub-sections.
2. THE Document_Generator SHALL produce Section 5.2 (Description of the Proposed System) covering its strengths (centralized, CBC-aligned, free, mobile-first, integrated diagnostic + enabler) and weaknesses/limitations (internet dependency, no live KUCCPS API, psychometric limitations).
3. THE Document_Generator SHALL produce Section 5.3 (Requirement Analysis) covering: Functional Requirements (user registration/login, email OTP verification, multi-step career profiling, algorithmic recommendation engine, scholarship repository with search, admin dashboard, counselor dashboard), Non-Functional Requirements (page load under 3G, mobile-first responsive design, SHA-256 password hashing, session management), User Requirements, and Usability Requirements.
4. THE Document_Generator SHALL produce Section 5.4 (Conceptual Architecture) describing the three-tier architecture (Presentation Layer: HTML/CSS/JS; Application Layer: Pure Python http.server; Data Layer: SQLite/PostgreSQL) and rendered as a Mermaid.js System Architecture Diagram.
5. THE Document_Generator SHALL produce Section 5.5 (Process Logic Design of the Proposed System) including:
   - A Use Case Diagram (Mermaid.js) showing three actors (Learner, Counselor, Admin) and all use cases.
   - An Activity Diagram (Mermaid.js) for the career profiling workflow (Steps 1–4).
   - Four Sequence Diagrams (Mermaid.js), one each for: (a) User Registration with OTP Email Verification, (b) Multi-Step Career Profiling and Algorithm Execution, (c) Scholarship Search and Retrieval, (d) Admin Adding/Deleting a Scholarship.
   - A Class Diagram (Mermaid.js) showing the main classes: handler, PortalRequestHandler, and their key methods.
   - A Collaboration Diagram description for the scholarship matching process.
   - A Context Diagram (Mermaid.js) for the proposed system.
   - A Level-0 DFD (Mermaid.js) for the proposed system.
   - Pseudocode for the `run_algorithm()` career matching function.
6. THE Document_Generator SHALL produce Section 5.6 (Database Design) including:
   - A detailed Entity-Relationship Diagram (ERD) rendered as a Mermaid.js `erDiagram`, showing entities: Users, Sessions, Verification_Tokens, Scholarships, and their attributes and relationships.
   - Normalization discussion (1NF, 2NF, 3NF).
   - A Data Dictionary table for each entity (Users, Sessions, Verification_Tokens, Scholarships) listing field name, data type, constraints, and description.
7. THE Document_Generator SHALL produce Section 5.7 (I/O Design of the Proposed System) describing at minimum four key screens: the Landing Page, the Multi-Step Career Profiling Form, the Recommendations Page, and the Scholarships Page, with mock-up descriptions.
8. THE Document_Generator SHALL produce Section 5.8 (Chapter Summary) as a concise paragraph.
9. WHEN a Mermaid.js diagram is produced, THE Document_Generator SHALL wrap it in a fenced code block with the `mermaid` language tag so it renders correctly in Markdown-compatible environments.

---

### Requirement 7: Chapter Six — System Implementation and Testing

**User Story:** As a student researcher, I want Chapter Six to document the actual implemented system with screenshots, a testing plan, and evaluation results, so that the project demonstrates a complete software engineering lifecycle.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 6.1 (Chapter Introduction) listing all sub-sections.
2. THE Document_Generator SHALL produce Section 6.2 (System Screenshots) with descriptions of at most four key system screenshots: (a) the Home/Landing Page, (b) the Career Profiling Step 1 (Academic Grades), (c) the Recommendations Page, and (d) the Scholarships Page, each with a figure caption (e.g., Figure 6.1: Home Page of the Career Guidance Portal).
3. THE Document_Generator SHALL produce Section 6.3 (Testing Plan) as a structured table covering: Test ID, Module Under Test, Test Description, Test Input, Expected Output, Actual Output, and Pass/Fail status, for a minimum of ten test cases covering: user registration, OTP verification, login with valid credentials, login with invalid credentials, profile step 1 submission, profile step 2 submission, profile step 3 submission, algorithm execution with STEM profile, scholarship search with keyword, and admin scholarship addition.
4. THE Document_Generator SHALL produce Section 6.4 (Evaluation Plan) covering: the UAT methodology using the System Usability Scale (SUS), the pilot group composition (Form Four students and counselors), the SUS questionnaire items, and a discussion of expected usability scores and their interpretation.
5. THE Document_Generator SHALL produce Section 6.5 (Chapter Summary) as a concise paragraph.

---

### Requirement 7b: Chapter Seven — Conclusions, Findings and Recommendations

**User Story:** As a student researcher, I want Chapter Seven to synthesise the entire research project with conclusions, findings, challenges, and future recommendations, so that the document has a proper academic closing chapter as required by the lecturer's documentation structure.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 7.1 (Introduction) listing all sub-sections of Chapter Seven.
2. THE Document_Generator SHALL produce Section 7.2 (Conclusion) of at least two pages, summarising the key findings of the research, confirming that the research aim and objectives stated in Chapter One have been achieved, and reflecting on the significance of the portal as a contribution to educational technology in Kenya.
3. THE Document_Generator SHALL produce Section 7.3 (Challenges Encountered) of at least one page, documenting the technical, methodological, and contextual challenges encountered during the research and development process, and explaining how each challenge was addressed.
4. THE Document_Generator SHALL produce Section 7.4 (Future Recommendations) of at least one page, proposing specific, actionable enhancements to the portal and the research that could be pursued in future work, including live KUCCPS API integration, Kiswahili localisation, PWA offline mode, and machine learning enhancements to the recommendation engine.
5. THE Document_Generator SHALL produce Section 7.5 (Chapter Conclusion) as a concise closing paragraph that brings the entire research document to a formal close.

---

### Requirement 8: References and Appendices

**User Story:** As a student researcher, I want a complete References section and relevant Appendices, so that the document is academically credible and complete.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce a References/Bibliography section with a minimum of 20 references in APA format, covering: Holland (1997), Davis (1989) TAM, Lent et al. (1994) SCCT, Kenya Ministry of Education CBC policy documents, KUCCPS annual reports, Naviance product documentation, and relevant peer-reviewed journal articles on EdTech in Sub-Saharan Africa.
2. THE Document_Generator SHALL produce an Appendix section containing: a sample student questionnaire (minimum 15 questions), a sample Key Informant Interview guide (minimum 8 questions for counselors), and a budget/time schedule table.
3. WHEN a reference is cited in the body of the document, THE Document_Generator SHALL use APA in-text citation format (Author, Year) consistently throughout.

---

### Requirement 11: Centralized Funding Repository

**User Story:** As a Form Four leaver, I want a searchable database of scholarship and bursary opportunities — including HEFoND, NG-CDF, and private foundation awards — so that I can discover and compare funding options relevant to my circumstances from a single platform.

#### Acceptance Criteria

1. THE Portal SHALL maintain a centralised scholarships table in the relational database containing records for at minimum the following funding categories: Government (HEFoND, NG-CDF, HELB, Presidential Scholarship, County CDF), Private Foundation (Equity Wings to Fly, KCB Foundation, Safaricom Foundation), and International (Mastercard Foundation Scholars Program, USAID Kenya).
2. WHEN a user submits a keyword search on the scholarships page, THE Portal SHALL query the scholarships table using a case-insensitive LIKE match against the name, provider, description, and eligibility_criteria fields and return all matching records within 3 seconds.
3. THE Portal SHALL display each scholarship record with the following fields visible to the user: name, provider, description, eligibility criteria, application deadline, funding amount, and an external application link.
4. THE Portal SHALL categorise each scholarship record under exactly one of the following categories: Government, Private, or International, and THE Portal SHALL allow users to filter the displayed list by category.
5. THE Document_Generator SHALL produce a dedicated sub-section within Section 2.4 (Scholarship and Tertiary Financing Landscape) that describes the HEFoND funding model (including MTI bands and the scholarship-to-loan ratio), the NG-CDF constituency-level bursary disbursement mechanism, and at least three named private foundation scholarships, with APA citations for each funding body.
6. THE Document_Generator SHALL produce a sub-section within Section 5.3 (Requirement Analysis) that lists the scholarship repository as a functional requirement, specifying the searchable fields, the category filter, and the administrative CRUD operations (Create, Read, Update, Delete) available through the admin dashboard.
7. WHEN an administrator accesses the admin dashboard, THE Portal SHALL present a scholarship management interface that allows the administrator to add a new scholarship record, edit an existing record, and delete a record, with each operation persisted immediately to the database.
8. IF a scholarship search returns zero results, THEN THE Portal SHALL display a descriptive message informing the user that no matching scholarships were found and suggesting alternative search terms.
9. THE Document_Generator SHALL include Table 5.4 (Data Dictionary: scholarships table) in Section 5.6, listing all fields — id, name, provider, description, eligibility_criteria, deadline, link, category, amount — with their data types, constraints, and descriptions as implemented in `api/index.py`.

---

### Requirement 12: System Validation and Deployment

**User Story:** As a student researcher, I want the portal to be deployed as a publicly accessible web-based system and evaluated for core functionalities — including OTP verification and career profiling — with user experience measured via the System Usability Scale (SUS), so that the research demonstrates a complete software engineering lifecycle from implementation through validated deployment.

#### Acceptance Criteria

1. THE Portal SHALL be deployed to the Vercel cloud platform using the configuration defined in `vercel.json`, making the system accessible via a public HTTPS URL without requiring local installation.
2. WHEN a new user completes the registration form, THE Portal SHALL generate a 6-digit OTP, store it in the verification_tokens table with a 600-second expiry, and transmit it to the user's registered email address via Gmail SMTP on port 465 (SSL), all within 30 seconds of form submission.
3. WHEN a user submits a valid OTP on the verification page within the 10-minute window, THE Portal SHALL set the user's is_verified flag to 1 in the users table and redirect the user to the login page.
4. IF a user submits an OTP that has expired or does not match the stored token, THEN THE Portal SHALL display a descriptive error message and provide a resend option without invalidating the user's account.
5. THE Portal SHALL complete the full four-step career profiling workflow — Step 1 (Academic Grades), Step 2 (Skills and Aptitude), Step 3 (Preferences), Step 4 (Final Review) — and execute the `run_algorithm()` function to produce a ranked list of career recommendations upon submission of Step 4.
6. THE Document_Generator SHALL produce Section 6.3 (Testing Plan) as a structured table with a minimum of ten test cases, each covering: Test ID, Module Under Test, Test Description, Test Input, Expected Output, Actual Output, and Pass/Fail status, including test cases for OTP generation, OTP verification with valid code, OTP rejection with expired code, and full profiling workflow execution.
7. THE Document_Generator SHALL produce Section 6.4 (Evaluation Plan) describing the UAT methodology using the System Usability Scale (SUS), specifying: the pilot group composition (minimum 10 Form Four students and 5 career counselors from Nairobi-based schools), all 10 standard SUS questionnaire items, the SUS scoring formula (sum of converted scores × 2.5), and the interpretation of scores (≥68 = above average usability, ≥80.3 = excellent usability).
8. THE Document_Generator SHALL produce Section 3.8 (Methodology for System Deployment) describing the full deployment pipeline — coding, building, testing, packaging, releasing, configuring, and monitoring — and explicitly documenting the Vercel deployment configuration, the SQLite-to-PostgreSQL migration path, and the environment variables required for production (Careerdatabase_URL, careerapp_gmail, careerapps_password).
9. WHERE the SUS evaluation is conducted, THE Document_Generator SHALL present the expected or actual SUS score results in Section 6.4, interpret the score against the Bangor et al. (2008) adjective rating scale, and discuss implications for the portal's usability in low-bandwidth Kenyan school environments.

---

### Requirement 13: Baseline System Analysis

**User Story:** As a student researcher, I want a documented evaluation of the existing manual career guidance and scholarship dissemination methods used in Nairobi-based secondary schools, so that the data flow gaps and process limitations of the current system are formally identified and used to justify the design of the proposed portal.

#### Acceptance Criteria

1. THE Document_Generator SHALL produce Section 4.2 (Description of the Current System) of at minimum two pages, describing the manual, fragmented career guidance process in Nairobi and peri-urban secondary schools, including: the role of the career counselor, the use of printed KUCCPS booklets and verbal advice, the absence of digital tools, and the low counselor-to-student ratio.
2. THE Document_Generator SHALL identify and document at minimum four specific weaknesses of the current manual system in Section 4.2: (a) geographic inequality in access to career information, (b) scholarship information silos with no centralised repository, (c) absence of data-driven or algorithmic career matching, and (d) dependence on individual counselor knowledge with no standardised process.
3. THE Document_Generator SHALL produce Section 4.4 (Data I/O Analysis) documenting: the data inputs captured by the current system (KCSE grade slips, counselor notes, printed booklets), the relationships between data entities (student, counselor, KUCCPS, scholarship bodies), and the outputs of the current system (verbal career advice, printed referral letters, scholarship application forms).
4. THE Document_Generator SHALL produce Section 4.5 (Process Logic Design of the Current System) including a Context Diagram rendered as a Mermaid.js `flowchart LR` diagram showing the student, counselor, KUCCPS, and scholarship bodies as external entities, a Level-0 DFD rendered as a Mermaid.js `flowchart TD` diagram, and a Flowchart of the current manual guidance process rendered as a Mermaid.js `flowchart TD` diagram.
5. THE Document_Generator SHALL produce Section 3.3 (Methodology for Requirement Specification, Data Collection and Analysis) documenting the data collection instruments used to evaluate the current system: structured digital questionnaires administered to Form Four students via Google Forms, semi-structured Key Informant Interviews (KIIs) of 45-minute duration conducted with 15–20 career counselors using purposive sampling, and document analysis of KUCCPS placement matrices and HELB/HEFoND MTI logic.
6. THE Document_Generator SHALL produce Section 3.4 (Methodology for System Analysis — Current System) defining System Analysis, describing the Context Diagram methodology, the DFD methodology, and the Flowchart methodology as applied to the current manual guidance system.
7. WHEN describing the target population in Section 3.3, THE Document_Generator SHALL specify the stratified random sampling strategy across four school strata in Nairobi and environs: National schools, Extra-County schools, Sub-County schools, and Private schools, with a justification for the stratum boundaries.
8. THE Document_Generator SHALL produce Section 4.3 (Feasibility Study and Conclusion) covering Technical Feasibility (Python, SQLite/PostgreSQL, HTML/CSS/JS are proven, accessible technologies with no licensing cost), Economic Feasibility (open-source stack, free Vercel hosting tier), and Operational Feasibility (mobile-first design for low-bandwidth environments), concluding with a clear feasibility determination.
9. THE Document_Generator SHALL produce Section 1.4 (Problem Statement) of at minimum one full page in continuous prose (not bullet points), addressing the five Ws — who (Form Four leavers in Nairobi-based schools), what (absence of an integrated digital career guidance and scholarship platform), where (Nairobi and peri-urban secondary schools), when (at the point of KCSE completion and post-secondary transition), why (information asymmetry and fragmented manual processes) — and citing at least two supporting references.

---

### Requirement 14: Automated Career Profiling

**User Story:** As a Form Four leaver, I want an algorithmic module that processes my KCSE grades, self-rated skills, and personal preferences to generate a ranked list of career pathway recommendations with percentage match scores, so that I can make an informed, data-driven decision about my post-secondary education and career direction.

#### Acceptance Criteria

1. THE Portal SHALL implement the `run_algorithm(profile_data)` function that accepts a profile data dictionary assembled from the four-step profiling workflow and returns a ranked list of at most eight career recommendations, each annotated with a percentage match score between 0 and 100.
2. WHEN computing career scores, THE Portal SHALL apply the GRADE_MAP (A=12, A-=11, B+=10, B=9, B-=8, C+=7, C=6, C-=5, D+=4, D=3, D-=2, E=1, blank=0) to convert each KCSE grade string to a numeric value, multiply each subject grade value by 2 to produce the subject_score component, and sum trait_score and industry_score components as defined in the CAREERS database.
3. THE Portal SHALL normalise all career scores relative to the highest-scoring career in the filtered result set, such that the top-ranked career always receives a 100% match score and all other careers receive proportionally lower scores.
4. WHEN a user's mean grade across the seven profiling subjects is below a career's min_grade threshold, THE Portal SHALL exclude that career from the recommendation results entirely.
5. WHERE a user has specified an education_goal (Degree, Diploma, Certificate, or Artisan), THE Portal SHALL filter the recommendation results to include only careers whose level field matches the specified education_goal.
6. THE Portal SHALL determine the user's study_level from their mean grade: mean_grade ≥ 7.0 maps to "University / Graduate", ≥ 5.0 maps to "Diploma / TVET", ≥ 3.0 maps to "Certificate", and below 3.0 maps to "Artisan", and THE Portal SHALL display this study_level on the recommendations page alongside the ranked career list.
7. THE Document_Generator SHALL produce pseudocode for the `run_algorithm()` function in Section 5.5, accurately representing the five computational steps: (a) grade mapping via GRADE_MAP, (b) mean grade computation and study_level determination, (c) career filtering by education_goal and min_grade, (d) score computation (subject_score + trait_score + industry_score), and (e) normalisation to percentage match.
8. THE Document_Generator SHALL produce a dedicated sub-section within Section 5.3 (Requirement Analysis) listing the career profiling module as a functional requirement, specifying the four profiling steps, the seven KCSE subjects collected in Step 1, the six skill ratings collected in Step 2, and the preference fields collected in Step 3 (work_environment, industry_interests, motivation, relocate, budget, education_goal).
9. THE Document_Generator SHALL produce Section 5.5 Activity Diagram (Mermaid.js `flowchart TD`) for the multi-step career profiling workflow, showing the sequential flow from Step 1 through Step 4, the cookie-based state accumulation between steps, the algorithm execution on submission, and the rendering of the recommendations page.
10. IF the `run_algorithm()` function produces zero matching careers after applying all filters, THEN THE Portal SHALL display a message informing the user that no careers matched their current profile and suggesting they broaden their education_goal filter or revisit their grade entries.
11. THE Document_Generator SHALL accurately describe the CAREERS database in `api/career_database.py` in Section 5.3, noting that it contains entries across six domains — Health Sciences, Engineering and Technology, Business and Economics, Arts Media and Law, Agriculture and Environment, and Education and Social Sciences — and that each entry specifies a name, level, min_grade, subjects list, industries list, and traits dictionary.

---

### Requirement 9: Formatting and Academic Standards

**User Story:** As a student researcher, I want the entire document to conform to the lecturer's strict formatting requirements, so that it is not penalized for non-compliance.

#### Acceptance Criteria

1. THE Document_Generator SHALL format all body paragraphs as justified, 1.5-spaced, Times New Roman, size 12.
2. THE Document_Generator SHALL format the Abstract as single-spaced, italicized, Times New Roman, size 12.
3. THE Document_Generator SHALL number preliminary pages in Roman lower-case numerals (i, ii, iii…) centered at the bottom.
4. THE Document_Generator SHALL number main chapter pages in Arabic numerals (1, 2, 3…) centered at the bottom.
5. THE Document_Generator SHALL label all figures with a caption below in the format "Figure X.Y: [Description]" and all tables with a caption above in the format "Table X.Y: [Description]".
6. THE Document_Generator SHALL ensure the Blank Page and Cover Page carry no page numbers.
7. THE Document_Generator SHALL ensure the Problem Statement is written in continuous prose, not bullet points.
8. THE Document_Generator SHALL ensure the Research Justification is anchored on existing published research, not assumptions.
9. THE Document_Generator SHALL ensure the Research Scope specifies the target organization and the features to be implemented by the proposed system.
10. THE Document_Generator SHALL ensure each paragraph contains at least one in-text citation where a theory, claim, or external fact is stated.
11. THE Document_Generator SHALL ensure the total expanded document content is sufficient to produce a minimum of 150 pages when formatted in Microsoft Word at the specified formatting standards.

---

### Requirement 10: Technical Accuracy to the Actual Codebase

**User Story:** As a student researcher, I want all technical descriptions in the document to accurately reflect the actual implemented system, so that the document is not contradicted by the code.

#### Acceptance Criteria

1. THE Document_Generator SHALL accurately describe the backend as Pure Python using the built-in `http.server` module, `sqlite3`, `hashlib` (SHA-256), `uuid`, `smtplib`, and `json` — not Django, Flask, or Laravel.
2. THE Document_Generator SHALL accurately describe the frontend as Vanilla HTML5, raw CSS3, and pure JavaScript (ES6+) — not React, Vue, Bootstrap, or Tailwind.
3. THE Document_Generator SHALL accurately describe the database as SQLite for local development and PostgreSQL (via Neon cloud, using the `pg8000` library) for production deployment.
4. THE Document_Generator SHALL accurately describe the deployment platform as Vercel (as evidenced by `vercel.json`).
5. THE Document_Generator SHALL accurately describe the career recommendation algorithm as a weighted scoring system that combines: subject grade scores (mapped via GRADE_MAP A=12 to E=1), trait/personality scores, and industry interest scores, normalized to a percentage match out of the top result.
6. THE Document_Generator SHALL accurately describe the database schema as containing four tables: `users` (id, full_name, email, password, role, school, phone, study_areas, is_verified, created_at, profile_data, last_results), `sessions` (session_id, user_id, created_at), `verification_tokens` (token, user_id, expires_at), and `scholarships` (id, name, provider, description, eligibility_criteria, deadline, link).
7. THE Document_Generator SHALL accurately describe the multi-step profiling flow as four steps: Step 1 (Academic Grades: Math, English, Kiswahili, Biology, Chemistry, Physics, Humanities), Step 2 (Skills and Aptitude: analytical, coding, verbal, critical, creative, leadership ratings), Step 3 (Preferences: work environment, industry interests, activities, motivation, relocation, budget), Step 4 (Final Review and Submission).
8. THE Document_Generator SHALL accurately describe the email verification system as a 6-digit OTP sent via Gmail SMTP (smtplib, port 465 SSL), stored in the `verification_tokens` table with a 10-minute expiry.
