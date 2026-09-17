import { browser } from '$app/environment';
import { SvelteSet, SvelteDate } from 'svelte/reactivity';
import { curriculum } from '$data/questions';
import { domainDefs, SKIP_ELIGIBLE_PART_ID } from '$data/roadmap-domains';
import { solved } from '$processes/progress-tracking/solved.svelte';

export interface RoadmapPartEntry {
	partId: string;
	skipped: boolean;
	position: number;
}

export interface RoadmapState {
	domainIds: string[];
	quizScore: { correct: number; total: number };
	// Advisory-only self-report; may hold the single "none of these" sentinel
	// value from the wizard's checklist steps. Never used to decide skips --
	// only the quiz score does that (self-report is too easy to over/under-
	// claim to trust for that).
	toolsKnown: string[];
	conceptsKnown: string[];
	parts: RoadmapPartEntry[];
	createdAt: string;
}

// The first store in this codebase to persist a structured object rather
// than a Set<string> of ids -- same readStorage/writeStorage/browser-guard
// skeleton as collapsed-sections.svelte.ts and solved.svelte.ts, just a
// plain $state<RoadmapState | null> instead of a SvelteSet.
const STORAGE_KEY = 'trentorch-active-roadmap';

function readStorage(): RoadmapState | null {
	if (!browser) return null;
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		return raw ? (JSON.parse(raw) as RoadmapState) : null;
	} catch {
		// localStorage unavailable or the stored value isn't valid JSON:
		// behave as if no roadmap is active rather than throw.
		return null;
	}
}

function writeStorage(state: RoadmapState | null) {
	if (!browser) return;
	try {
		if (state) localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
		else localStorage.removeItem(STORAGE_KEY);
	} catch {
		// Same as above: the active roadmap just won't persist across visits.
	}
}

let current = $state<RoadmapState | null>(readStorage());

export const activeRoadmap = {
	get value(): RoadmapState | null {
		return current;
	},

	// Unions partIds across every selected domain, first-occurrence-wins
	// dedup, in domainDefs' own priority order (DS -> ML -> DL -> NLP ->
	// Inference) -- so e.g. picking Data Science + Classical ML puts Math &
	// Statistics for ML exactly once, at the position its first-listing
	// domain put it in.
	build(
		domainIds: string[],
		quizScore: { correct: number; total: number },
		toolsKnown: string[],
		conceptsKnown: string[]
	): RoadmapState {
		const seen = new SvelteSet<string>();
		const partIds: string[] = [];
		for (const domain of domainDefs.filter((d) => domainIds.includes(d.id))) {
			for (const partId of domain.partIds) {
				if (!seen.has(partId)) {
					seen.add(partId);
					partIds.push(partId);
				}
			}
		}

		// Placement quiz is the ONLY thing that skips content -- the
		// tools/concepts checklists above are advisory tags only, per the
		// spec's explicit "quiz overrides checklists" decision.
		const mastered = quizScore.total > 0 && quizScore.correct >= Math.ceil(quizScore.total * 0.66);

		const parts = partIds.map((partId, position) => ({
			partId,
			position,
			skipped: mastered && partId === SKIP_ELIGIBLE_PART_ID
		}));

		return {
			domainIds,
			quizScore,
			toolsKnown,
			conceptsKnown,
			parts,
			createdAt: new SvelteDate().toISOString()
		};
	},

	// Overwrites whatever roadmap was active before, if any -- re-running the
	// wizard always replaces, never merges. Question-completion state
	// (`solved`) is a completely separate store and is never touched here.
	activate(state: RoadmapState) {
		current = state;
		writeStorage(current);
	},

	// Clears which roadmap is active. Does NOT touch `solved` -- questions
	// already solved under the old roadmap stay solved.
	reset() {
		current = null;
		writeStorage(null);
	}
};

export interface RoadmapPartProgress {
	partId: string;
	title: string;
	solved: number;
	total: number;
	skipped: boolean;
}

export interface RoadmapProgress {
	rows: RoadmapPartProgress[];
	totalSolved: number;
	totalCount: number;
}

// Derived at read time from `solved.slugs`, exactly like getPartProgress
// already does for the Questions page -- no separate roadmap-completion
// tracking is stored, so this stays correct even if solved state changes
// out from under an active roadmap.
export function getRoadmapProgress(): RoadmapProgress | null {
	if (!current) return null;

	const rows = current.parts.map((entry): RoadmapPartProgress => {
		const part = curriculum.find((p) => p.id === entry.partId);
		const slugs = part ? part.tracks.flatMap((t) => t.questions.map((q) => q.slug)) : [];
		const solvedCount = slugs.filter((s) => solved.slugs.has(s)).length;
		return {
			partId: entry.partId,
			title: part?.title ?? entry.partId,
			solved: solvedCount,
			total: slugs.length,
			skipped: entry.skipped
		};
	});

	const active = rows.filter((r) => !r.skipped);
	return {
		rows,
		totalSolved: active.reduce((sum, r) => sum + r.solved, 0),
		totalCount: active.reduce((sum, r) => sum + r.total, 0)
	};
}
