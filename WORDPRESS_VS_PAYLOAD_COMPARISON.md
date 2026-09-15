# WordPress + Plugin Stack vs. Payload CMS 3.x

**A platform decision for the RegenCare content platform**

| | |
|---|---|
| **Document version** | 3.0 — CMS comparison only; design-file analysis removed |
| **Date** | 2026-09-09 |
| **Context** | Pivot away from appointment booking toward a dynamic content platform |
| **Scope** | Dynamic pages, clinical research articles, blogs, video/media, deep SEO, AI agent readiness |
| **Compared** | WordPress 7.0 + Rank Math/Yoast + ACF Pro + CPT UI + Elementor Pro + Smush **vs.** Payload CMS 3.88.0 native |
| **Existing asset** | Working Payload 3.88.0 POC in `clinic-poc/` (see `PROJECT_DETAILS.txt`) |
| **Deliberately excluded** | The supplied design files. This document compares the two platforms on their own merits — see the note below. |

> **On scope.** An earlier version of this document leaned on an audit of the supplied design bundles to argue that WordPress's theme-ecosystem advantage was neutralised. That analysis has been removed at the team's direction, and the comparison now stands on the platforms alone.
>
> This is a deliberate handicap on Payload's side, and it should be read as one. Without the design analysis, **WordPress's "buy a theme and launch in weeks" advantage is live and real**, and it is credited as such throughout (§1, §6, §14). The verdict is unchanged, but it now rests on structure, governance, performance, security and agent safety rather than on any property of the incoming designs.

---

## Contents

| § | Section |
|---|---|
| 1 | Executive summary and verdict |
| 2 | What the pivot changes |
| 3 | Platform anatomy — what you are actually adopting |
| **4** | **Plugin deep-dive: CPT UI vs. typed collections** |
| **5** | **Plugin deep-dive: ACF Pro vs. Payload native fields** |
| **6** | **Plugin deep-dive: Elementor Pro vs. Payload blocks → React** |
| **7** | **Plugin deep-dive: Yoast / Rank Math vs. plugin-seo + `generateMetadata`** |
| **8** | **Plugin deep-dive: Smush / ShortPixel vs. native `sharp` variants** |
| 9 | Dynamic URLs, slugs and routing |
| 10 | Performance and Core Web Vitals |
| 11 | Security attack surface |
| 12 | AI agent readiness — MCP vs. WP REST |
| 13 | Editorial governance and clinical credentialing |
| 14 | Cost of ownership |
| 15 | Scorecard |
| 16 | Architectural verdict |
| 17 | Target architecture |
| 18 | Migration path |
| 19 | Sources |

---

## 1. Executive summary and verdict

**Recommendation: build on Payload CMS 3.x. Do not adopt WordPress.**

### 1.1 The plugin comparison is close to a tie

Compared head to head on the stack we would actually buy, the result is nearly even:

| Capability | Plugin | Payload equivalent | Winner |
|---|---|---|---|
| Content types | CPT UI | typed collections | **WordPress** |
| Custom fields | ACF Pro | native `fields: [...]` | **Payload** |
| Page building | Elementor Pro | `blocks` → React | **Payload** |
| SEO tooling | Rank Math / Yoast | `plugin-seo` + `generateMetadata` | **WordPress** |
| Images | Smush / ShortPixel | native `sharp` | Even |

**Two each, one even.** If this decision rested on plugin capability alone, it would be a coin toss, and the cheaper, easier-to-hire-for option would win by default.

It does not rest there. Three things outside the plugin comparison decide it.

### 1.2 What actually decides it

**1. Five plugins is the attack surface.**
Adopting Rank Math + ACF Pro + CPT UI + Elementor + Smush means adopting five independently-maintained codebases with database access inside the admin. In 2025, **91% of 11,334 WordPress ecosystem vulnerabilities were in plugins**; core had six, all low-risk. The weighted median time from disclosure to first exploitation is **five hours**, and **46%** were disclosed with no patch available (§11). For a clinical brand, a defacement is a reputational event, not an outage.

**2. Clinical content needs an enforced credentialing chain.**
`MedicalWebPage.reviewedBy` is the signal Google's quality systems and AI answer engines use to judge medical trustworthiness. In Payload it is a **required relationship to a credentialed clinician record, enforced at publish time by access control**. In WordPress it is a schema field an editor types into and can leave blank (§13).

**3. Structure and speed compound across hundreds of articles.**
A booking site has twenty pages, so `wp_postmeta` scans and Elementor's DOM weight stay theoretical. A content platform has hundreds and growing, where they become crawl budget, indexation depth and AI-citation eligibility (§5, §6, §10).

A fourth point matters for the roadmap rather than today: **agent write-scope must be enforced, not configured.** Both platforms now ship MCP servers — WordPress is genuinely *not* behind here — but Payload's access control can return a **query constraint** rather than a boolean, so the restriction is declared once on the collection and applies to every route into it instead of being repeated per endpoint (§12).

### 1.3 Where WordPress genuinely wins

State these to management rather than hiding them:

- **Speed to first launch.** A purchased theme plus these five plugins can put a competent clinical site live in weeks. Payload starts from components. With the design question set aside, **this is WordPress's strongest card and it is a real one.**
- **Editor autonomy.** CPT UI + ACF let marketing staff create content types with no developer and no deploy. Payload cannot do this at all.
- **SEO tooling velocity.** Rank Math's Schema Builder, readability scoring, 404 monitoring and redirect UI are mature. Payload has none of it pre-built.
- **Media library UX.** WordPress's is better, and asset-folder plugins are mature.
- **Hiring and handover.** WordPress developers are abundant and cheap; Payload developers are neither.

### 1.4 The verdict

Build on Payload — **unless** the business requires non-technical staff to create and restructure content types without engineering involvement. That is the one requirement that flips the decision, and it is a business question, not a technical one. Settle it before build starts (§16.3).

---

## 2. What the pivot changes

### 2.1 Old target vs. new target

| | Before the pivot | After the pivot |
|---|---|---|
| Centre of product | Appointment booking | Content at volume |
| Dominant entity | Appointment slot | Article, procedure, condition |
| Success metric | Bookings completed | Organic reach, indexation, AI citation |
| Content volume | ~20 static pages | Hundreds of articles, growing |
| Riskiest data | **PHI** | Public marketing content |
| SEO role | Nice to have | **The product** |

### 2.2 What the new target demands

1. **Composable dynamic pages** — marketing must assemble pages from approved sections without a developer per page.
2. **Clinical research articles** with author, medical reviewer, review date, citations and credentials as *structured data*, not prose.
3. **Editorial governance** — nothing clinical reaches patients unreviewed.
4. **Video and media** at scale, with transcripts.
5. **Deep SEO** — technical, structured and answer-engine.
6. **AI agent readiness** — agents drafting content safely.
7. **Security** proportionate to a healthcare brand.

### 2.3 Why volume changes the answer

Every criticism of WordPress in this document is survivable at twenty pages. `wp_postmeta` scans are fast on a small table. Elementor's DOM weight costs one page's LCP. Five plugins are five things to patch.

At several hundred articles with faceted filtering, reverse relationships and a publishing cadence, the same properties become structural: meta queries that cannot be indexed well, a DOM tax paid on every indexed page, and a patch surface that must be watched continuously. **The pivot did not change the platforms. It changed which of their properties matter.**

