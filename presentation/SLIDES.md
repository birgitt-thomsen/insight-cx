# InsightCX MVP Presentation

## Purpose

Create a ~30-minute presentation introducing the InsightCX MVP.

The presentation should tell a clear story:

> **Customer feedback is abundant, but turning it into reliable, actionable insight is difficult. InsightCX explores how LLMs can transform unstructured customer feedback into structured CX data and executive-level business insight.**

The presentation should feel like a **product + AI engineering case study**, not a generic software demo or a technical walkthrough.

The strongest narrative is:

**CX problem → realistic business scenario → AI approach → two LLM capabilities → evaluation → business value → working MVP → demo**

The presenter has extensive experience in Customer Experience and analytics and is currently developing AI engineering skills. The presentation should naturally communicate this intersection without making the career background the focus.

---

# Build & delivery specification

This section is instructions for Claude Code, not presentation content — it defines the concrete deliverable.

**Output format:** Build the deck as a `.pptx` file using `python-pptx`, saved to `presentation/InsightCX_MVP.pptx` in the repo root. Do not attempt to write directly to Google Slides — there is no API access for that from this session. The `.pptx` will be uploaded to Google Drive afterward and opened as a native, editable Google Slides file.

**Canvas:** 16:9 widescreen, 13.33in × 7.5in.

**Fonts:** Use only fonts that render identically in Google Slides after a 
PowerPoint import — Arial, Roboto, or Open Sans. Use whatever typeface 
`frontend/DESIGN.md` already specifies if it's one of these; otherwise default 
to Roboto for headlines and Open Sans for body text.

