# InsightCX — Design System & UX Specification
## Product Identity
**Product:** InsightCX
**Tagline:** Every Voice. Every Insight.

InsightCX is an AI-powered Voice of Customer analytics platform that interprets customer feedback into business meaning, priorities, and recommended actions.

Traditional CX dashboards answer "What happened?" InsightCX should answer:
**What is happening, why, what does it mean for the business, and what should leadership do next?**

## Target Users
- **Executives / Leadership:** customer health, impact, priorities, actions.
- **CX professionals:** customer signals, drivers, evidence.
- **Business / Operations:** operational issues, themes, evidence.
- **Technical / AI users:** prompts, models, benchmarks, configuration.

User-facing pages should be business-oriented; internal AI tooling can be technical.

## Visual Direction
Combine modern premium SaaS with an editorial, insight-led hierarchy and a light touch of AI/technology feel.

Should feel intelligent, calm, professional, trustworthy, insightful, modern, precise, and business-oriented.

Avoid loud, neon, gaming-oriented, overly futuristic, overly corporate, or generic BI-dashboard styling.

## Color Direction
Light mode only.
- Primary: indigo
- Secondary: teal
- Base: very light neutral background
- Surfaces: white
- Text: dark slate/charcoal
- Semantic: green positive, red negative/critical, amber warning, blue/indigo informational

Use semantic colors meaningfully and sparingly.

## Typography & Layout
Use a modern, highly readable sans-serif with clear hierarchy between titles, sections, insight headlines, supporting text, labels, metadata, and metrics.

KPI numbers should support the narrative rather than dominate it.

Use generous whitespace, consistent spacing, subtle borders/shadows, moderate corner rounding, and clear alignment.

Cards should group meaningful information, not simply divide the page. Avoid excessive nesting and dense walls of information.

## Application Shell
Use a consistent SaaS shell with:
1. Executive Brief
2. Feedback Explorer
3. Upload
4. AI Evaluation
5. Administration

Active navigation must be obvious.

Wordmark: **InsightCX — Every Voice. Every Insight.**
Keep it simple and text-based.

## Executive Brief
This is the most important page: an intelligent executive briefing, not a conventional dashboard.

Narrative arc:
**Customer state → explanation → business impact → priority → action → evidence**

Hierarchy:
Customer Health → Executive Summary → Key Metrics → Business Drivers → Sentiment & Emotion → Leadership Priorities → Recommended Actions → Trends → Customer Evidence

Customer Health is the signature component: status, headline interpretation, why it exists, and supporting signals. Narrative should be more prominent than raw numbers.

Executive Summary answers what leadership needs to know right now in concise business language; never present raw JSON as the primary experience.

Key Metrics support the narrative rather than forming a conventional KPI grid.

Business Drivers should use insight-oriented cards containing impact, sentiment, explanation, evidence, and business relevance.

Sentiment & Emotion should pair percentages with interpretation.

Leadership Priorities connect Problem → Business Impact → Priority → Action.

Recommended Actions should be specific and tied to identified drivers.

Trends should show direction, magnitude, period, and interpretation.

Customer Evidence should provide traceability from conclusions to underlying feedback and link to Feedback Explorer where practical.

## Feedback Explorer
Purpose: find and understand the evidence behind InsightCX conclusions.

Core flow:
**Search → Filter → Scan → Investigate**

Filters may include search, sentiment, survey type, priority, date, theme/reason, and customer intent where supported.

Detail views should show available analysis such as original comment, sentiment, emotion, customer intent, priority, confidence, reason codes/themes, business signal, and AI summary.

## Upload
Preferred flow:
**Select → Validate → Preview → Import → Confirmation**

Keep it simple and trustworthy. If a stage is not backend-supported, use realistic frontend/demo state rather than changing backend behavior.

## AI Evaluation
AI Evaluation is one cohesive technical workspace, not two unrelated pages.

The experience should make this workflow intuitive:
**Test → Compare → Benchmark → Evaluate**

Use shared configuration patterns and consistent navigation across:

### Single Test
Input → Configuration → AI Analysis → Results

Configuration may include model, temperature, system prompt, and feedback prompt. Results may include sentiment, emotion, customer intent, priority, confidence, reason codes, and business signal.

### Benchmark Lab
Configuration → Dataset → Run → Summary → Results

Show supported statistics such as processed, successful, failed, and average confidence.

### Model Comparison
Present existing model/configuration performance clearly using the backend benchmark and comparison data.

### Current vs. New Analysis
Use side-by-side comparison to highlight changed fields and answer:
**Did this model/prompt combination produce a better or different analysis?**

Do not invent backend evaluation logic.

## Administration
Administration should feel professional and operational, not like a generic settings page.

Include existing areas for Feedback Analysis, Executive Analysis, Executive Summary Generation, Maintenance, and Danger Zone.

Technical/raw JSON may be available where useful, but should never be the primary presentation.

Destructive operations always require confirmation.

## Technical Metadata
Model names, prompt versions, timestamps, benchmark status, processing statistics, and similar metadata belong primarily in internal AI/administration areas.

Keep technical detail subtle or hidden in executive-facing areas.

## Reusable Components
Prefer reusable components such as:
AppShell, Navigation, PageHeader, SectionHeader, InsightCard, MetricCard, StatusBadge, PriorityBadge, SentimentBadge, DataTable, FilterBar, EmptyState, LoadingState, ErrorState, ConfirmationDialog, Tabs, Modal/Drawer, ProgressIndicator.

Use consistent patterns rather than page-specific duplicates.

## Interaction, Accessibility & Responsive
Use purposeful interactions only: clear hover/selected states, restrained transitions, meaningful loading/empty states, and helpful errors. Avoid decorative motion.

Prioritize keyboard access, visible focus states, semantic HTML, accessible labels, sufficient contrast, and interfaces that do not rely on color alone.

Priority:
**desktop → laptop → tablet → smaller screens**

On smaller screens, tables may scroll or become cards, navigation may collapse, and multi-column layouts may stack. Preserve information hierarchy rather than simply shrinking everything.

## Visual Do / Don't
**Do:** restrained indigo/teal identity, meaningful semantic colors, generous whitespace, strong hierarchy, prominent interpretation, evidence-backed conclusions, clean investigative tables, technical detail in internal tools, calm and trustworthy presentation.

**Don't:** dark mode, neon colors, excessive gradients, futuristic AI imagery, excessive charts, giant KPI grids, generic BI layouts, excessive card nesting/badges, decorative illustrations without purpose, dense walls of text, unnecessary animations, or technical jargon in executive-facing areas.

## Guiding Principle
> **Do not optimize for showing more information. Optimize for helping users understand what matters.**

Every major screen should answer:
**What is happening? Why is it happening? Why does it matter? What should we do? What evidence supports the conclusion?**

This is what differentiates InsightCX from a conventional CX dashboard.