### 2.4 The PHI boundary gets easier, not harder

Dropping booking removes the only feature that dragged patient data toward the CMS. Keep it that way. **PHI in the CMS would pull the entire database into HIPAA scope** — audit controls, encryption at rest, a signed BAA, breach notification. Both platforms are acceptable for public marketing content; neither should hold patient records.

---

## 3. Platform anatomy — what you are actually adopting

Before comparing features, be precise about what each option *is*.

| | WordPress option | Payload option |
|---|---|---|
| Core | WordPress 7.0 (PHP) | Payload 3.88.0 (TypeScript) |
| Runtime | PHP-FPM + MySQL per request | Node — Next.js 16 App Router |
| Admin UI | PHP-rendered, plugin-extended | React app **inside your Next.js app** |
| Frontend | PHP themes, or headless via REST/WPGraphQL | Same app, `(frontend)` route group |
| Content types | **CPT UI plugin** | TypeScript collection configs |
| Custom fields | **ACF Pro plugin** | Native `fields: [...]` |
| Page building | **Elementor Pro plugin** | Native `blocks` field |
| SEO | **Rank Math / Yoast plugin** | `@payloadcms/plugin-seo` + Next.js Metadata API |
| Images | **Smush / ShortPixel plugin** | Native `sharp` `imageSizes` |
| Third-party code in runtime | **5 plugins** | **0** |
| Schema lives in | Database (plugin tables + options) | Version-controlled code |
| Schema change process | Click in admin, instant | Edit code → PR → deploy |

The structural difference in one line: **WordPress assembles capability from five independently-versioned third-party plugins at runtime; Payload provides the same five capabilities natively, in one codebase, at build time.**

That sentence explains most of what follows — including where WordPress wins.

---

## 4. Plugin deep-dive: CPT UI vs. typed collections

### 4.1 What CPT UI actually does

CPT UI exposes every `register_post_type()` argument as a form field, registers the type when you save, and offers export-to-PHP so you can graduate the registration into a real plugin later.

Its honest limitations:

- **It does not add custom fields.** CPT UI creates the *container* only. You must pair it with ACF or Meta Box (§5). Two plugins for what is one concept.
- **Everything shares `wp_posts`.** Custom post types are not separate tables — they are rows in `wp_posts` discriminated by a `post_type` column. Articles, procedures, conditions, clinicians and testimonials all pile into one table alongside posts, pages and revisions.
- **Rewrite rules must be flushed.** New CPTs 404 until permalinks are re-saved. In code you hook `flush_rewrite_rules()` to activation; via the UI it is a manual step people forget.
- **20-character slug limit** per post type.
- **Schema lives in the database.** A content type created in staging does not exist in production until someone repeats the clicks or exports PHP. There is no diff, no review, no rollback.

### 4.2 The Payload equivalent

A collection is a TypeScript file. From the working POC:

```ts
// src/collections/Doctors.ts  (abridged from the real POC)
export const Doctors: CollectionConfig = {
  slug: 'doctors',
  admin: {
    group: 'Clinic',
    useAsTitle: 'name',
    defaultColumns: ['name', 'department', 'specialization', 'updatedAt', '_status'],
  },
  access: {
    read: publishedOrAuthenticated,
    create: authenticated,
    update: authenticated,
    delete: authenticated,
    readVersions: authenticated,
  },
  versions: { drafts: true, maxPerDoc: 20 },
  fields: [ /* … */ ],
}
```

For the content platform this becomes `Articles.ts`, `Research.ts`, `Procedures.ts`, `Conditions.ts`, `Clinicians.ts`, `Testimonials.ts`, `Locations.ts`, `Pages.ts`.

Each gets its own relational table, generated types in `payload-types.ts`, and access control declared alongside the schema rather than bolted on by a separate plugin.

### 4.3 Head-to-head

| Capability | CPT UI (+ ACF) | Payload collections | Advantage |
|---|---|---|---|
| **Create a type with no developer** | ✅ **minutes, in admin** | ❌ code + deploy | **WordPress** |
| **Create a type with no deploy** | ✅ | ❌ | **WordPress** |
| Schema in version control | ❌ database | ✅ TypeScript files | Payload |
| Schema diffable / reviewable in PR | ❌ | ✅ | Payload |
| Schema promotes staging → production | ❌ manual repeat or PHP export | ✅ it is the code | Payload |
| Storage model | shared `wp_posts` | dedicated table per collection | Payload |
| Generated TypeScript types | ❌ | ✅ `payload-types.ts` | Payload |
| Custom fields included | ❌ needs ACF | ✅ native | Payload |
| Access control per type | 🟡 capabilities, plugin-mediated | ✅ per-operation functions | Payload |
| Drafts/versioning per type | 🟡 revisions; drafts need plugins | ✅ `versions: { drafts: true }` | Payload |
| Rewrite-rule flush needed | ⚠️ yes | ❌ n/a | Payload |
| Slug length limit | 20 chars | none meaningful | Payload |

### 4.4 Verdict

**This is WordPress's strongest structural win and it deserves to be taken seriously.** For a marketing team that wants to spin up a "Webinars" content type on a Tuesday afternoon, CPT UI is unbeatable and Payload has no answer at all.

Weigh what that autonomy costs on a *clinical* platform: an undiffable schema, no review before a content type reaches production, and no type safety downstream. For content where `medicalReviewer` must be a guaranteed relationship rather than a field someone forgot to add, schema-as-code is the safer default.

**Advantage: WordPress on autonomy; Payload on governance.** For this project, governance wins — see §16.3 for the condition that reverses it.

---

## 5. Plugin deep-dive: ACF Pro vs. Payload native fields

### 5.1 What ACF Pro provides

ACF Pro is the reason WordPress can behave like a structured CMS at all. Field groups, conditional logic, a large field-type library, Repeater and Flexible Content, and a genuinely excellent editing UX. It is mature, well-documented and widely known.

### 5.2 The storage problem

ACF stores field values in **`wp_postmeta`**, and this is where it strains at content-platform scale:

- **Repeater and Flexible Content write one row per field per row.** A procedure with 8 fields × 10 repeater rows is 80+ meta rows for one document.
- **Meta queries scan `wp_postmeta`.** Meta keys are not strictly typed and values can hold anything from JSON to URLs, so a `meta_query` scans across potentially millions of rows. Filtering, sorting and reporting degrade.
- **Indexing options are limited**, which is exactly what "find all articles reviewed by Dr. X, published in the last year, tagged cardiology" needs.
- **Flexible Content loads everything in the editor.** The admin loads *every* row and *every* sub-field on page load — the documented failure mode for exactly the shape a composable page needs.
- The vendor's own remedy is **moving ACF fields into custom database tables**, which is an admission that the default storage model does not scale for query-heavy content.

Note the contrast the ACF ecosystem itself draws: native Gutenberg blocks and ACF Blocks store values in `post_content`, avoiding the extra queries — but Flexible Content does not.

### 5.3 The Payload equivalent

Fields are declared in the collection and become **real relational columns and child tables**. From the POC's `Doctors.ts`:

```ts
{
  name: 'consultationHours',
  type: 'array',
  fields: [{
    type: 'row',
    fields: [
      { name: 'day', type: 'select', required: true, options: [...DAYS], admin: { width: '40%' } },
      { name: 'startTime', type: 'text', required: true, admin: { width: '30%' } },
      { name: 'endTime',   type: 'text', required: true, admin: { width: '30%' } },
    ],
  }],
}
```

