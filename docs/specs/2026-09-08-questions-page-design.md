# Questions Page: Design

## Context

TrenTorch-Web needs a page where a student sees their progress, browses the curriculum's modules and questions, and clicks through to an individual question's IDE window (built separately, by another dev; this spec covers only the navigation page in front of it).

Nothing backing this exists yet: no schema, no backend, no auth. This is the front-end-only first pass; the plan is to swap in a real API once the schema/backend work happens.

## Scope

In scope:
- A `/questions` route: profile + progress on the left, module/question list on the right
- A "Questions" button on the homepage linking to it
- Static local data seeded from the curriculum designed earlier in this project (Part 0 through Part 4)
- `shadcn-svelte` + `bits-ui`, components added one at a time, only what's actually used

Out of scope (explicitly, per the user):
- The individual question/IDE window itself (`/questions/[slug]`'s content) — another dev owns this; this page only needs to link to that route
- Real progress persistence (localStorage or a backend) — placeholder numbers for now
- Auth / real profile data

## Layout

Two columns, LeetCode-style:
- **Left, sticky sidebar**: profile card (avatar placeholder + name), progress summary (e.g. "12 / 200 completed" with a progress bar)
- **Right, main content**: module list grouped by Part (matching the curriculum's own Part 0 to Part 4 structure), each Part collapsible, each question a clickable row inside it

Grouped-by-Part over a flat list: once the full curriculum is seeded, this is 100+ questions, a flat list would be unscannable. Collapsible sections match how the curriculum is already structured.

## Components

Each small, single-purpose, reusable on its own:
- `ProfileCard.svelte`: avatar + name
- `ProgressSummary.svelte`: completed/total, wraps a `bits-ui` Progress primitive
- `ModuleSection.svelte`: one collapsible Part, wraps a `bits-ui` Accordion primitive
- `QuestionRow.svelte`: one clickable question, links to `/questions/[slug]`
- `DifficultyBadge.svelte`: small colored Easy/Medium/Hard badge

## Data shape

`src/lib/data/questions.ts`, a static array of Parts, each with Tracks, each with Questions:

```ts
interface Question {
	slug: string;
	title: string;
	difficulty: 'Easy' | 'Medium' | 'Hard';
	topics: string[];
}

interface Track {
	name: string;
	questions: Question[];
}

interface Part {
	id: string;
	title: string;
	tracks: Track[];
}
```

Seeded from the curriculum's Part 0 to Part 4 tracks and questions, plus the confirmed additions from the 200-item problem bank cross-check (GELU, Swish, InfoNCE, Triplet Loss, KL Divergence, Policy Gradient, GAE).

Progress numbers (`completed`/`total`) are hardcoded placeholders for now, computed from the static data's total question count.

## Dependencies added

- `shadcn-svelte` (CLI, dev-time only, no runtime footprint of its own)
- `bits-ui` (peer dependency shadcn-svelte's components need)
- Individual component additions only: Progress, Avatar, Accordion, Badge — nothing installed that isn't rendering something on this page

## Testing

Built and verified on a local dev server (`npm run dev`) before anything is deployed.
