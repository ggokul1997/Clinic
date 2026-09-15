# Project Brief: AI-Native Healthcare Platform & Operating Hub

## 1. Core Vision
We are building a modern digital operating hub for a clinic/hospital. Rather than a static brochure website, the core of the product is an **Agentic Admin CMS** that manages both the public-facing patient portal and an internal network of automated AI subagents.

## 2. Guiding Principles & Team Constraints
* **CMS-First Priority:** The admin dashboard is the foundational product. All clinic controls, page modifications, and autonomous subagents live inside this interface.
* **Agentic Harness Over Simple Prompts:** We are not building standard Q&A bots. We are designing multi-step, observable autonomous loops (agentic workflows) that perform ongoing tasks.
* **Security-First Architecture:** The CMS must be strictly guarded against admin hijacking, unauthorized page injection (SEO spam poisoning), and payment compromise.
* **Designer Collaboration:** Frontend page templates will be provided as responsive HTML/CSS by our UI designer. The CMS must ingest and map dynamic data into these modular designs.

## 3. Product Architecture

### A. The Admin CMS (Priority #1)
* Acts as the single-pane-of-glass operating system.
* Dynamic navigation menu reordering and department/service page management.
* Exploration of Natural Language / Agentic UI editing (e.g., updating site layouts or blocks via conversational prompts).
* Secure access control and audit logging.

### B. The Public Clinic Portal
* Fast, mobile-first patient experience: doctor directories, appointment booking, department overviews, and clinic services.
* High SEO visibility and clean Core Web Vitals.

### C. Subagent Ecosystem
1. **Competitor Intelligence Agent (First Target):** Autonomously monitors domestic and international clinic competitors to extract pricing trends, new clinical offerings, and high-performing healthcare content topics.
2. **Product & Discovery Agent:** Challenges product assumptions, uncovers missing clinical edge cases, and drafts technical specifications.
3. **Marketing & SEO Agent:** Tracks regional healthcare keywords and drafts educational medical blogs for doctors to review.
4. **Front-Desk & Booking Agent:** Frontline website assistant handling patient inquiries, calendar slot checks, and appointment scheduling.
5. **Observability & Sandbox QA Agent:** Simulates synthetic patient flows in a staging environment to detect broken links, latency spikes, or failed booking states.

## 4. Current Phase: Strategic Product Research
* Focus is strictly on **product strategy, competitive benchmarking, feature prioritization, and edge-case discovery**.
* Do not generate production code yet. Act as an expert healthcare systems architect and product strategist.