That array produced a dedicated `doctors_consultation_hours` table (25 rows in the current POC database) plus `_doctors_v_version_consultation_hours` for the versioned copy. Queries hit indexed relational columns, not a key-value scan.

### 5.4 Field-type parity

| Field type | ACF Pro | Payload native |
|---|---|---|
| Text / textarea / number / email | ✅ | ✅ |
| WYSIWYG / rich text | ✅ TinyMCE | ✅ Lexical (extensible, JSON) |
| Select / radio / checkbox | ✅ | ✅ |
| Date / time picker | ✅ | ✅ |
| Image / file | ✅ | ✅ upload |
| Relationship / post object | ✅ | ✅ relationship |
| **Reverse relationship** | ❌ needs custom query | ✅ **`join` field, virtual** |
| Repeater | ✅ | ✅ `array` |
| Flexible Content | ✅ | ✅ `blocks` |
| Group / tabs / accordion | ✅ | ✅ group / tabs / collapsible |
| Conditional logic | ✅ | ✅ `admin.condition` |
| Colour picker | ✅ | 🟡 text or custom component |
| Google Map | ✅ | 🟡 point field (not on SQLite) |
| oEmbed | ✅ | 🟡 model as typed block |
| Clone field | ✅ | ✅ export a field array and reuse |
| **Field-level access control** | ❌ | ✅ per-field create/read/update |
| **Field-level hooks** | 🟡 filters | ✅ `beforeValidate` etc. |
| **Generated TypeScript types** | 🟡 third-party generators | ✅ built in |

Two entries deserve emphasis.

**The `join` field has no clean ACF equivalent.** In the POC, `Departments.doctors` is a virtual join on `Doctors.department` — doctors own the relationship, departments surface them automatically, no duplicated data. It renders in the admin as a sortable, column-configurable table. In ACF you either duplicate the relationship on both sides and keep them in sync, or hand-write reverse queries against `wp_postmeta`.

**Field-level access control has no ACF equivalent at all.** Payload can permit an agent identity to write a draft body but forbid it from touching the canonical URL or the reviewer relationship. ACF has no such concept.

### 5.5 Where ACF genuinely wins

- **Editing UX is more polished** in places, particularly the WYSIWYG and the map field.
- **Field groups can be created without a deploy** — the §4 autonomy argument again.
- **`clone` and field-group reuse** are more ergonomic than exporting TypeScript arrays.
- **Enormous community knowledge.** Almost any ACF problem has been solved publicly.

### 5.6 Verdict

For a brochure site, ACF is excellent and the storage critique is academic. For **hundreds of clinical articles with faceted filtering, reverse relationships and reporting**, `wp_postmeta` is the wrong data structure — and ACF's own documentation points you to custom tables as the fix.

**Advantage: Payload**, on storage model, reverse relations, field-level access control and type generation. WordPress retains the no-deploy advantage.

---

## 6. Plugin deep-dive: Elementor Pro vs. Payload blocks → React

### 6.1 What Elementor buys

Genuine freedom, and it should not be dismissed. A marketer can build an arbitrary landing page in an afternoon with a true WYSIWYG canvas, no developer, no deploy, and thousands of templates to start from. **With the design question set aside, this is a substantial part of WordPress's speed-to-launch advantage.**

### 6.2 What it costs, quantified

| Metric | Elementor | Baseline | Source |
|---|---|---|---|
| DOM elements per page | **1,500–3,000** (wrapper divs) | 200–400 (Bricks) | benchmarks |
| Added frontend assets | **200–400 KB** extra CSS/JS | — | benchmarks |
| CSS/JS payload multiplier | **3–5×** vs. block editor | 1× | benchmarks |
| Installed code footprint | **> 21 MB** unzipped | — | benchmarks |
| **CWV pass rate** | **25–35%** | WP average 33–40%; Bricks 55–65% | benchmarks |
| Median mobile LCP (unoptimised) | **3.8–5.2 s** | — | benchmarks |

Two fair mitigations:

- Elementor's **new single-DIV wrapper system reduces DOM output by up to 40%** — the biggest performance change it has shipped in years.
- Disciplined optimisation recovers **50–70%** of the penalty.

But note where that leaves you: Elementor's *starting* CWV pass rate sits **below the WordPress average**, and optimisation is ongoing engineering effort spent clawing back a self-inflicted cost.

### 6.3 The deeper problem: content lock-in

Elementor stores layouts as **serialised data in `wp_postmeta`**. That has consequences beyond speed:

- Content is entangled with presentation. Migrating away means parsing Elementor's format.
- It is not meaningfully queryable. You cannot ask "which pages use the testimonial section".
- **Elementor and ACF Flexible Content are competing answers to the same question.** Running both means two page-building paradigms and unclear ownership of layout — a real governance problem on a team.

### 6.4 The Payload equivalent

A `blocks` field is a discriminated union of typed section variants. Each block maps 1:1 to a React component:

```ts
// Pages.ts
{
  name: 'layout',
  type: 'blocks',
  blocks: [HeroBlock, IntroBlock, SpecialtyGridBlock, ProcedureGridBlock,
           ClinicianGridBlock, ArticleFeedBlock, EvidenceBlock,
           TestimonialBlock, FaqBlock, CtaBlock, InquiryFormBlock],
}
```

```tsx
// rendered with a typed switch — no serialised blob
{page.layout?.map((block) => {
  switch (block.blockType) {
    case 'heroBlock':          return <Hero {...block} key={block.id} />
    case 'clinicianGridBlock': return <ClinicianGrid {...block} key={block.id} />
    // …
  }
})}
```

Editors get a constrained palette of approved sections. Developers get typed props. The output DOM is exactly what the component author wrote — no wrapper-div tax.

A block set for a clinical content platform would plausibly cover: hero, intro, specialty grid, procedure grid, clinician grid, article feed, evidence/research list, testimonials, FAQ (which doubles as `FAQPage` schema), CTA, and an enquiry form. The POC already implements the enquiry-form equivalent end to end — public form → server action → Local API → admin triage, verified working.

### 6.5 Head-to-head

| Capability | Elementor Pro | Payload blocks | Advantage |
|---|---|---|---|
| **Free-form visual layout** | ✅ **drag anything anywhere** | ❌ approved blocks only | **WordPress** |
| **Live visual editing** | ✅ **true WYSIWYG canvas** | 🟡 live preview iframe | **WordPress** |
| **Template library to start from** | ✅ **thousands** | ❌ build your own | **WordPress** |
| Non-developer page creation | ✅ | ✅ (from existing blocks) | Even |
| **New section type without a developer** | ✅ | ❌ | **WordPress** |
| Design-system enforcement | ❌ editors can break brand | ✅ blocks constrain output | Payload |
| DOM output control | ❌ 1,500–3,000 nodes | ✅ exactly what you author | **Payload** |
| Frontend payload | +200–400 KB | component cost only | **Payload** |
| Content queryable | ❌ serialised meta | ✅ typed relational rows | Payload |
| Migration risk | ⚠️ proprietary format | ✅ plain JSON structures | Payload |
| Licence | **$199/yr** | free (MIT) | Payload |

### 6.6 Verdict

