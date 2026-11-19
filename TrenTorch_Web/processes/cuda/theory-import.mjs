// Converts the two authored theory files (docs/cuda/source/TRENTORCH_CUDA_THEORY*.md) into the chapter files
// the site renders:  data/cuda/theory/<NN-slug>/{meta.json, theory.md}  and  data/cuda/viz-specs/<VIZ-ID>.md.
//   node processes/cuda/theory-import.mjs
// The wording of the theory is copied as written. What the converter changes is structure only: appended
// sections are merged before "Check yourself", answer keys go behind <details>, 🎬 spec blocks become a
// placeholder <div data-viz> (the spec itself is kept in data/cuda/viz-specs), and proposed problems become
// "Coming soon" cards.
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const SRC = join('docs', 'cuda', 'source');
const OUT = join('data', 'cuda', 'theory');
const SPECS = join('data', 'cuda', 'viz-specs');
const base = readFileSync(join(SRC, 'TRENTORCH_CUDA_THEORY.md'), 'utf8');
const addendum = readFileSync(join(SRC, 'TRENTORCH_CUDA_THEORY_ADDENDUM.md'), 'utf8');

const ORDER =
	'A1 A2 A3 A4 A5 B1 B2 B3 B4 B5 C1 C2 C3 D1 D2 D3 D4 D5 D6 E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 F1 F2 F3 F4 F5 F7 F8 F9 F6 G1'.split(
		' '
	);

