# InsightCX — Frontend Project Instructions
## Project
InsightCX is an AI-powered Voice of Customer analytics platform that turns customer feedback into actionable business insights.


Core philosophy:
> What is happening, why is it happening, what does it mean for the business, and what should happen next?


The backend is a working MVP. The goal is a modern React frontend that preserves existing functionality.


## Technology
Backend: Python, Flask, SQLAlchemy, OpenAI Responses API, existing database/models, AI analysis and executive insight services, benchmark/model-comparison functionality, and existing HTML/CSS MVP frontend.
Frontend: React.


Inspect the repository and verify the actual structure and capabilities before making architectural decisions.


## Critical Backend Protection
The Flask backend is the source of truth and is READ-ONLY unless explicitly instructed otherwise.


Do not:
- modify backend logic, business rules, models, database, AI/OpenAI services, analysis schemas, or benchmark logic
- introduce a second database such as Supabase/Firebase
- move, rename, or delete backend files
- silently create new backend API requirements


If frontend functionality is not currently supported:
1. Identify the gap.
2. Explain the required backend capability.
3. Prefer realistic mock/demo frontend state where appropriate.
4. Wait for explicit approval before changing backend code.


The frontend must call the backend, not OpenAI directly. Never expose API keys, secrets, database credentials, or server-side environment variables.


## Development Philosophy
Inspect before changing. Understand existing code before proposing replacements.


Make small, focused changes. Avoid unrelated refactoring and broad architectural changes. Preserve working functionality.


Prefer reusable components and clear separation between frontend presentation, data access, and business logic. Do not recreate backend business logic in React.


For substantial changes, explain the proposed approach before implementing unless immediate implementation is explicitly requested.


Run relevant checks after meaningful changes and fix errors before moving on.


## Frontend Architecture
Build a modular React application with clear separation between:
- pages and layouts
- reusable UI components
- feature-specific components
- API/service functions
- data/state handling
- design-system components


Prefer reusable patterns for cards, buttons, badges, metrics, tables, filters, tabs, dialogs, loading/error states, and confirmations.


Structure the frontend so existing Flask functionality can be connected with minimal restructuring.


## Application Areas
Top-level navigation:
1. Executive Brief
2. Feedback Explorer
3. Upload
4. AI Evaluation
5. Administration


These should feel like one cohesive application while having different UX priorities.


### AI Evaluation
AI Evaluation is one unified frontend experience for evaluating AI analysis quality. It combines the existing:
- Prompt Testing
- Benchmark Lab
- Model Comparison


Do not present these as unrelated top-level application areas.


The experience should support:
**Test → Compare → Benchmark → Evaluate**


Preserve existing backend capabilities and evaluation logic. Do not invent new evaluation logic.


### Executive vs. Technical UX
Executive-facing areas prioritize business interpretation, clarity, impact, recommendations, evidence, and concise language.


AI Evaluation and Administration may expose model names, prompt versions, configuration, evaluation metrics, benchmark results, and technical metadata.


## Existing Concepts to Preserve
Preserve relevant existing terminology and functionality:
Customer Health, Executive Summary, Business Impact, Key Metrics, Business Drivers/Top Themes, Sentiment, Emotion, Customer Intent, Priority, Confidence, Reason Codes, Leadership Priorities, Recommended Actions, Trends, Customer Evidence, AI-generated summaries, model/prompt configuration, benchmark evaluation, and Current vs. New Analysis comparison.


Use existing backend code/models as the source of truth for exact fields and capabilities.


## Administration
Provide a professional settings console covering existing:
- Feedback Analysis configuration
- Executive Analysis configuration
- Executive Summary Generation
- Maintenance
- Danger Zone


Preserve existing model, prompt, temperature, release-note, generation, and maintenance functionality.


Destructive operations always require confirmation UI.


## Upload
Preferred flow where supported:
**Select → Validate → Preview → Import → Confirmation**


Existing fields:
customer_name, customer_id, order_number, comment, survey_type, survey_score, source, survey_date.


Maximum records: 5,000.


Do not modify the CSV importer to make the frontend workflow possible.


## Accessibility & Responsiveness
Support desktop, laptop, tablet, and smaller screens where practical; prioritize desktop.


Use semantic HTML, accessible labels, visible focus states, sufficient contrast, keyboard-accessible controls, and meaningful loading/error states.


## Design Reference
`DESIGN.md` contains the detailed visual and UX specification. Consult it before substantial visual or UX changes.


Rules hierarchy:
**CLAUDE.md → DESIGN.md → existing backend code/capabilities**


Existing MVP screenshots are references for information architecture, terminology, and functionality, not the desired final visual design.


## Avoid
Avoid dark mode, excessive gradients, neon/futuristic AI styling, excessive animation, decorative graphics without purpose, giant KPI grids, excessive charts, generic dashboard templates, unnecessary dependencies, unnecessary architectural complexity, and unrelated refactoring.


Do not optimize for maximum information. Optimize for helping users understand what matters.


## Preferred Agent Workflow
1. Read `CLAUDE.md`.
2. Read relevant `DESIGN.md` sections.
3. Inspect existing frontend and backend.
4. Identify reusable components and backend capabilities.
5. For substantial changes, propose the smallest appropriate approach.
6. Implement.
7. Run relevant checks and fix errors.
8. Review against the design system and existing functionality.
9. Summarize changes, assumptions, and unresolved integration needs.


When asked to analyze without changes, do not modify files. When uncertain, ask rather than silently changing architecture or backend behavior.