Elementor buys real freedom and charges for it in DOM weight, CWV, lock-in and licence fees.

**That trade was defensible for a booking site with twenty pages. It is much harder to defend for a content platform whose entire value is organic reach**, because the DOM tax is paid on every indexed page and now damages AI extraction as well as speed (§10.4).

**Advantage: Payload for this use case** — while conceding that Elementor's template library and free-form canvas are a genuine launch-speed advantage that Payload does not match.

---

## 7. Plugin deep-dive: Yoast / Rank Math vs. `plugin-seo` + `generateMetadata`

**This is WordPress's clearest and most legitimate win. Do not spin it.**

### 7.1 What the WordPress plugins provide

**Rank Math** ships a **Schema Builder** with drag-and-fill authoring and live preview — 40+ schema types in Pro, 20+ in the free tier (sources differ on the exact free count; verify against current docs before quoting). Plus redirect management, 404 monitoring, readability analysis and automatic sitemaps.

**Yoast** takes a different and technically elegant approach: it generates schema **automatically as a connected entity graph** — pages, authors and the site linked as entities, which is the shape Google recommends. Article for posts, WebPage for pages, Person/Organization for authors, without manual configuration.

Both give editors a live SERP preview and a content-scoring workflow that non-technical staff genuinely use.

### 7.2 What Payload provides

`@payloadcms/plugin-seo` adds a `meta` field group — title, description, image — with a real-time search-engine preview and character counters. It supports:

- `generateTitle`, `generateDescription`, `generateImage` — derive metadata from document content
- `generateURL` — render the true URL in the preview
- `tabbedUI` — append an SEO tab to the collection
- extensible `fields` for custom entries such as `og:title` or a JSON-LD field

**What it does not do — state this plainly:** the plugin does **not** generate JSON-LD, sitemaps or redirects. Those are separate work.

On the Next.js side you get `generateMetadata()` for full programmatic control of every tag on dynamic routes, `app/sitemap.ts` and `app/robots.ts` generated from Payload data, and JSON-LD injected as a `<script type="application/ld+json">` in the page component. Payload's official **redirects** plugin covers redirect management.

### 7.3 Technical SEO head-to-head

| Capability | Rank Math / Yoast | Payload + Next.js | Advantage |
|---|---|---|---|
| Editable meta title/description | ✅ excellent UI | ✅ SEO plugin | Even |
| Live SERP preview | ✅ mature | ✅ plugin provides one | Even |
| **Readability / SEO scoring** | ✅ **signature feature** | ❌ absent | **WordPress** |
| **Visual schema builder** | ✅ **Rank Math, 40+ types** | ❌ hand-written | **WordPress** |
| **404 / broken-link monitoring** | ✅ Rank Math | ❌ external tooling | **WordPress** |
| Automatic entity graph | ✅ **Yoast** | ❌ build it | **WordPress** |
| XML sitemap | ✅ automatic | ✅ `app/sitemap.ts` from Payload | Even |
| robots.txt | ✅ UI | ✅ `app/robots.ts` | Even |
| Redirects | ✅ Rank Math built-in | ✅ official redirects plugin | Even |
| Canonical URLs | ✅ | ✅ `generateMetadata` | Even |
| OG / Twitter cards | ✅ | ✅ Metadata API | Even |
| Breadcrumbs + schema | ✅ | 🟡 nested-docs plugin + custom | WordPress |
| hreflang | ✅ with WPML | 🟡 custom from locales | WordPress |
| **Programmatic control of every tag** | 🟡 filters, plugin-mediated | ✅ **full control** | Payload |
| **Schema guaranteed by data model** | ❌ editor free-text | ✅ typed relationships | **Payload** |

### 7.4 The counter-argument, and why it decides this section

Rank Math ships schema faster. That is true and it matters.

But medical schema is not a checkbox. The `reviewedBy` property on `MedicalWebPage` is the **credentialing chain** that Google's quality systems and AI citation models use to assess trustworthiness. Its value depends entirely on whether the underlying data is *reliable*.

- **In WordPress:** `reviewedBy` is a schema field an editor types into. It can be left blank, filled with a name that matches no real clinician, or copy-pasted wrongly. Nothing structurally prevents it.
- **In Payload:** `reviewedBy` is generated from a **required relationship to a credentialed clinician record**, and access control prevents publishing without it. The JSON-LD generator cannot emit a reviewer that does not exist.

For YMYL content, a hand-written JSON-LD generator backed by a guaranteed relationship beats a beautiful builder backed by free text. **You write the generator once**, covering `MedicalWebPage`, `Article`, `Physician`, `MedicalProcedure`, `Organization` and `BreadcrumbList`.

### 7.5 Verdict

**Advantage: WordPress on tooling velocity — genuinely, and by a clear margin.** Budget explicitly for the gap: you will hand-write JSON-LD, and you will lose readability scoring and 404 monitoring (replace with Screaming Frog, Ahrefs or Search Console rather than pretending the gap is not there).

**Advantage: Payload on schema *reliability***, which is the axis that matters for clinical content.

---

## 8. Plugin deep-dive: Smush / ShortPixel vs. native `sharp` variants

### 8.1 The WordPress plugins

**Smush** — free tier compresses, lazy-loads and offers a CDN. Its algorithm is **less aggressive** than competitors, and **WebP/AVIF conversion is Pro-only**.

**ShortPixel** — generally considered the strongest option in 2026: better compression, local WebP and AVIF, 100 free images per month, then paid.

Both work the same way: a plugin intercepts uploads, generates derivatives and rewrites URLs. Optimisation is **on-demand** — the first visitor triggers processing, subsequent requests serve from cache.

### 8.2 The Payload equivalent — already built in the POC

`sharp` is a Payload dependency, not a plugin. Derivatives are declared in the collection:

```ts
// src/collections/Media.ts — verbatim from the POC
upload: {
  staticDir: path.resolve(dirname, '../../media'),
  mimeTypes: ['image/*'],
  focalPoint: true,
  crop: true,
  imageSizes: [
    { name: 'thumbnail', width: 400,  height: 300, position: 'centre' },
    { name: 'card',      width: 768,  height: 576, position: 'centre' },
    { name: 'hero',      width: 1920, height: 800, position: 'centre' },
  ],
}
```

Measured in the POC: **18 media documents produced 60 files** — larger images get all three sizes plus the original, while 600×600 avatars skip the larger `hero` size. Generating all 60 took roughly **7 seconds** during seeding.

On the delivery side, Next.js runs images through `sharp` for a **40–70% size reduction**, with WebP/AVIF conversion saving a further **25–35%** — combined **60–80%** smaller payloads. `sharp` benchmarks roughly **25× faster than squoosh-cli**.

### 8.3 Head-to-head

| Capability | Smush / ShortPixel | Payload + `sharp` | Advantage |
|---|---|---|---|
| Automatic derivative generation | ✅ | ✅ declarative `imageSizes` | Even |
| WebP / AVIF | 🟡 **Smush: Pro only**; ShortPixel: yes | ✅ via `next/image` | Payload |
| Compression quality | ✅ ShortPixel strongest | ✅ `sharp`, configurable | Even |
| **Cost** | **paid tier for WebP/AVIF** | **free** | **Payload** |
| Focal point / crop UI | 🟡 plugin-dependent | ✅ native | Payload |
| Bulk re-optimise existing library | ✅ **mature UI** | 🟡 script | **WordPress** |
| **Media library UX** | ✅ **better** | 🟡 adequate | **WordPress** |
| Asset folders / tagging | ✅ mature plugins | ✅ official Folders/Tags collections | Even |
| CDN offload | ✅ bundled | ✅ cloud-storage adapter plugins | Even |
| Third-party runtime code | ⚠️ yes | ✅ none | Payload |
| Derivatives declared in version control | ❌ plugin settings | ✅ in the collection config | Payload |