// ---------- helpers ----------
const slugify = (t) =>
	t
		.toLowerCase()
		.replace(/[`*_$\\]/g, '')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '');
const esc = (t) =>
	t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** Splits markdown at lines that start with `prefix` ("# " or "## "), ignoring code fences. */
function splitAt(md, prefix) {
	const out = [];
	let cur = null,
		fence = false;
	for (const line of md.split('\n')) {
		if (/^```/.test(line)) fence = !fence;
		if (!fence && line.startsWith(prefix)) {
			cur = { heading: line.slice(prefix.length).trim(), lines: [] };
			out.push(cur);
		} else if (cur) cur.lines.push(line);
		else (out.pre ??= []).push(line);
	}
	return out.map((s) => ({
		heading: s.heading,
		text: s.lines
			.join('\n')
			.replace(/\n+---\s*$/, '')
			.trim()
	}));
}
const sectionsOf = (text) => {
	const parts = splitAt('\n' + text, '## ');
	const pre = text.split('\n## ')[0].startsWith('## ') ? '' : text.split(/\n## /)[0].trim();
	return { pre, sections: parts };
};

// ---------- base chapters ----------
const chapters = new Map();
const baseBlocks = splitAt(base, '# ').filter((b) => /^CHAPTER /.test(b.heading));
for (const b of baseBlocks) {
	const m = /^CHAPTER (\w+): (.+)$/.exec(b.heading);
	chapters.set(m[1], newChapter(m[1], m[2], b.text));
}
function newChapter(id, title, text) {
	const lines = text.split('\n');
	const metaLine = lines.shift().replace(/`/g, '').trim();
	const { pre, sections } = sectionsOf(lines.join('\n').trim());
	return {
		id,
		title,
		metaLine,
		pre,
		sections,
		appended: [],
		gapfill: [],
		extraChecks: [],
		refs: [],
		furtherReading: []
	};
}

// ---------- addendum ----------
const addBlocks = splitAt(addendum, '# ');
const specs = new Map(); // viz id -> { chapterIds, text }
const answerKey = new Map();
let g1Answers = '';
let furtherLines = [];
const gapfill = [];
let extensionsText = '';
for (const b of addBlocks) {
	let m;
	if ((m = /^NEW CHAPTER (\w+): (.+)$/.exec(b.heading)))
		chapters.set(m[1], newChapter(m[1], m[2], b.text));
	else if ((m = /^APPEND TO (\w+):/.exec(b.heading))) {
		const ch = chapters.get(m[1]);
		if (!ch) throw new Error('APPEND TO unknown chapter ' + m[1]);
		const { sections } = sectionsOf(b.text);
		for (const s of sections) {
			if (/^Check yourself/.test(s.heading)) {
				ch.extraChecks.push(
					...s.text
						.split('\n')
						.filter((l) => /^\d+\.\s/.test(l))
						.map((l) => l.replace(/^\d+\.\s*/, ''))
				);
				// the block's closing "*PMPP reference:* ..." line follows its additional questions: keep it
				ch.refs.push(...s.text.split('\n').filter((l) => l.trim() && !/^\d+\.\s/.test(l)));
			} else ch.appended.push(s);
		}
	} else if (/^VISUALIZATION GAP-FILL/.test(b.heading)) {
		for (const s of sectionsOf(b.text).sections) {
			if (s.heading.startsWith('🎬')) gapfill.push(s);
			else if (/^Small extensions/.test(s.heading)) extensionsText = s.text;
		}
	} else if (/^ANSWER KEY/.test(b.heading)) {
		const [key, further] = b.text.split(/\n## Further reading/);
		furtherLines = (further ?? '').split('\n').filter((l) => l.startsWith('- '));
		const g1 = key.split(/\n## G1 workbook answers/);
		g1Answers = (g1[1] ?? '').trim();
		for (const line of g1[0].split('\n')) {
			const k = /^\*\*(\w+)\.\*\*\s*(.*)$/.exec(line.trim());
			if (k) answerKey.set(k[1], k[2]);
		}
	}
}
// further reading: "- text: A, B" attaches to those chapters
for (const line of furtherLines) {
	const m = /:\s*((?:[A-G]\d+)(?:,\s*[A-G]\d+)*)\.?\s*$/.exec(line);
	if (!m) continue;
	const bullet =
		line.slice(0, m.index).replace(/\s+$/, '') + (line.slice(0, m.index).endsWith('.') ? '' : '');
	for (const id of m[1].split(/,\s*/)) chapters.get(id)?.furtherReading.push(bullet);
}

// gap-fill specs go to the named chapters
const GAP_TARGETS = {
	'VIZ-WORK-SPAN': ['A1'],
	'VIZ-ISSUE-SLOTS': ['A3', 'B3'],
	'VIZ-DIVERGENCE-PROBABILITY': ['C1'],
	'VIZ-BANK-STRIDE-SWEEP': ['D5'],
	'VIZ-SHARED-BOUND': ['D4'],
	'VIZ-FLOAT-ACCUMULATION': ['E2'],
	'VIZ-SCAN-LOOKBACK': ['E6'],
	'VIZ-RADIX-PASS': ['E8'],
	'VIZ-IM2COL': ['E4'],
	'VIZ-FUSION-BREAKEVEN': ['F3', 'F6'],
	'VIZ-ALPHA-BETA': ['F4']
};
for (const s of gapfill) {
	const id = /VIZ-[A-Z0-9-]+/.exec(s.heading)[0];
	const targets = GAP_TARGETS[id];
	if (!targets) throw new Error('no chapter for ' + id);
	for (const t of targets) chapters.get(t).gapfill.push(s);
}

// ---------- viz blocks ----------
function vizPlaceholder(section, chapterId) {
	const h = section.heading;
	let id = /VIZ-[A-Z0-9-]+/.exec(h)?.[0];
	if (!id) {
		if (/Annotated report/.test(h)) id = 'VIZ-ANNOTATED-REPORT';
		else throw new Error('viz without id: ' + h);
	}
	const quoted = /"([^"]+)"/.exec(h)?.[1];
	const title =
		quoted ??
		id
			.replace(/^VIZ-/, '')
			.toLowerCase()
			.split('-')
			.map((w) => w[0].toUpperCase() + w.slice(1))
			.join(' ');
	const ext = /(?:extension of|extra mode of) (VIZ-[A-Z0-9-]+)/.exec(h);
	const mode = ext ? id.replace(/^VIZ-/, '').toLowerCase() : '';
	const entry = specs.get(id) ?? { chapters: [], text: `## ${h}\n${section.text}\n` };
	if (!entry.chapters.includes(chapterId)) entry.chapters.push(chapterId);
	specs.set(id, entry);
	const attrs = `data-viz="${ext ? ext[1] : id}"${mode ? ` data-mode="${mode}"` : ''} data-title="${esc(title)}" data-spec="${id}"`;
	return { heading: `Interactive: ${title}`, text: `<div class="cuda-viz" ${attrs}></div>` };
}

// ---------- problem cards ----------
function proposedCards(section) {
	// "**CU-053 SpMV (CSR)**: text"  ->  coming-soon card
	return section.text
		.split('\n')
		.map((line) => {
			const m = /^\*\*(CU-\d+) ([^*]+)\*\*:\s*(.*)$/.exec(line.trim());
			return m ? card(m[1], m[2], m[3]) : line;
		})
		.join('\n');
}
const card = (id, name, text) =>
	`<div class="coming-soon"><div class="cs-head"><strong>${esc(id)} ${esc(name.trim())}</strong><span class="cs-badge">Coming soon</span></div><p>${esc(text)}</p></div>`;
function inlineProposed(text) {
	return text
		.split('\n')
		.map((line) => {
			const m = /^\*\*Proposed:\*\*\s*(CU-\d+)\s+([^(]+?)\s*\((.*)\)\.?$/.exec(line.trim());
			return m ? card(m[1], m[2], m[3]) : line;
		})
		.join('\n');
}

// ---------- hand-drawn diagrams ----------
// Placeholders mounted by the chapter page (platform/components/cuda/diagrams). They sit before a section heading, so
// no heading is renamed and no authored sentence changes.
const DIAGRAMS = {
	A1: [['Check yourself', 'gpu-data-flow', 'Follow one launch from host to thread']],
	A2: [
		['SIMT in one paragraph', 'cpu-gpu-system', 'The host, the device and the road between them']
	],
	A4: [],
	B1: [['The global index', 'grid-of-blocks', 'A grid of blocks of threads']],
	B2: [['Residency', 'block-scheduling', 'Blocks handed to SMs']],
	B3: [['Linearized thread id \u2192 warp and lane', 'warps-in-block', 'A block cut into warps']]
};
function addDiagrams(id, md) {
	if (id === 'A3') {
		// the box-drawing tree becomes a real figure; the heading stays
		md = md.replace(
			/(## The tree\n\n)```[\s\S]*?```/,
			'$1<div class="cuda-diagram" data-diagram="chip-hierarchy" data-title="Inside a GPU"></div>'
		);
	}
	for (const [heading, name, title] of DIAGRAMS[id] ?? []) {
		const h = `## ${heading}`;
		const i = md.indexOf(`\n${h}\n`);
		if (i < 0) throw new Error(`diagram anchor missing in ${id}: ${heading}`);
		md =
			md.slice(0, i) +
			`\n<div class="cuda-diagram" data-diagram="${name}" data-title="${title}"></div>\n` +
			md.slice(i);
	}
	return md;
}

// ---------- answer keys ----------
/** "(1) a. (2) b." -> ["a.", "b."], scanning for the next expected number. */
function splitNumbered(text, pattern) {
	const items = [];
	let n = 1;
	const mk = (k) => pattern(k);
	const m = mk(1).exec(text);
	if (!m) return [text];
	let start = m.index + m[0].length;
	for (;;) {
		n++;
		const re = mk(n);
		re.lastIndex = 0;
		const rest = text.slice(start);
		const next = re.exec(rest);
		if (!next) {
			items.push(text.slice(start).trim());
			break;
		}
		items.push(rest.slice(0, next.index).trim());
		start += next.index + next[0].length;
	}
	return items;
}
const answerList = (raw) =>
	splitNumbered(raw.replace(/\*Add\.:\*/g, ' '), (k) => new RegExp(`(?:^|\\s)\\(${k}\\)\\s`))
		.map((a, i) => `${i + 1}. ${a}`)
		.join('\n');

function g1Items(text) {
	// "1. ... 2. ... 3. ..." (several per line), numbered 1..34
	return splitNumbered(text.replace(/\n/g, ' '), (k) => new RegExp(`(?:^|\\s)${k}\\.\\s(?=\\S)`));
}

// ---------- assemble chapters ----------
const parseMeta = (line) => {
	const f = Object.fromEntries(
		line.split(' · ').map((p) => {
			const i = p.indexOf(':');
			return [p.slice(0, i).trim(), p.slice(i + 1).trim()];
		})
	);
	const ids = (s) => [...(s ?? '').matchAll(/\b([A-G]\d+)\b/g)].map((m) => m[1]);
	const probs = f.problems ?? '';
	const real = [...probs.replace(/proposed[^,]*/gi, '').matchAll(/CU-\d+/g)].map((m) => m[0]);
	const proposed = [...probs.matchAll(/proposed (CU-\d+)/gi)].map((m) => m[1]);
	const est = /(\d+)/.exec(f.est ?? '')?.[1];
	const pm = f.pmpp ?? '';
	return {
		part: f.part,
		estMinutes: est ? Number(est) : 0,
		prereqs: f.prereqs === 'none' ? [] : ids(f.prereqs),
		prereqNote:
			f.prereqs !== 'none' &&
			/[a-z]{4,}/.test(f.prereqs.replace(/\b(and|any|chapter|you|are|practising)\b/g, ''))
				? ''
				: /any chapter/.test(f.prereqs ?? '')
					? f.prereqs
					: '',
		problems: real,
		proposedProblems: proposed,
		problemsNote: /none|calculation|quiz/.test(probs) ? probs : '',
		pmpp: [...pm.matchAll(/Ch\.\s*([\d, \-()a-z]+?)(?:$|;)/g)].length
			? pm
					.replace(/^Ch\.\s*/, '')
					.split(/,\s*/)
					.map((x) => `Ch. ${x.trim()}`)
			: []
	};
};

rmSync(OUT, { recursive: true, force: true });
rmSync(SPECS, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });
mkdirSync(SPECS, { recursive: true });

const report = { chapters: 0, appended: 0, viz: 0 };
const g1ItemsList = g1Items(g1Answers);
let order = 0;
for (const id of ORDER) {
	const ch = chapters.get(id);
	if (!ch) throw new Error('missing chapter ' + id);
	order++;
	const meta = parseMeta(ch.metaLine);

	// merge sections: base up to Check yourself, then appended, then gap-fill, then the rest
	const ci = ch.sections.findIndex((s) => /^Check yourself/.test(s.heading));
	const head = ci < 0 ? ch.sections : ch.sections.slice(0, ci);
	const check = ci < 0 ? null : ch.sections[ci];
	const tail = ci < 0 ? [] : ch.sections.slice(ci + 1);
	const pieces = [...head, ...ch.appended, ...ch.gapfill];
	report.appended += ch.appended.length;
	const out = [];
	for (const s of pieces) {
		let sec = s;
		if (s.heading.startsWith('🎬')) {
			sec = vizPlaceholder(s, id);
			report.viz++;
		}
		out.push(`## ${sec.heading}\n\n${sec.text}`);
	}
	// check yourself (merged list) + answers
	if (check) {
		const items = [
			...check.text
				.split('\n')
				.filter((l) => /^\d+\.\s/.test(l))
				.map((l) => l.replace(/^\d+\.\s*/, '')),
			...ch.extraChecks
		];
		const lead = check.text
			.split('\n')
			.filter((l) => !/^\d+\.\s/.test(l))
			.join('\n')
			.trim();
		let body = (lead ? lead + '\n\n' : '') + items.map((t, i) => `${i + 1}. ${t}`).join('\n');
		if (answerKey.has(id))
			body += `\n\n<details class="answers">\n<summary>Show answers</summary>\n\n${answerList(answerKey.get(id))}\n\n</details>`;
		out.push(`## Check yourself\n\n${body}`);
	}
	for (const s of tail) {
		if (s.heading === 'Proposed problem') out.push(`## Proposed problem\n\n${proposedCards(s)}`);
		else if (s.heading.startsWith('🎬')) {
			const p = vizPlaceholder(s, id);
			report.viz++;
			out.push(`## ${p.heading}\n\n${p.text}`);
		} else out.push(`## ${s.heading}\n\n${inlineProposed(s.text)}`);
	}
	if (id === 'G1') {
		// the workbook: every numbered problem is a card with its own answer toggle
		out.length = 0;
		let n = 0;
		for (const s of ch.sections) {
			const items = s.text
				.split('\n')
				.filter((l) => /^\d+\.\s/.test(l))
				.map((l) => l.replace(/^\d+\.\s*/, ''));
			const cards = items.map((q) => {
				n++;
				return `<div class="g1-card" data-problem="${n}">\n\n**Problem ${n}.** ${q}\n\n<div class="g1-check" data-problem="${n}"></div>\n\n<details class="answers">\n<summary>Show worked answer</summary>\n\n${g1ItemsList[n - 1] ?? ''}\n\n</details>\n\n</div>`;
			});
			out.push(`## ${s.heading}\n\n${cards.join('\n\n')}`);
		}
		if (n !== 34) throw new Error('G1 expected 34 problems, found ' + n);
		if (g1ItemsList.length !== 34)
			throw new Error('G1 expected 34 answers, found ' + g1ItemsList.length);
	}
	if (ch.refs.length) out.push(ch.refs.join('\n\n'));
	if (ch.furtherReading.length) out.push(`## Further reading\n\n${ch.furtherReading.join('\n')}`);

	let preText = ch.pre;
	if (id === 'G1') {
		// the agent-facing paragraph (how to build the cards) is not for learners; keep the profiles line
		const at = preText.indexOf('Profiles:');
		preText =
			'Work each problem with a pen first, then press **Check** to compare your number with the model. Answers are behind a toggle.\n\n' +
			(at >= 0 ? preText.slice(at) : '');
	}
	const pre = preText ? preText + '\n\n' : '';
	let md = `# ${ch.title}\n\n${pre}${out.join('\n\n')}\n`;
	md = addDiagrams(id, md);
	const dir = join(OUT, `${String(order).padStart(2, '0')}-${slugify(ch.title)}`);
	mkdirSync(dir, { recursive: true });
	writeFileSync(join(dir, 'theory.md'), md);
	writeFileSync(
		join(dir, 'meta.json'),
		JSON.stringify({ id, title: ch.title, ...meta }, null, '\t') + '\n'
	);
	report.chapters++;
}
writeFileSync(
	join(SPECS, '_extensions.md'),
	'## Small extensions to existing viz\n\n' + extensionsText + '\n'
);
for (const [id, s] of specs)
	writeFileSync(join(SPECS, `${id}.md`), `<!-- chapters: ${s.chapters.join(', ')} -->\n${s.text}`);
console.log(JSON.stringify({ ...report, specs: specs.size }));