**Colors:** Pull the exact indigo/teal hex values from `frontend/DESIGN.md` (or the frontend's CSS variables) rather than inventing new shades. Reuse the same palette used in the product itself so the deck and the live demo feel like one product.

**Diagrams:** Every flow shown below with "↓" (e.g. Slide 2, Slide 4, Slide 8, the demo journey) should be built as real shapes with connector arrows — rounded rectangles or cards linked by arrow connectors — not literal arrow characters or plain stacked text.

**Assets to use:**
**Wordmark logo:** There is no exported image asset — the logo is rendered live in the frontend from `frontend/src/components/Logo.tsx` (or wherever it lives) as styled text, not a file. Recreate it as native text directly in the slide (not an image):
  * "Insight" in `#312e81` (Tailwind indigo-900), "CX" in `#115e59` (Tailwind teal-800), both bold/semibold with tight letter spacing — same two-tone treatment as the component.
  * Tagline "Every Voice. Every Insight." underneath, smaller, in `#115e59`.
  * Confirm these hex values against the actual Tailwind config before use, in case the color scale was customized from the defaults.
* Product screenshots — **use component-level crops, not full-page captures.** Full pages (e.g. the whole Executive Brief view) carry far too much context for a 5-second-read slide; every screenshot used in the deck should be a single self-contained UI element, captured via Chrome DevTools "Capture node screenshot" for a clean, pixel-perfect crop. Specific crops needed:
  * **Slide 5 / demo step 2** — the Feedback Explorer detail panel (single feedback item with AI Assessment: sentiment, emotions, intent, reason codes, business interpretation). Crop out the "Re-analyze Feedback / Test in AI Evaluation" action buttons at the bottom. Path: `presentation/assets/feedback_detail.png`
  * **Slide 7 (dashboard)** — the Key Metrics strip only (Total feedback / NPS / CSAT / Confidence), as one crop. Path: `presentation/assets/key_metrics.png`. Optionally a second, separate crop of just the sentiment breakdown cards (positive/neutral/negative %). Path: `presentation/assets/sentiment_metrics.png`
  * **Slide 6 / demo step 3 (executive insight)** — a single Leadership Priority card (business objective / why now / executive owner), not the full Executive Brief page. Path: `presentation/assets/leadership_priorities.png`
  * **Slide 9 / demo step 4 (AI evaluation)** — a crop of the model comparison view. Path: `presentation/assets/model_comparison.png`
  * If a needed crop isn't available at build time, skip that visual element rather than substituting the full-page screenshot or a mockup.
* If an asset above isn't found at build time, don't invent a placeholder graphic in its place — skip that visual element and flag it rather than guessing.

**Build order:** First generate a one-line-per-slide outline matching the "Overall story" section near the end of this doc, for review, before generating the full deck.

**Deliverable:** 12 numbered slides + the closing slide = 13 slides total, matching the slide-by-slide sections below.

---

# Presentation goals

By the end of the presentation, the audience should understand:

1. What customer-feedback problem InsightCX is solving.
2. Why unstructured customer comments are difficult to analyze at scale.
3. How InsightCX uses an LLM to turn individual comments into structured CX data.
4. How a second LLM capability turns aggregated feedback into executive-level insight.
5. Why model evaluation matters when building an application around LLMs.
6. What the MVP demonstrates and what would be required to move toward production.
7. How the different components come together in the live demo.

---

# Audience takeaway

The audience should leave remembering five ideas:

### 1. There is a real CX problem

**Lots of feedback does not automatically mean lots of insight.**

### 2. LLMs can structure the customer voice

**Unstructured text → structured CX data**

### 3. LLMs can help interpret the bigger picture

**Customer comments → business insight**

### 4. AI needs to be evaluated

**Quality is not the only consideration — cost, latency and consistency matter.**

### 5. InsightCX is a working MVP

This is not simply an experiment calling an LLM API. It is an application that connects data ingestion, AI analysis, persistence, visualization, executive insights and model evaluation.

---

# Presentation length

Target approximately **30 minutes total**.

Recommended allocation:

| Section                             | Approx. time |
| ----------------------------------- | -----------: |
| Opening / problem                   |      2–3 min |
| Business scenario                   |        3 min |
| InsightCX overview                  |        2 min |
| LLM feature #1                      |        4 min |
| LLM feature #2                      |        4 min |
| From AI output to business decision |      2–3 min |
| AI evaluation                       |        3 min |
| Lessons learned                     |        2 min |
| Future direction                    |      1–2 min |
| Live demo                           |      6–8 min |

The presentation content itself should ideally take **~22–23 minutes**, leaving flexibility for transitions and the demo.

---

# Slide design principles

Follow the existing InsightCX visual direction and `frontend/DESIGN.md`.

Use:

* Indigo / teal visual language
* Clean, modern SaaS / analytics aesthetic
* Light mode
* Strong visual hierarchy
* Minimal text
* Large headlines
* Simple diagrams and flows
* Realistic product screenshots where available
* Consistent typography
* Consistent spacing
* Subtle use of cards and data visualizations

Do NOT create slides that look like text-heavy corporate PowerPoint templates.

The slides should support the speaker rather than contain the entire script.

Use short phrases and visual storytelling.

Avoid:

* Paragraph-heavy slides
* Excessive bullet points
* Generic AI imagery
* Decorative stock photography
* Unnecessary technical jargon
* Long code snippets
* A standalone "technology stack" slide

Technology should be introduced naturally where relevant.

---

# Slide 1 — InsightCX

## Headline

**InsightCX**

## Subheadline

**Every Voice. Every Insight.**

## Supporting text

**AI-powered Voice of Customer analytics**

Optional supporting line:

> Transforming customer feedback into structured insight and actionable business intelligence.

## Visual direction

Create a strong, minimal opening slide.

Feature the InsightCX wordmark logo (see Assets in the Build & delivery specification) prominently — this is the primary branding moment of the deck.

Possible visual:

**Customer Feedback → AI Analysis → Actionable Insight**

Keep this slide visually simple.

Do not introduce detailed technical architecture yet.

## Speaker focus

Introduce InsightCX as an exploration of how AI engineering can be applied to a real CX problem.

The presenter should explain that the project combines CX/domain knowledge with AI engineering.

---

# Slide 2 — The Problem

## Headline

**Customer feedback contains the answers — but they're buried in text.**

## Core message

Companies may have hundreds or thousands of customer comments, but the feedback is unstructured.

## Visual content

Show several short, realistic customer comments, for example:

> "The sofa is beautiful, but delivery was two days late."

> "The assembly instructions were impossible to follow."

> "Returning the table was surprisingly easy."

> "I couldn't find any information about my order."

Then visually connect:

**Hundreds of comments**

↓

**Unstructured customer language**

↓

**Manual analysis**

↓

**Slow / inconsistent insight**

↓

**Missed opportunities**

## Speaker focus

Explain that the problem is not lack of customer feedback.

The problem is converting large amounts of free-text feedback into consistent, actionable information.

Different customers may describe the same underlying problem in completely different ways.

Management ultimately needs patterns, priorities and business implications rather than hundreds of individual comments.

End with the question:

> **Can an LLM turn that unstructured customer voice into something we can actually analyze?**

---

# Slide 3 — The Business Scenario

## Headline

**A home-furnishing retailer with hundreds of customer voices**

## Context

The MVP uses a fictional online home-furnishing retailer as the test environment.

## Customer journey

Show visually:

**Discover → Purchase → Delivery → Assembly → Use → Support / Return**

## Feedback sources

### NPS

Recommendation / loyalty feedback

### CSAT

Customer satisfaction feedback

### Customer comments

Free-text feedback explaining the experience

## Test dataset

Show visually rather than as a long list:

* Several hundred feedback records
* NPS + CSAT
* Multiple weeks of activity
* Positive / neutral / negative feedback
* Multiple CX themes

Important themes:

* Delivery
* Product quality & assembly
* Returns
* Website experience
* Payment / billing
* Brand loyalty

## Speaker focus

Explain that the dataset was deliberately designed to create a realistic test environment.

The goal was not to claim that this is production data.

The goal was to create a controlled scenario where the AI functionality could be tested consistently.

---

# Slide 4 — What is InsightCX?

## Headline

**From customer voice to business insight**

## Main visual

Create a simple end-to-end flow:

**Customer Feedback**

↓

**CSV Import**

↓

**Feedback Data**

↓

**LLM Analysis**

↓

**Structured CX Data**

↓

**Dashboard + Executive Insights**

↓

**Business Decisions**

Alongside or underneath, show:

**AI Evaluation**

**Model quality / consistency · latency · tokens · cost**

## Speaker focus

Explain the three major stages:

1. Ingest customer feedback.
2. Use an LLM to convert individual comments into structured CX attributes.
3. Aggregate those results into dashboards and executive-level insights.

Explain that AI evaluation sits alongside the application because model selection is itself an engineering decision.

Do not spend significant time explaining the framework or individual libraries.

---

# Slide 5 — LLM Feature #1

## Headline

**Turning customer language into structured CX data**

## Main visual

Show one realistic customer comment prominently:

> "The sofa looks great, but delivery was two days late and the assembly instructions were confusing."

Then show the resulting structured analysis.

Example:

| Attribute  | Result                                                          |
| ---------- | --------------------------------------------------------------- |
| Sentiment  | Negative                                                        |
| Emotion    | Frustration                                                     |
| Themes     | Delivery, Assembly                                              |
| Priority   | High                                                            |
| Confidence | 0.91                                                            |
| Summary    | Delivery delay and unclear instructions affected the experience |

The exact values may be replaced with representative values if necessary.

## Key concept

Visually emphasize:

**Natural language → Structured data**

## Speaker focus

Explain that the LLM is not simply being asked to summarize the comment.

It is being asked to transform natural language into a predefined analytical structure.

The structured output can then be:

* Stored
* Aggregated
* Queried
* Visualized
* Used as input for further analysis

Important statement to emphasize:

> **Once the LLM output is structured, it stops being just text and becomes data the application can work with.**

Mention that customers can express similar experiences in many different ways, while the application needs consistent categories for analysis.

---

# Slide 6 — LLM Feature #2

## Headline

**From individual comments to executive insight**

## Main visual

Contrast the two LLM capabilities.

| Feedback analysis  | Executive insights    |
| ------------------ | --------------------- |
| Individual comment | Aggregated feedback   |
| What happened?     | What does it mean?    |
| Sentiment          | Customer health       |
| Themes             | Business impact       |
| Priority           | Leadership priorities |
| Summary            | Recommended actions   |

Then show:

**Hundreds of customer comments**

↓

**Patterns across feedback**

↓

**Business interpretation**

↓

**Recommended action**

## Speaker focus

Explain the conceptual difference:

### Feature 1

**What is this customer saying?**

### Feature 2

**What does everything we're seeing mean for the business?**

Example:

Individual analyses reveal:

* Delivery appears frequently.
* Delivery appears frequently in negative feedback.
* Delivery is common among detractors.

The executive insight layer can turn those observations into:

> **Delivery reliability is emerging as a significant driver of customer dissatisfaction.**

And potentially:

> **Leadership priority: investigate delivery reliability and communication around delays.**

Important point:

> The value is not simply generating a nicer summary. It is moving from classification to interpretation.

---

# Slide 7 — The Dashboard

## Headline

**Making customer health visible**

## Visual

Use an actual InsightCX dashboard screenshot if available.

Show / highlight:

* Total feedback
* NPS
* CSAT
* Sentiment distribution
* Top themes
* Trends, if available

Use subtle numbered callouts:

**1. Customer health**

**2. Sentiment**

**3. Main drivers**

## Speaker focus

Explain that once individual feedback has been structured, it can be analyzed as a dataset.

The dashboard turns the AI-generated data into something a CX team can monitor.

Do not explain every dashboard component.

Focus on the journey:

**Individual comments → structured analysis → aggregated customer-health view**

---

# Slide 8 — From AI Output to Business Decision

## Headline

**From customer voice to action**

## Main visual

Create a clear chain:

**Customer voice**

↓

**Structured AI analysis**

↓

**Aggregated patterns**

↓

**Business interpretation**

↓

**Recommended action**

## Example

Show a simplified example:

**Delivery appears in a large share of negative feedback**

↓

**Delivery is disproportionately represented among detractors**

↓

**Delivery may be a customer-health driver**

↓

**Investigate carrier performance and delivery communication**

## Speaker focus

This slide connects the technical AI functionality back to CX/business value.

The purpose of InsightCX is not to produce AI labels for their own sake.

The ultimate goal is to help people identify what deserves attention.

Emphasize:

> **InsightCX is intended to augment CX expertise, not replace it.**

---

# Slide 9 — Can We Trust the AI?

## Headline

**Model performance isn't just about quality**

## Main visual

Show:

**Same dataset**

**240 feedback records**

↓

**Same task / same prompts**

↓

**Different models**

* GPT-5-mini
* GPT-4.1-mini
* GPT-4o-mini

↓

**Compare**

* Consistency / agreement
* Latency
* Token usage
* Estimated cost

## Optional results table

Use the actual benchmark results from the InsightCX project if available.

Do not invent numbers.

If final benchmark values are not available when the slides are generated, create clearly marked placeholders.

Example:

| Model        | Consistency | Latency | Tokens | Cost |
| ------------ | ----------: | ------: | -----: | ---: |
| GPT-5-mini   |           — |       — |      — |    — |
| GPT-4.1-mini |           — |       — |      — |    — |
| GPT-4o-mini  |           — |       — |      — |    — |

## Speaker focus

Explain the practical engineering question:

> If the application relies on an LLM, how do we decide which model to use?

The most capable model is not necessarily the best production choice.

A model can be:

* More expensive
* Slower
* More capable than necessary for the task

The benchmark evaluates practical trade-offs.

Important positioning:

> This is not intended to be a comprehensive LLM evaluation framework. It is a lightweight MVP approach to answering which model provides the best trade-off for this specific use case.

---

# Slide 10 — What I Learned

## Headline

**What did the MVP teach me?**

## Four visual cards

### 1. Structure matters

**LLM output becomes much more useful when it can reliably feed downstream application logic.**

### 2. Prompt design matters

**Instructions and expected output structure influence consistency.**

### 3. Model choice is a trade-off

**Capability isn't the only consideration — cost and latency matter too.**

### 4. AI needs evaluation

**"It looks good" isn't enough when AI output drives business decisions.**

## Speaker focus

Use this as a reflective engineering slide.

Key message:

> Integrating an LLM is relatively easy. Designing useful output, handling variability and evaluating whether the result is actually useful are harder problems.

This slide should make the project feel like an engineering learning experience rather than simply a product showcase.

---

# Slide 11 — What's Next?

## Headline

**From MVP to production**

## Four areas

### Human-in-the-loop

Validate and correct AI classifications.

### Trend analysis

Identify emerging CX issues over time.

### Advanced evaluation

Introduce ground-truth datasets and more formal quality metrics.

### Real-world integrations

Connect survey, CRM and support systems.

Optional fifth:

### Role-specific insights

Tailor insights for CX managers, operations teams and executives.

## Speaker focus

Clearly distinguish MVP scope from production requirements.

The most important production consideration is likely human validation / ground truth.

Explain that future evaluation should compare AI output against expert judgments.

Do not present this as a promise or committed roadmap.

---

# Slide 12 — Live Demo

## Headline

**Let's see it in action**

## Visual

Show the demo journey:

**1. Upload feedback**

↓

**2. Analyze customer voice**

↓

**3. Explore customer health**

↓

**4. Generate executive insight**

↓

**5. Evaluate the AI**

## Speaker focus

Tell the audience:

> "Rather than showing every feature, I'm going to follow one feedback-to-insight journey through the application."

Then begin the live demo.

---

# Live Demo Plan

The live demo should take approximately **6–8 minutes**.

Do not attempt to demonstrate every application feature.

Use one coherent customer-feedback story.

## Demo step 1 — Dashboard

Show:

* Overall customer health
* NPS
* CSAT
* Sentiment
* Top themes

Narrative:

> "I start here because I want to understand the overall customer picture."

## Demo step 2 — Individual feedback

Open one realistic customer comment.

Show:

**Raw comment → sentiment → emotion → themes → priority → summary**

Narrative:

> "Let's look at what sits behind those numbers."

## Demo step 3 — Executive insights

Show the executive insight functionality.

Focus on:

* What is happening?
* Why does it matter?
* What should leadership pay attention to?
* What actions are recommended?

Narrative:

> "Now instead of looking at one customer, let's ask what the overall feedback tells us."

## Demo step 4 — AI Evaluation

Show the model comparison.

Focus on:

* Same dataset
* Different models
* Latency
* Tokens
* Cost
* Consistency / agreement

Narrative:

> "And if I'm going to rely on an LLM for this, I also want to understand how different models behave."

---

# Backup Demo

A short pre-recorded demo should cover the same journey as the live demo.

If the live demo encounters a technical issue, switch quickly rather than troubleshooting for several minutes.

Suggested wording:

> "I've also recorded the same flow in advance, so if the API decides to have other plans today, we can switch to the recording."

The backup recording should ideally be **5–7 minutes maximum**.

---

# Closing message

The final takeaway should return to the original problem.

Use the following conceptual message:

> **InsightCX is about using AI to make customer feedback more structured, scalable and actionable — so CX teams can spend less time processing feedback and more time acting on it.**

Final branding:

**InsightCX** wordmark logo (see Assets in the Build & delivery specification)

**Every Voice. Every Insight.**

---

# Content constraints

## Keep slides concise

Slides should contain:

* Headlines
* Short supporting statements
* Diagrams
* Data
* Screenshots
* Short examples

Slides should NOT contain the complete spoken script.

## Avoid overclaiming

Do not describe the MVP as:

* Production-ready
* Fully autonomous
* Scientifically validated
* A comprehensive LLM evaluation framework
* A replacement for CX teams

Use language such as:

* "MVP"
* "explores"
* "demonstrates"
* "prototype"
* "test scenario"
* "lightweight evaluation"
* "potential next step"

## Technical detail

Technical details are relevant when they explain a design decision.

Do not create a technology-stack showcase.

Mention technologies in context:

* OpenAI API → LLM functionality
* Flask → application/backend
* SQLAlchemy → data persistence
* Chart.js → dashboard visualization

The presentation should remain understandable to a mixed technical/business audience.

---

# Overall story

The final presentation should feel like one continuous story:

## Problem

**We have lots of customer feedback, but extracting insight is difficult.**

↓

## Scenario

**Let's test the idea using a realistic home-furnishing retailer.**

↓

## Solution

**InsightCX converts customer language into structured CX data.**

↓

## Intelligence

**A second LLM layer turns patterns into executive insight.**

↓

## Evaluation

**We need to understand whether the AI is consistent, fast and cost-effective.**

↓

## Business value

**The result is a path from customer voice to business action.**

↓

## MVP

**Here is the working application.**

↓

## Demo

**Let's see that journey in action.**

---

# Design priority

When choosing between adding more information and making a slide easier to understand:

**Choose clarity.**

The audience should be able to understand the main point of every slide within approximately **5 seconds**.

The presenter will provide the detail verbally.