### 8.4 Video — neither platform should self-host

| Capability | WordPress | Payload |
|---|---|---|
| Self-hosting MP4s | ❌ never | ❌ never |
| Structured video relation | 🟡 ACF oEmbed | ✅ typed provider block |
| Transcripts as structured content | 🟡 custom field | ✅ typed field |

**Recommendation for both platforms:** use Mux or Cloudflare Stream and model the asset as a typed block with `provider`, `playbackId`, `poster`, `captions`, `transcript`. **Transcripts are not optional** — they are simultaneously an accessibility requirement and the only way video becomes citable by answer engines.

### 8.5 Verdict

**Advantage: Payload on cost and configuration-as-code; WordPress on library UX and bulk re-optimisation.** This is the most evenly matched of the five plugin comparisons and the smallest factor in the decision. Note that we removed Payload's official Folders/Tags collections from the POC for demo clarity — **restore them** for a real content platform.

---

## 9. Dynamic URLs, slugs and routing

A content platform lives or dies on URL structure. This deserves its own treatment.

### 9.1 WordPress

Permalinks are configured globally and per-post-type via the `rewrite` argument. Strengths and sharp edges:

- ✅ Mature, well-understood, with an established plugin ecosystem for redirects.
- ✅ Editors control slugs directly in the editor.
- ⚠️ **Rewrite rules must be flushed** when post types or taxonomies change, or URLs 404 (§4.1).
- ⚠️ Hierarchical URLs across *different* post types (e.g. `/procedures/orthopaedics/prp-therapy`) require custom rewrite rules — a known source of conflicts.
- ⚠️ Slug collisions across post types sharing `wp_posts` need explicit handling.

### 9.2 Payload + Next.js

Routing is Next.js file-system routing; slugs are collection fields. The POC already implements a reusable slug field:

```ts
// src/fields/slugField.ts — auto-derives from a source field, editor can override
export const slugField = (sourceField = 'title'): Field => ({
  name: 'slug',
  type: 'text',
  required: true, unique: true, index: true,
  admin: { position: 'sidebar' },
  hooks: { beforeValidate: [deriveSlug(sourceField)] },
})
```

`unique: true` and `index: true` are enforced by the **database**, not by convention. For hierarchy, the official **nested-docs** plugin adds a `parent` field and an automatic `breadcrumbs` array with `label` and `url`, with a `generateURL` function producing full paths — and **recursive updates**: editing a great-grandparent updates every descendant's breadcrumbs automatically.

### 9.3 Head-to-head

| Capability | WordPress | Payload + Next.js | Advantage |
|---|---|---|---|
| Editor-editable slug | ✅ | ✅ sidebar field | Even |
| Auto-slug from title | ✅ | ✅ `beforeValidate` hook | Even |
| **Uniqueness enforced** | 🟡 auto-suffixed | ✅ **DB unique index** | Payload |
| Indexed for lookup | 🟡 | ✅ explicit `index: true` | Payload |
| Hierarchical URLs | 🟡 custom rewrite rules | ✅ nested-docs plugin | Payload |
| Breadcrumbs auto-maintained | 🟡 plugin | ✅ recursive descendant updates | Payload |
| **Rewrite flush needed** | ⚠️ **yes** | ❌ n/a | **Payload** |
| Redirect management UI | ✅ **Rank Math** | ✅ official redirects plugin | Even |
| Arbitrary route patterns | 🟡 rewrite API | ✅ file-system routing | Payload |
| Preview of unpublished URL | ✅ | ✅ draft mode + live preview | Even |
| Localised URLs | ✅ WPML (paid) | ✅ native field-level localisation | Payload |

### 9.4 Verdict

**Advantage: Payload.** Database-enforced uniqueness, no rewrite-flush class of bug, and recursive breadcrumb maintenance are meaningful at hundreds of documents. WordPress retains the better redirect UI.

---

## 10. Performance and Core Web Vitals

### 10.1 Platform field data

| Metric | Figure | Source |
|---|---|---|
| WordPress origins passing all three CWV | **46.28%** | HTTP Archive, Nov 2025 |
| All tracked origins passing all three CWV | **55.9%** | CrUX, May 2026 (18.4M origins) |
| Good LCP / CLS / INP across all origins | 68.6% / 81.3% / 86.6% | CrUX, May 2026 |
| WordPress INP pass rate | **85.89%** | CrUX |
| Sites with TTFB < 200 ms passing LCP | **~73%** | CrUX |

Read this carefully and fairly: **WordPress's INP is fine.** Interactivity is not the problem. WordPress underperforms on **LCP and loading** — TTFB from per-request PHP execution, plus plugin-layered CSS/JS.

### 10.2 The compounding factor

Add Elementor's contribution from §6.2 — a **25–35% CWV pass rate**, *below* the 33–40% WordPress average, and 3–5× the CSS/JS payload.

The honest counterpoint, which should be conceded: *a well-built WordPress site with a lightweight theme and disciplined image handling can pass comfortably; a Next.js site stuffed with third-party scripts can fail.* **The platform tilts the odds; the build decides the outcome.**

But the pivot changes how much those odds matter. A booking page's speed affects one conversion. A content platform's speed affects **crawl budget, indexation depth and AI citation eligibility across hundreds of articles** — it compounds.

### 10.3 What we measured in our own POC

> **Scope warning: these are development-mode figures and are NOT production benchmarks. No production build has been benchmarked. Do not quote these as evidence of production performance.**

| Measurement | Result |
|---|---|
| Dev server cold boot | ~1.6 s (Turbopack) |
| Landing page, warm dev render | ~1.5–2.1 s (dev mode, `force-dynamic`, unoptimised) |
| Seed 18 media docs → 60 derivatives | ~7 s |
| SQLite database size | 434 KB |
| Typecheck + lint | clean |

The POC deliberately uses `force-dynamic` (no caching) so publish-then-refresh is visible during demos, and plain `<img>` rather than `next/image`. **Both must change before any performance claim is made.** Production should use ISR with on-demand revalidation from an `afterChange` hook (§18.2).

### 10.4 Answer Engine Optimisation — where DOM weight becomes an SEO liability

Patients increasingly begin in ChatGPT, Perplexity and AI Overviews before clicking any link, and every major AI platform applies its own YMYL evaluation to health content.

AEO rewards clean semantic HTML, low DOM depth, reliable structured data and server-rendered content. This is precisely where **Elementor's 1,500–3,000 DOM nodes stop being merely a speed problem and become an extraction problem** — deeply nested wrapper divs make content harder to parse for the systems now mediating patient discovery.

**Advantage: Payload**, on the ground that matters most after the pivot.

---

## 11. Security attack surface

### 11.1 The WordPress ecosystem, quantified

From Patchstack's *State of WordPress Security in 2026* and corroborating sources:

| Finding | Figure |
|---|---|
| New ecosystem vulnerabilities (2025) | **11,334** (+42% YoY) |
| Share located in **plugins** | **91%** |
| Share in themes | 9% |
| Share in **core** | **6 total, all low risk** |
| Plugin vulnerabilities disclosed per week | **250+** (~36/day) |
| Exploited within 6 hours of disclosure | 20% |
| Exploited within 24 hours | 45% |
| Exploited within 7 days | 70% |
| **Weighted median time to first exploitation** | **5 hours** |
| **Disclosed with no developer patch available** | **46%** |
| Growth in highly exploitable vulnerabilities | **+113% YoY** |

**Read these numbers precisely, because the naive reading is wrong.** WordPress *core* has an excellent security record — six low-risk issues in a year. The risk is almost entirely the **plugin supply chain**.

Our proposed WordPress stack is **five** independently-maintained codebases with database access running inside the admin. When one is disclosed, you have a median of five hours and a 46% chance no patch exists yet.

### 11.2 Surface comparison

| Vector | WordPress stack | Payload 3.x |
|---|---|---|
| Third-party runtime code with DB access | **5+ plugins** | **none** — no runtime plugin marketplace |
| Admin login exposure | `/wp-login.php`, universally botted | `/admin`, standard Next.js route |
| Dependency update model | runtime, per-plugin, urgent | build-time npm, tested in CI, deployed |
| Unauthenticated surface | XML-RPC, REST, admin-ajax, plugin endpoints | Payload REST/GraphQL under access control |
| Privilege escalation | recurring plugin CVE class | access control in code, typed, reviewable |
| **Page injection / SEO spam** | documented plugin CVE class | requires code + deploy access |
| File upload handling | plugin-dependent | `mimeTypes` restricted, executables blocked |
| Supply chain | plugin marketplace | npm (real, but audited at build time) |
| Compliance attestations | n/a (self-hosted) | **none from Payload** — provider's BAA |

### 11.3 Fair qualifications — do not over-claim this

- **Payload is not inherently secure.** It holds no SOC 2 Type II, ISO 27001 or HIPAA BAA. Self-hosting shifts responsibility to your cloud provider.
- **npm is a real supply chain risk.** The difference is timing and control: you upgrade deliberately, test in CI and deploy — versus patching a live site inside a five-hour window.
- **Managed WordPress hosting with a WAF and virtual patching materially reduces exposure.** Patchstack's 2026 report nonetheless found hosting defences block only a fraction of exploits.
- **A smaller ecosystem means fewer researchers looking.** Payload's low CVE count is partly genuine architecture and partly lower scrutiny.

**Advantage: Payload — the strongest single argument in this document.**

---

## 12. AI agent readiness — MCP vs. WP REST

> **Correct a likely misconception before it reaches management: WordPress is not behind on AI in 2026.**

### 12.1 Both platforms ship MCP

**WordPress:** Automattic's standalone `Automattic/wordpress-mcp` plugin was **archived on GitHub on 2026-01-19**. The supported path is now the official **`WordPress/mcp-adapter`**, which bridges the **WordPress 6.9 Abilities API** to MCP, exposing abilities as MCP tools, resources and prompts. Common tools cover drafting/publishing/updating posts, querying by topic/status/author/date, taxonomy and metadata operations, and maintenance tasks. WordPress also ships an AI Client in core for outbound provider calls, plus a connector UI. *Any tutorial referencing the archived Automattic plugin is stale.*

**Payload:** the official `@payloadcms/plugin-mcp` auto-generates find/create/update/delete tools per collection, plus find/update for globals, and supports custom tools, prompts and resources.

The useful framing: **the REST API is a set of endpoints a developer must know about and write code against; an MCP server sits on top and describes those capabilities so an AI can discover and use them autonomously.** Both platforms now offer that layer. This is genuinely even.

### 12.2 Where the real difference lies

Both let an agent call tools. The question is **what happens when a compromised or prompt-injected agent calls them.**

This is not hypothetical for this project. `PROJECT_BRIEF.md` §4 specifies a **Competitor Intelligence Agent that reads untrusted competitor websites**, feeding a **Marketing/SEO Agent that drafts articles**. That is a direct prompt-injection path into the publishing pipeline — and §2 of the same brief names **"SEO spam poisoning"** as a threat. **The pivot increases this risk, because content volume is now the point.**

**Payload's structural answer.** Each agent gets a Payload user and an MCP API key. The plugin enforces access control **as the user tied to that key**, so this rule makes publishing impossible at the data layer:

```ts
update: ({ req }) => isAgent(req.user)
  ? { _status: { equals: 'draft' } }   // returns a QUERY — cannot publish
  : true
```

The constraint is merged into every query Payload builds for that identity — through REST, GraphQL, the admin UI and MCP alike — so a hijacked agent's publish attempt matches nothing. Revoke one key without touching the others. Every write is a version row attributed to that agent.

**Be precise about what this is.** This is *application-layer* enforcement — the same category as a controller check — not a database constraint. Payload builds the query; Postgres enforces nothing here. The giveaway is that the Local API defaults `overrideAccess` to `true`, which skips access control entirely. Anything that bypasses Payload — direct SQL, a migration script, or Local API code that forgets `overrideAccess: false` — is not covered.

The advantage over hand-written controllers is therefore **coverage, not strength**: one declaration on the collection, versus the same check repeated on every endpoint that touches it — each a place to forget one. A disciplined team with a service layer and route guards achieves the same property, and WordPress's `map_meta_cap` filters and REST `permission_callback` are the same category. For a genuinely harder boundary you would need Postgres row-level security, triggers, or per-identity database roles — none of which drop in cleanly, since Payload connects as a single database user.

**WordPress's answer** is capability checks in PHP, mediated by whichever plugins are installed. Correct configuration is achievable; it is not structurally guaranteed, and it sits atop the plugin surface quantified in §11.

### 12.3 Head-to-head

| Capability | WordPress 7.0 | Payload 3.88 | Advantage |
|---|---|---|---|
| MCP server | ✅ official MCP Adapter | ✅ official `plugin-mcp` | Even |
| Ability/tool discovery | ✅ Abilities API (6.9+) | ✅ auto CRUD per collection | Even |
| **Outbound AI provider calls** | ✅ **AI Client in core** | 🟡 your own code | **WordPress** |
| **Agent connector UI** | ✅ **Settings → Connectors** | 🟡 API-key screen | **WordPress** |
| Typed schema as agent context | 🟡 REST schema, loosely typed | ✅ typed collections + generated types | Payload |
| **Agent inherits access control** | 🟡 capability checks, plugin-dependent | ✅ **enforced as the key's user** | **Payload** |
| Per-agent scoped identity | 🟡 application passwords | ✅ user + API key per agent | Payload |
| **Query-level write restriction** | ❌ | ✅ **`Where`-returning access control** | **Payload** |
| Long-running agent loops | 🟡 WP-Cron (unreliable) or external | ✅ **jobs queue: tasks, workflows, retry-from-failure** | **Payload** |
| Audit trail of agent writes | 🟡 plugin | ✅ versions carry the agent's user | Payload |

### 12.4 Provenance tainting — required on either platform

Tag content by source class (`untrusted-external`, `internal`, `clinician-authored`), **set in the ingestion layer rather than trusting the agent's self-report**, and require clinical approval for anything touched by untrusted provenance. Separation of duties: the agent that proposes must never be an approver.

**Advantage: Payload** — not because WordPress lacks agent tooling (it does not), but because Payload's guarantees are *enforced* rather than *configured*.

---

## 13. Editorial governance and clinical credentialing

### 13.1 Medical E-E-A-T requirements

2026 healthcare SEO consensus: content must be written or reviewed by qualified professionals, with credentials, degrees and affiliations displayed and reinforced by author schema. Author bylines plus "medically reviewed by" credentials are repeatedly cited as **the single biggest healthcare E-E-A-T signal**.

| Requirement | WordPress | Payload |
|---|---|---|
| Author credentials as structured data | 🟡 ACF fields on user/CPT | ✅ `clinicians` collection, typed |
| Medical reviewer distinct from author | 🟡 custom ACF field | ✅ separate required relationship |
| **Reviewer must be credentialed** | ❌ **free text, unenforceable** | ✅ **relationship to a real record** |
| Review date tracked | 🟡 custom field | ✅ field + version history |
| **Cannot publish without reviewer** | ❌ needs a workflow plugin | ✅ **access control / `beforeChange`** |
| Credentials render consistently | 🟡 template work | ✅ typed component, one source |

### 13.2 The mechanism, verified in the POC

Payload's `update` access control can return a **query** rather than a boolean, and the constraint merges into the database query itself:

```ts
export const publishedOrAuthenticated: Access = ({ req: { user } }) =>
  user ? true : { _status: { equals: 'published' } }
```

Measured in the POC (`PROJECT_DETAILS.txt` §13):

- With a doctor saved as draft: anonymous `/api/doctors` returned **11**; the rendered HTML contained **0** occurrences of the name.
- After publishing: **12** and **1**.
- Editing produced **3 version rows** with correct status transitions (`draft → published → published`); restoring a prior version reverted the field.
- Anonymous `GET /api/inquiries` → **403**; anonymous `POST` → **201** (public form works by design); authenticated `GET` → **200**.

The access rule even reaches inside the `join` field's count: General Medicine displays "1 CONSULTANT" on the public site although it has two doctors, because one is a draft.

WordPress can reach a similar outcome with an editorial-workflow plugin — which is a sixth plugin, and returns you to §11.

**Advantage: Payload.**

---

## 14. Cost of ownership

| Item | WordPress stack | Payload |
|---|---|---|
| CMS licence | free (GPL) | free (MIT) |
| Elementor Pro | **$199/yr** | — |
| Yoast Premium *or* Rank Math Pro | **$99/yr** or **$83.88/yr** | — |
| ACF Pro | paid annual licence — *verify current tier* | — |
| CPT UI | free | — |
| Smush Pro (needed for WebP/AVIF) | paid tier | — |
| **Recurring licences** | **≈ $400–500/yr, renewing** | **$0** |
| Hosting | managed WP, mid-tier | Node host + Postgres |
| Security maintenance | **continuous, urgent, unschedulable** | periodic, scheduled |
| **Time to first launch** | **weeks (theme + plugins)** | **longer — components first** |
| Build — schema | **lower (UI-driven)** | higher (code) |
| Build — SEO schema | **lower (Rank Math)** | higher (hand-written) |
| Build — editorial workflow | higher (plugin/custom) | **lower (native)** |
| Specialist hiring | **easy, cheap** | harder, pricier |

Licence cost is not decisive at this scale. The real economics are **security maintenance labour** — recurring, urgent, unschedulable — versus **higher initial build cost**, which is one-off and plannable.

**Be honest that WordPress launches sooner.** The case for Payload is that a slower, plannable build buys a lower ongoing risk and maintenance burden, on a platform where a defacement is a reputational event.

---

## 15. Scorecard

| Requirement | WordPress stack | Payload 3.x | Winner |
|---|---|---|---|
| Content types (CPT UI vs collections) | 8/10 | 8/10 | Even |
| Custom fields (ACF vs native) | 7/10 | 9/10 | Payload |
| Page building (Elementor vs blocks) | 7/10 | 9/10 | Payload |
| SEO tooling (Rank Math vs plugin-seo) | **9/10** | 6/10 | **WordPress** |
| Schema reliability | 5/10 | 9/10 | **Payload** |
| Images (Smush vs sharp) | 8/10 | 8/10 | Even |
| Dynamic URLs and routing | 7/10 | 9/10 | Payload |
| Clinical credentialing | 5/10 | 9/10 | **Payload** |
| Editorial governance | 6/10 | 9/10 | Payload |
| AI agent readiness | 7/10 | 9/10 | Payload |
| **Security** | **3/10** | **8/10** | **Payload** |
| Performance / CWV | 4/10 | 9/10 | Payload |
| **Time to first launch** | **9/10** | **5/10** | **WordPress** |
| **Editor autonomy** | **9/10** | **4/10** | **WordPress** |
| **Hiring / handover** | **9/10** | **5/10** | **WordPress** |
| TCO (3-year) | 6/10 | 8/10 | Payload |

Scores are judgement calls informed by the cited data, not measurements. They exist to make the *shape* of the trade-off legible: **WordPress wins launch speed, SEO tooling, editor autonomy and hiring; Payload wins structure, governance, routing, performance, agent safety and security.**

---

## 16. Architectural verdict

**Build the RegenCare content platform on Payload CMS 3.88.0, extending the existing POC.**

### 16.1 The reasoning in four sentences

1. On plugin capability the two stacks are near-even — two wins each and one tie — so the decision is made by what sits outside the plugins (§1.1).
2. Adopting five plugins means adopting the surface behind **91% of 11,334 annual vulnerabilities**, with a five-hour median exploitation window and a 46% chance of no available patch (§11.1).
3. Clinical YMYL content requires a *guaranteed* credentialing chain, and Payload enforces `reviewedBy` as a required relationship to a credentialed record rather than as text an editor may leave blank (§7.4, §13).
4. `wp_postmeta` storage and Elementor's DOM weight are survivable at twenty pages and structural at several hundred — and several hundred is now the target (§5.2, §6.2, §10.2).

### 16.2 Accept these costs explicitly

- **WordPress would launch sooner.** A theme plus five plugins is weeks; components are longer. This is a real cost, not a rhetorical one.
- **You will write JSON-LD by hand.** Rank Math's builder is better. Budget for it; write it once, generated from typed relationships.
- **Clinic staff cannot add content types.** Every schema change is a developer task and a deploy.
- **You lose readability scoring and 404 monitoring.** Replace with Screaming Frog, Ahrefs or Search Console — do not pretend the gap is absent.
- **Payload developers are harder to hire.** Document heavily; `PROJECT_DETAILS.txt` is the start.
- **Payload's media library is less pleasant.** Restore the official Folders/Tags collections.

### 16.3 The one finding that would reverse this

If the business requires **marketing staff to create and restructure content types without engineering involvement**, then WordPress + ACF Pro + CPT UI is the correct answer and this recommendation should be discarded.

Confirm this before build starts. It is the only identified requirement that flips the verdict, and it is a business question, not a technical one.

---

## 17. Target architecture

```
                    ┌─────────────────────────────────┐
                    │   Next.js 16 (App Router)       │
                    │   ISR + on-demand revalidation  │
                    │   generateMetadata + JSON-LD    │
                    └──────────────┬──────────────────┘
                                   │ Local API (in-process)
                    ┌──────────────┴──────────────────┐
                    │   Payload 3.x                   │
                    │   ┌───────────────────────────┐ │
                    │   │ pages (blocks)            │ │
                    │   │ articles → author,        │ │
                    │   │            medicalReviewer│ │
                    │   │ procedures ↔ conditions   │ │
                    │   │ specialties, clinicians   │ │
                    │   │ testimonials, locations   │ │
                    │   │ media, users              │ │
                    │   └───────────────────────────┘ │
                    │   drafts · versions · access    │
                    └──────┬──────────────┬───────────┘
                           │              │
                  ┌────────┴────┐   ┌─────┴──────────────┐
                  │ PostgreSQL  │   │ MCP plugin         │
                  │ + S3 media  │   │ per-agent API keys │
                  └─────────────┘   │ draft-only scope   │
                                    └─────┬──────────────┘
                                          │
                          ┌───────────────┴────────────────┐
                          │ Subagents (draft-only)         │
                          │ competitor intel · SEO drafts  │
                          │ → human publish gate           │
                          └────────────────────────────────┘

  Video → Mux / Cloudflare Stream (typed block, never self-hosted)
  PHI   → separate service. Never in the CMS.
```

---

## 18. Migration path

### 18.1 Immediate — before any new build

1. **`git init` and commit.** Nothing is version controlled yet.
2. Rebrand: the POC uses placeholder "Meridian Clinic"; the real brand is **RegenCare**.
3. **Confirm the §16.3 editor-autonomy question with the business.**

### 18.2 Foundation

4. SQLite → PostgreSQL, with generated migrations.
5. Media → S3 or equivalent via the official cloud-storage adapter.
6. Replace `force-dynamic` with ISR + `afterChange` revalidation; adopt `next/image`.
7. **Then** benchmark production for real and retire the dev-mode figures in §10.3.
8. Restore the Folders/Tags collections.
9. Add an email adapter.

### 18.3 Content platform

10. Build the collections, with `articles` carrying **required** `author` + `medicalReviewer` relationships.
11. Build the page block set (§6.4), starting from the enquiry-form block already working in the POC.
12. Establish the design-system tokens — colour, radius, type scale, spacing — as a `theme` global so editors get typed controls.
13. Hand-write the JSON-LD generator — `MedicalWebPage` with `reviewedBy` from the clinician relationship, plus `Article`, `Physician`, `MedicalProcedure`, `Organization`, `BreadcrumbList`.
14. `app/sitemap.ts` and `app/robots.ts` driven from Payload; add the official redirects plugin.
15. Video via Mux, with transcripts as structured content.
16. Restore the Playwright/Vitest harness and add real tests.

### 18.4 Agentic layer — last, not first

17. Agent users + per-agent MCP API keys.
18. Draft-only access control for agent identities.
19. Provenance tainting for untrusted external sources.
20. Review-queue admin view with dual editorial + clinical sign-off.

---

## 19. Sources

**Security**
- Patchstack, *State of WordPress Security in 2026* — https://patchstack.com/whitepaper/state-of-wordpress-security-in-2026/
- *Patchstack 2026 report: vulnerabilities up 42%* — https://wp-content.co/patchstack-wordpress-security-report-2026-vulnerabilities-rises-hosting-defenses-struggles/
- *250+ Weekly WordPress Plugin Vulnerabilities in 2026* — https://www.webmastered.com/blog/wordpress-plugin-vulnerabilities-exploitable/
- *Patchstack 2026: faster attacks, stealthier malware* — https://www.therepository.email/patchstacks-2026-wordpress-security-report-faster-attacks-stealthier-malware-inadequate-hosting-defences

**Performance**
- *Core Web Vitals Benchmarks 2026* — https://www.digitalapplied.com/blog/core-web-vitals-benchmarks-2026-pass-rate-reference
- *Core Web Vitals for WordPress: Optimization Guide (2026)* — https://www.corewebvitals.io/core-web-vitals/wordpress-guide
- *Elementor DOM Reduction: Enterprise Core Web Vitals* — https://fachremyputra.com/elementor-dom-reduction/
- *Next.js vs WordPress for SEO: 2026* — https://www.brandrums.com/blog/nextjs-vs-wordpress-for-seo-2026/

**SEO**
- *Rank Math vs Yoast, tested and compared 2026* — https://aioseo.com/rank-math-vs-yoast/
- *Yoast vs Rank Math: Complete 2026 Comparison* — https://www.ubitools.com/yoast-vs-rank-math-2026/
- Payload SEO plugin docs — https://payloadcms.com/docs/plugins/seo
- *Next.js SEO Guide 2026: App Router, CWV & Structured Data* — https://pagepro.co/blog/nextjs-seo/
- *Next.js SEO & Metadata API Guide 2026* — https://nextjslaunchpad.com/article/nextjs-seo-metadata-api-sitemaps-json-ld-og-images

**Fields, post types and page building**
- ACF, *WordPress Post Meta Query Performance Best Practices* — https://www.advancedcustomfields.com/blog/wordpress-post-meta-query/
- ACF, *How to Move ACF Fields into Custom Database Tables* — https://www.advancedcustomfields.com/blog/acf-fields-custom-database-tables/
- *ACF Flexible Content Field: Complete Guide* — https://wplake.org/blog/acf-flexible-field/
- *register_post_type()* — https://developer.wordpress.org/reference/functions/register_post_type/
- *flush_rewrite_rules()* — https://developer.wordpress.org/reference/functions/flush_rewrite_rules/
- *WordPress Custom Post Types: 2026 Developer Tutorial* — https://gatilab.com/wordpress-custom-post-types/

**Media**
- *The 7 Best WordPress Image Optimization Plugins in 2026* — https://wp-rocket.me/blog/best-image-optimization-plugins-wordpress/
- *WordPress image optimization plugins compared* — https://stackharbor.com/en/knowledge-base/wp-image-optimization-plugins-compared/
- *Install `sharp` to Use Built-In Image Optimization* — https://nextjs.org/docs/messages/install-sharp
- *Next.js Image Optimization: A Guide for Web Developers* — https://strapi.io/blog/nextjs-image-optimization-developers-guide

**AI agent readiness**
- *WordPress MCP: Connect AI Agents to Your Site (2026)* — https://smartwp.com/wordpress-mcp/
- *10 Best WordPress MCP Servers Compared (2026)* — https://instawp.com/best-wordpress-mcp-servers-compared/
- Payload MCP plugin — https://payloadcms.com/docs/plugins/mcp

**Payload capability references**
- Access control — https://payloadcms.com/docs/access-control/collections
- Drafts and versions — https://payloadcms.com/docs/versions/drafts
- Nested docs plugin — https://payloadcms.com/docs/plugins/nested-docs
- Fields overview — https://payloadcms.com/docs/fields/overview

**Internal**
- `PROJECT_BRIEF.md` — programme brief
- `PROJECT_DETAILS.txt` — POC documentation and verification results

---

*Performance figures in §10.1–10.2 are cited industry benchmarks. Figures in §10.3 are development-mode measurements of our own POC and are explicitly **not** production benchmarks. ACF Pro pricing was not verified and is left unquantified. Rank Math free-tier schema-type counts differ between sources and should be confirmed against current documentation before being quoted externally. The supplied design files were deliberately excluded from this analysis at the team's direction; see the scope note at the head of the document.*
