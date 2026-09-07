import { r as onDestroy } from "../../../../chunks/index-server.js";
import { D as attr, M as writable, O as clsx, a as derived, c as head, d as spread_props, f as store_get, g as html, i as bind_props, k as escape_html, m as unsubscribe_stores, n as attr_style, p as stringify, s as ensure_array_like, t as attr_class } from "../../../../chunks/server.js";
import "../../../../chunks/exports.js";
import { t as resolve } from "../../../../chunks/paths.js";
import "../../../../chunks/state.js";
import { t as Icon } from "../../../../chunks/Icon.js";
import { t as Arrow_left } from "../../../../chunks/arrow-left.js";
import { t as Book_open } from "../../../../chunks/book-open.js";
import { n as Chevron_left, t as Chevron_right } from "../../../../chunks/chevron-right.js";
import { i as session, n as potdEntries, r as Badge, t as solved } from "../../../../chunks/solved.svelte.js";
import { t as signInPrompt } from "../../../../chunks/sign-in-prompt.svelte.js";
import { t as attempted } from "../../../../chunks/attempted.svelte.js";
import { n as questionsById } from "../../../../chunks/curriculum-index.js";
import { n as localDateString } from "../../../../chunks/get-todays-potd.js";
import { marked } from "marked";
import markedKatex from "marked-katex-extension";
//#region node_modules/@lucide/svelte/dist/icons/circle-alert.svelte
function Circle_alert($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "circle-alert",
		"size": 24,
		"node": [
			["circle", {
				"cx": "12",
				"cy": "12",
				"r": "10"
			}],
			["line", {
				"x1": "12",
				"x2": "12",
				"y1": "8",
				"y2": "12"
			}],
			["line", {
				"x1": "12",
				"x2": "12.01",
				"y1": "16",
				"y2": "16"
			}]
		],
		"aliases": ["alert-circle"]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/circle-check.svelte
function Circle_check($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "circle-check",
		"size": 24,
		"node": [["circle", {
			"cx": "12",
			"cy": "12",
			"r": "10"
		}], ["path", { "d": "m16 9-5.5 5.5L8 12" }]],
		"aliases": ["check-circle-2"]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/circle-x.svelte
function Circle_x($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "circle-x",
		"size": 24,
		"node": [
			["circle", {
				"cx": "12",
				"cy": "12",
				"r": "10"
			}],
			["path", { "d": "m15 9-6 6" }],
			["path", { "d": "m9 9 6 6" }]
		],
		"aliases": ["x-circle"]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/cloud-upload.svelte
function Cloud_upload($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "cloud-upload",
		"size": 24,
		"node": [
			["path", { "d": "M12 13v8" }],
			["path", { "d": "M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" }],
			["path", { "d": "m8 17 4-4 4 4" }]
		],
		"aliases": ["upload-cloud"]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/code-xml.svelte
function Code_xml($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "code-xml",
		"size": 24,
		"node": [
			["path", { "d": "m18 16 4-4-4-4" }],
			["path", { "d": "m6 8-4 4 4 4" }],
			["path", { "d": "m14.5 4-5 16" }]
		],
		"aliases": ["code-2"]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/copy.svelte
function Copy($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "copy",
		"size": 24,
		"node": [["rect", {
			"width": "14",
			"height": "14",
			"x": "8",
			"y": "8",
			"rx": "2",
			"ry": "2"
		}], ["path", { "d": "M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/list-checks.svelte
function List_checks($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "list-checks",
		"size": 24,
		"node": [
			["path", { "d": "M13 5h8" }],
			["path", { "d": "M13 12h8" }],
			["path", { "d": "M13 19h8" }],
			["path", { "d": "m3 17 2 2 4-4" }],
			["path", { "d": "m3 7 2 2 4-4" }]
		]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/loader-circle.svelte
function Loader_circle($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "loader-circle",
		"size": 24,
		"node": [["path", { "d": "M21 12a9 9 0 1 1-6.219-8.56" }]],
		"aliases": ["loader-2"]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/maximize.svelte
function Maximize($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "maximize",
		"size": 24,
		"node": [
			["path", { "d": "M8 3H5a2 2 0 0 0-2 2v3" }],
			["path", { "d": "M21 8V5a2 2 0 0 0-2-2h-3" }],
			["path", { "d": "M3 16v3a2 2 0 0 0 2 2h3" }],
			["path", { "d": "M16 21h3a2 2 0 0 0 2-2v-3" }]
		]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/minimize.svelte
function Minimize($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "minimize",
		"size": 24,
		"node": [
			["path", { "d": "M8 3v3a2 2 0 0 1-2 2H3" }],
			["path", { "d": "M21 8h-3a2 2 0 0 1-2-2V3" }],
			["path", { "d": "M3 16h3a2 2 0 0 1 2 2v3" }],
			["path", { "d": "M16 21v-3a2 2 0 0 1 2-2h3" }]
		]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/play.svelte
function Play($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "play",
		"size": 24,
		"node": [["path", { "d": "M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/refresh-ccw.svelte
function Refresh_ccw($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "refresh-ccw",
		"size": 24,
		"node": [
			["path", { "d": "M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" }],
			["path", { "d": "M3 3v5h5" }],
			["path", { "d": "M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" }],
			["path", { "d": "M16 16h5v5" }]
		]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/rotate-ccw.svelte
function Rotate_ccw($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "rotate-ccw",
		"size": 24,
		"node": [["path", { "d": "M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" }], ["path", { "d": "M3 3v5h5" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/shield-check.svelte
function Shield_check($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "shield-check",
		"size": 24,
		"node": [["path", { "d": "M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" }], ["path", { "d": "m9 12 2 2 4-4" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/terminal.svelte
function Terminal($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "terminal",
		"size": 24,
		"node": [["path", { "d": "M12 19h8" }], ["path", { "d": "m4 17 6-6-6-6" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/trash.svelte
function Trash($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "trash",
		"size": 24,
		"node": [
			["path", { "d": "M10 11v6" }],
			["path", { "d": "M14 11v6" }],
			["path", { "d": "M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" }],
			["path", { "d": "M3 6h18" }],
			["path", { "d": "M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" }]
		],
		"aliases": ["trash-2"]
	} }]));
}
//#endregion
//#region processes/ide-content/get-adjacent-question-ids.ts
function getAdjacentQuestionIds(id) {
	const ids = [...questionsById.keys()];
	const index = ids.indexOf(id);
	if (index === -1) return {
		prevId: null,
		nextId: null
	};
	return {
		prevId: index > 0 ? ids[index - 1] : null,
		nextId: index < ids.length - 1 ? ids[index + 1] : null
	};
}
//#endregion
//#region processes/code-execution/sanitize-student-code.ts
function parenDelta(line) {
	let delta = 0;
	for (const ch of line) if (ch === "(") delta++;
	else if (ch === ")") delta--;
	return delta;
}
function isBoilerplateStart(line) {
	return /^\s*sys\.path\.insert\s*\(/.test(line) || /^\s*from\s+_load\s+import\b/.test(line) || /^\s*\S+\s*=\s*load_solution\s*\(/.test(line);
}
function sanitizeStudentCode(code) {
	const kept = [];
	let openParens = 0;
	for (const line of code.split("\n")) {
		if (openParens > 0) {
			openParens += parenDelta(line);
			continue;
		}
		if (isBoilerplateStart(line)) {
			openParens = Math.max(0, parenDelta(line));
			continue;
		}
		kept.push(line);
	}
	return kept.join("\n");
}
//#endregion
//#region processes/code-execution/pyodide-service.ts
var PyodideService = class {
	worker = null;
	requestId = 0;
	pendingRequests = /* @__PURE__ */ new Map();
	runtimeState = writable("uninitialized");
	consoleOutput = writable("");
	testResults = writable(null);
	isRunning = writable(false);
	init() {
		if (typeof window === "undefined" || this.worker) return;
		try {
			this.runtimeState.set("loading_runtime");
			this.worker = new Worker(new URL("./pyodide-worker.ts", import.meta.url), { type: "module" });
			this.worker.onmessage = (e) => {
				const { id, type, status, output, error, success, durationMs, ...rest } = e.data;
				if (type === "status") {
					this.runtimeState.set(status);
					return;
				}
				if (type === "run_result") {
					this.isRunning.set(false);
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const formattedOut = (output || "") + (error ? `\n\nTraceback:\n${error}` : "");
						this.consoleOutput.set(formattedOut);
						req.resolve({
							success: Boolean(success),
							output: formattedOut,
							error,
							durationMs
						});
					}
					return;
				}
				if (type === "test_result") {
					this.isRunning.set(false);
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						const subResult = {
							contentId: rest.contentId,
							totalTests: rest.totalTests,
							passedTests: rest.passedTests,
							failedTests: rest.failedTests,
							allPassed: rest.allPassed,
							totalDurationMs: rest.totalDurationMs,
							results: rest.results || [],
							rawOutput: rest.rawOutput || "",
							error: error || void 0,
							isSample: Boolean(rest.isSample)
						};
						this.testResults.set(subResult);
						if (error) this.consoleOutput.set(`Run failed before the tests could execute:\n\n${error}`);
						else if (subResult.rawOutput.trim()) this.consoleOutput.set(subResult.rawOutput);
						else this.consoleOutput.set(`${subResult.passedTests}/${subResult.totalTests} checks passed.`);
						req.resolve(subResult);
					}
					return;
				}
				if (type === "error") {
					this.isRunning.set(false);
					const req = this.pendingRequests.get(id);
					if (req) {
						this.pendingRequests.delete(id);
						req.reject(new Error(error));
					}
					this.consoleOutput.update((prev) => prev + `\n[Error]: ${error}`);
				}
			};
			this.worker.onerror = (err) => {
				console.error("Worker error", err);
				this.runtimeState.set("error");
				this.isRunning.set(false);
			};
			const id = ++this.requestId;
			this.worker.postMessage({
				id,
				action: "init"
			});
		} catch (err) {
			console.error("Failed to instantiate Pyodide worker", err);
			this.runtimeState.set("error");
		}
	}
	async runCode(code) {
		this.init();
		this.isRunning.set(true);
		this.consoleOutput.set("Executing Python code in Web Worker...\n");
		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.has(id)) {
					this.pendingRequests.delete(id);
					this.isRunning.set(false);
					this.consoleOutput.set("[Timeout]: Execution exceeded 20 seconds. Terminating execution.");
					reject(/* @__PURE__ */ new Error("Execution timed out"));
				}
			}, 2e4);
			this.pendingRequests.set(id, {
				resolve: (res) => {
					clearTimeout(timeout);
					resolve(res);
				},
				reject: (err) => {
					clearTimeout(timeout);
					reject(err);
				}
			});
			this.worker?.postMessage({
				id,
				action: "run",
				code: sanitizeStudentCode(code)
			});
		});
	}
	async runTests(code, testHarnessCode, contentId, sampleLimit) {
		this.init();
		this.isRunning.set(true);
		this.consoleOutput.set(sampleLimit ? `Running the first ${sampleLimit} checks for [${contentId}]...\n` : `Running test suite for [${contentId}]...\n`);
		return new Promise((resolve, reject) => {
			const id = ++this.requestId;
			const timeout = setTimeout(() => {
				if (this.pendingRequests.has(id)) {
					this.pendingRequests.delete(id);
					this.isRunning.set(false);
					this.consoleOutput.set("[Timeout]: Test suite exceeded 25 seconds.");
					reject(/* @__PURE__ */ new Error("Test execution timed out"));
				}
			}, 25e3);
			this.pendingRequests.set(id, {
				resolve: (res) => {
					clearTimeout(timeout);
					resolve(res);
				},
				reject: (err) => {
					clearTimeout(timeout);
					reject(err);
				}
			});
			this.worker?.postMessage({
				id,
				action: "test",
				code: sanitizeStudentCode(code),
				testHarnessCode,
				contentId,
				sampleLimit
			});
		});
	}
};
var pyodideService = new PyodideService();
//#endregion
//#region processes/code-execution/code-storage-key.ts
var CODE_KEY_PREFIX = "trentorch_code_";
//#endregion
//#region processes/code-execution/save-user-code.ts
function saveUserCode(contentId, code) {
	if (typeof window === "undefined") return;
	try {
		localStorage.setItem(`${CODE_KEY_PREFIX}${contentId}`, code);
	} catch (e) {
		console.error("Failed to save code to localStorage", e);
	}
}
//#endregion
//#region processes/code-execution/reset-user-code.ts
function resetUserCode(contentId) {
	if (typeof window === "undefined") return;
	try {
		localStorage.removeItem(`${CODE_KEY_PREFIX}${contentId}`);
	} catch (e) {
		console.error("Failed to reset code in localStorage", e);
	}
}
//#endregion
//#region platform/components/ide/IdeHeader.svelte
function IdeHeader($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { content, fromPage = null, runtimeState = "ready", isRunning = false, isFullscreen = false, onResetCode = () => {}, onReattempt = () => {}, onRunCode = () => {}, onRunTests = () => {}, onToggleFullscreen = () => {} } = $$props;
		let isBusy = derived(() => isRunning || runtimeState === "loading_runtime" || runtimeState === "loading_packages");
		let backHref = derived(() => fromPage ? resolve(`/questions?page=${fromPage}`) : resolve("/questions"));
		$$renderer.push(`<header class="grid h-12 w-full grid-cols-[1fr_auto_1fr] items-center border-b border-border bg-background px-2 font-mono text-xs text-foreground"><div class="flex items-center gap-1 justify-self-start"><a${attr("href", backHref())} class="flex items-center gap-1.5 rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground" title="Back to Questions">`);
		Arrow_left($$renderer, { class: "size-4" });
		$$renderer.push(`<!----></a> <div class="h-4 w-px bg-border"></div> <a${attr("href", backHref())} class="flex items-center gap-1.5 rounded px-2 py-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground">`);
		List_checks($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----> <span class="hidden truncate sm:inline">${escape_html(content.metadata.title)}</span></a></div> <div class="flex items-center gap-2 justify-self-center"><button type="button" class="flex items-center gap-1.5 rounded-full border border-border bg-secondary px-3.5 py-1.5 font-medium text-foreground transition-colors hover:border-foreground/30 hover:bg-muted disabled:pointer-events-none disabled:opacity-40"${attr("disabled", isBusy(), true)} title="Run code (Shift+Enter)">`);
		if (isBusy()) {
			$$renderer.push("<!--[0-->");
			Loader_circle($$renderer, { class: "size-3.5 animate-spin" });
		} else {
			$$renderer.push("<!--[-1-->");
			Play($$renderer, { class: "size-3 fill-current" });
		}
		$$renderer.push(`<!--]--> <span>Run</span></button> <button type="button" class="flex items-center gap-1.5 rounded-full bg-emerald-600 px-3.5 py-1.5 font-medium text-white shadow-sm transition-colors hover:bg-emerald-500 disabled:pointer-events-none disabled:opacity-40 dark:bg-emerald-500 dark:hover:bg-emerald-400"${attr("disabled", isBusy(), true)} title="Run the test suite and submit">`);
		Cloud_upload($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----> <span>Submit</span></button></div> <div class="flex items-center gap-1 justify-self-end"><button type="button" class="flex items-center rounded border border-red-500/30 p-1.5 text-red-600 transition-colors hover:bg-red-500/10 dark:text-red-400" title="Re-attempt this question: reset to the starter code and mark it unsolved again" aria-label="Re-attempt this question">`);
		Refresh_ccw($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----></button> <button type="button" class="rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground" title="Reset code to the original starter template">`);
		Rotate_ccw($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----></button> <button type="button" class="rounded p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"${attr("title", isFullscreen ? "Exit fullscreen" : "Enter fullscreen")}>`);
		if (isFullscreen) {
			$$renderer.push("<!--[0-->");
			Minimize($$renderer, { class: "size-3.5" });
		} else {
			$$renderer.push("<!--[-1-->");
			Maximize($$renderer, { class: "size-3.5" });
		}
		$$renderer.push(`<!--]--></button></div></header>`);
	});
}
//#endregion
//#region platform/components/ide/GuidePane.svelte
function GuidePane($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		marked.use(markedKatex({ throwOnError: false }));
		let { content, isCompleted = false, prevId = null, nextId = null, visibleTabs = [
			"description",
			"theory",
			"solution"
		] } = $$props;
		/** Which guide tabs to offer for this question -- the ide/[id] page
		* narrows this for Problem of the Day questions (today's: just
		* Description; a past one: Description + Theory, still no Solution).
		* Every other question gets the full default set. */
		let fromPage = derived(() => null);
		let prevHref = derived(() => prevId ? fromPage() ? resolve(`/ide/[id]?from=${fromPage()}`, { id: prevId }) : resolve("/ide/[id]", { id: prevId }) : null);
		let nextHref = derived(() => nextId ? fromPage() ? resolve(`/ide/[id]?from=${fromPage()}`, { id: nextId }) : resolve("/ide/[id]", { id: nextId }) : null);
		let descriptionHtml = derived(() => marked.parse(content.descriptionMarkdown, { async: false }));
		derived(() => marked.parse(content.theoryMarkdown, { async: false }));
		derived(() => marked.parse("```python\n" + content.solutionCode + "\n```", { async: false }));
		derived(() => content.explanationMarkdown ? marked.parse(content.explanationMarkdown, { async: false }) : "");
		const difficultyClass = {
			Beginner: "text-green-600 dark:text-green-400 border-green-600/30",
			Intermediate: "text-yellow-600 dark:text-yellow-400 border-yellow-600/30",
			Advanced: "text-orange-600 dark:text-orange-400 border-orange-600/30",
			Mastery: "text-red-600 dark:text-red-400 border-red-600/30"
		};
		$$renderer.push(`<div class="flex h-full flex-col bg-background text-foreground/90"><div class="flex h-8 shrink-0 items-center justify-between border-b border-border px-2"><a${attr("href", prevHref() ?? void 0)} title="Previous question"${attr("aria-disabled", !prevHref())}${attr("tabindex", prevHref() ? 0 : -1)}${attr_class(`flex items-center rounded p-1 text-muted-foreground transition-colors ${prevHref() ? "hover:bg-secondary hover:text-foreground" : "pointer-events-none opacity-30"}`)}>`);
		Chevron_left($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----></a> <a${attr("href", nextHref() ?? void 0)} title="Next question"${attr("aria-disabled", !nextHref())}${attr("tabindex", nextHref() ? 0 : -1)}${attr_class(`flex items-center rounded p-1 text-muted-foreground transition-colors ${nextHref() ? "hover:bg-secondary hover:text-foreground" : "pointer-events-none opacity-30"}`)}>`);
		Chevron_right($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----></a></div> <div class="flex h-9 shrink-0 items-center gap-1 border-b border-border px-2 font-mono text-xs">`);
		if (visibleTabs.includes("description")) $$renderer.push(`<!--[0--><button type="button"${attr_class(`px-3 py-1.5 font-medium transition-colors border-b-2 border-foreground text-foreground`)}>Description</button>`);
		else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		if (visibleTabs.includes("theory")) $$renderer.push(`<!--[0--><button type="button"${attr_class(`px-3 py-1.5 font-medium transition-colors text-muted-foreground hover:text-foreground`)}>Theory</button>`);
		else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--> `);
		if (visibleTabs.includes("solution")) $$renderer.push(`<!--[0--><button type="button"${attr_class(`px-3 py-1.5 font-medium transition-colors text-muted-foreground hover:text-foreground`)}>Solution</button>`);
		else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></div> <div class="flex-1 overflow-y-auto p-5 text-sm"><div class="mb-5 border-b border-border pb-4"><div class="mb-2 flex flex-wrap items-center gap-2"><h1 class="font-mono text-lg font-semibold tracking-tight text-foreground">${escape_html(content.metadata.title)}</h1> `);
		if (isCompleted) {
			$$renderer.push("<!--[0-->");
			Badge($$renderer, {
				variant: "outline",
				class: "border-green-600/30 font-mono text-green-600 dark:text-green-400",
				children: ($$renderer) => {
					Circle_check($$renderer, { class: "size-3" });
					$$renderer.push(`<!----> Solved`);
				},
				$$slots: { default: true }
			});
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></div> <div class="flex flex-wrap items-center gap-1.5 text-xs">`);
		Badge($$renderer, {
			variant: "outline",
			class: `font-mono ${stringify(difficultyClass[content.metadata.difficulty])}`,
			children: ($$renderer) => {
				$$renderer.push(`<!---->${escape_html(content.metadata.difficulty)}`);
			},
			$$slots: { default: true }
		});
		$$renderer.push(`<!----> <!--[-->`);
		const each_array = ensure_array_like(content.metadata.tags);
		for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
			let tag = each_array[$$index];
			$$renderer.push(`<span class="inline-flex items-center rounded-md border border-border bg-muted/50 px-1.5 py-0.5 font-mono text-[11px] leading-none text-muted-foreground">${escape_html(tag)}</span>`);
		}
		$$renderer.push(`<!--]--></div></div> `);
		$$renderer.push(`<!--[0--><div class="question-prose">${html(descriptionHtml())}</div>`);
		$$renderer.push(`<!--]--></div></div>`);
	});
}
//#endregion
//#region platform/components/ide/CodeEditor.svelte
function CodeEditor($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { value = "", onRun = () => {}, onChange = () => {}, onCursorChange = () => {} } = $$props;
		const sharedRoot = {
			height: "100%",
			fontFamily: "'Geist Mono', 'JetBrains Mono', ui-monospace, Menlo, monospace",
			fontSize: "13px"
		};
		({ ...sharedRoot });
		({ ...sharedRoot });
		onDestroy(() => void 0);
		$$renderer.push(`<div class="relative h-full w-full overflow-hidden bg-background"></div>`);
		bind_props($$props, { value });
	});
}
//#endregion
//#region platform/components/ide/OutputConsole.svelte
function OutputConsole($$renderer, $$props) {
	let { output = "", onClear = () => {} } = $$props;
	$$renderer.push(`<div class="flex h-full flex-col bg-background font-mono text-xs text-foreground"><div class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3"><div class="flex items-center gap-1.5 text-[11px] tracking-wider text-muted-foreground uppercase">`);
	Terminal($$renderer, { class: "size-3" });
	$$renderer.push(`<!----> <span>Console Output</span></div> <div class="flex items-center gap-1"><button type="button" class="flex size-6 items-center justify-center text-muted-foreground transition-colors hover:text-foreground" title="Copy Output">`);
	$$renderer.push("<!--[-1-->");
	Copy($$renderer, { class: "size-3" });
	$$renderer.push(`<!--]--></button> <button type="button" class="flex size-6 items-center justify-center text-muted-foreground transition-colors hover:text-foreground" title="Clear Console">`);
	Trash($$renderer, { class: "size-3" });
	$$renderer.push(`<!----></button></div></div> <div class="flex-1 overflow-auto p-3 text-xs leading-relaxed">`);
	if (output) $$renderer.push(`<!--[0--><pre class="font-mono whitespace-pre-wrap text-foreground/80 select-text">${escape_html(output)}</pre>`);
	else $$renderer.push(`<!--[-1--><div class="flex h-full items-center justify-center text-muted-foreground italic">Click "Run Code" or press Shift+Enter to execute</div>`);
	$$renderer.push(`<!--]--></div></div>`);
}
//#endregion
//#region platform/components/ide/TestResultsView.svelte
function TestResultsView($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { results = null } = $$props;
		$$renderer.push(`<div class="flex h-full flex-col bg-background font-mono text-xs text-foreground"><div class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3"><div class="flex items-center gap-1.5 text-[11px] tracking-wider text-muted-foreground uppercase">`);
		Shield_check($$renderer, { class: "size-3" });
		$$renderer.push(`<!----> <span>${escape_html(results?.isSample ? "Sample Run" : "Test Verification Suite")}</span></div> `);
		if (results) $$renderer.push(`<!--[0--><div class="text-[11px]"><span${attr_class(clsx(results.allPassed ? "font-bold text-foreground" : "text-muted-foreground"))}>${escape_html(results.passedTests)}/${escape_html(results.totalTests)} Passed</span> <span class="ml-1 text-muted-foreground/60">(${escape_html(results.totalDurationMs)}ms)</span></div>`);
		else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></div> <div class="flex-1 overflow-auto p-4">`);
		if (results) {
			$$renderer.push("<!--[0-->");
			if (results.allPassed && results.isSample) {
				$$renderer.push(`<!--[0--><div class="mb-4 border border-border bg-secondary p-4"><div class="flex items-center gap-3">`);
				Circle_check($$renderer, { class: "size-6 text-green-600 dark:text-green-400" });
				$$renderer.push(`<!----> <div><h3 class="text-sm font-bold text-foreground">Sample checks passed</h3> <p class="text-xs text-muted-foreground">This only ran the first ${escape_html(results.totalTests)} check${escape_html(results.totalTests === 1 ? "" : "s")}. Hit Submit to run the full hidden suite and mark the question solved.</p></div></div></div>`);
			} else if (results.allPassed) {
				$$renderer.push(`<!--[1--><div class="mb-4 border border-border bg-secondary p-4"><div class="flex items-center gap-3">`);
				Circle_check($$renderer, { class: "size-6 text-green-600 dark:text-green-400" });
				$$renderer.push(`<!----> <div><h3 class="text-sm font-bold text-foreground">All Tests Passed! ⚡</h3> <p class="text-xs text-muted-foreground">Your implementation conforms to the core TrenTorch specification.</p></div></div></div>`);
			} else if (results.error && results.totalTests === 0) {
				$$renderer.push(`<!--[2--><div class="mb-4 flex items-center gap-2 border border-border bg-secondary p-3 text-foreground/80">`);
				Circle_x($$renderer, { class: "size-4 shrink-0 text-muted-foreground" });
				$$renderer.push(`<!----> <span class="text-xs">Your code crashed before any check could run. See the exception below.</span></div>`);
			} else {
				$$renderer.push(`<!--[-1--><div class="mb-4 flex items-center gap-2 border border-border bg-secondary p-3 text-foreground/80">`);
				Circle_alert($$renderer, { class: "size-4 shrink-0 text-muted-foreground" });
				$$renderer.push(`<!----> <span class="text-xs">${escape_html(results.failedTests)} test${escape_html(results.failedTests === 1 ? "" : "s")} failing. Check assertions
						below.</span></div>`);
			}
			$$renderer.push(`<!--]--> `);
			if (results.error) {
				$$renderer.push(`<!--[0--><div class="mb-4 border border-border bg-secondary p-3 text-foreground/80"><div class="mb-1 flex items-center gap-1.5 text-xs font-bold text-foreground">`);
				Circle_x($$renderer, { class: "size-3.5 text-muted-foreground" });
				$$renderer.push(`<!----> <span>Execution Exception</span></div> <pre class="font-mono text-[11px] whitespace-pre-wrap text-muted-foreground">${escape_html(results.error)}</pre></div>`);
			} else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--> <div class="space-y-2"><!--[-->`);
			const each_array = ensure_array_like(results.results);
			for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
				let test = each_array[$$index];
				$$renderer.push(`<div${attr_class(`border p-3 transition-colors ${test.passed ? "border-border bg-secondary/40" : "border-border bg-secondary"}`)}><div class="flex items-center justify-between"><div class="flex items-center gap-2">`);
				if (test.passed) {
					$$renderer.push("<!--[0-->");
					Circle_check($$renderer, { class: "size-3.5 text-green-600 dark:text-green-400" });
					$$renderer.push(`<!----> <span class="font-bold text-foreground/80">${escape_html(test.name)}</span>`);
				} else {
					$$renderer.push("<!--[-1-->");
					Circle_x($$renderer, { class: "size-3.5 text-muted-foreground" });
					$$renderer.push(`<!----> <span class="font-bold text-foreground">${escape_html(test.name)}</span>`);
				}
				$$renderer.push(`<!--]--></div> <span class="font-mono text-[11px] text-muted-foreground">${escape_html(test.durationMs)}ms</span></div> `);
				if (!test.passed && test.error) $$renderer.push(`<!--[0--><div class="mt-2 border-t border-border pt-2 font-mono text-[11px] text-muted-foreground"><p class="whitespace-pre-wrap">${escape_html(test.error)}</p></div>`);
				else $$renderer.push("<!--[-1-->");
				$$renderer.push(`<!--]--></div>`);
			}
			$$renderer.push(`<!--]--></div>`);
		} else {
			$$renderer.push(`<!--[-1--><div class="flex h-full flex-col items-center justify-center text-center text-muted-foreground">`);
			Shield_check($$renderer, { class: "mb-2 size-8 stroke-[1.5]" });
			$$renderer.push(`<!----> <p class="italic">Click "Run Tests" to test your implementation</p></div>`);
		}
		$$renderer.push(`<!--]--></div></div>`);
	});
}
//#endregion
//#region platform/components/ide/PaneResizer.svelte
function PaneResizer($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { axis, onResize, step = 24, valueNow, valueMin, valueMax, class: className = "" } = $$props;
		$$renderer.push(`<div role="separator"${attr("aria-orientation", axis === "x" ? "vertical" : "horizontal")}${attr("aria-valuenow", Math.round(valueNow))}${attr("aria-valuemin", valueMin)}${attr("aria-valuemax", valueMax)} aria-label="Resize panes" tabindex="0"${attr_class(`shrink-0 touch-none bg-border transition-colors select-none hover:bg-foreground/30 focus-visible:bg-foreground/40 focus-visible:outline-none ${axis === "x" ? "w-1 cursor-col-resize" : "h-1 cursor-row-resize"}  ${stringify(className)}`)}></div>`);
	});
}
//#endregion
//#region platform/routes/ide/[id]/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		var $$store_subs;
		const DEFAULT_LAYOUT = {
			leftPanePercent: 38,
			bottomPanePercent: 42
		};
		let { data } = $$props;
		let content = derived(() => data.content);
		let userCode = "";
		let fromPage = derived(() => null);
		let backHref = derived(() => fromPage() ? resolve(`/questions?page=${fromPage()}`) : resolve("/questions"));
		let adjacentQuestions = derived(() => content() ? getAdjacentQuestionIds(content().id) : {
			prevId: null,
			nextId: null
		});
		let guideTabs = derived(() => {
			if (!content() || true) return [
				"description",
				"theory",
				"solution"
			];
			const entry = potdEntries.find((e) => e.questionId === content().id);
			if (!entry) return [
				"description",
				"theory",
				"solution"
			];
			const today = localDateString(/* @__PURE__ */ new Date());
			return entry.date < today ? ["description", "theory"] : ["description"];
		});
		const SAMPLE_TEST_COUNT = 2;
		let activeRightTab = "tests";
		let mobileActiveTab = "editor";
		const runtimeState = pyodideService.runtimeState;
		const consoleOutput = pyodideService.consoleOutput;
		const testResults = pyodideService.testResults;
		const isRunning = pyodideService.isRunning;
		let isFullscreen = false;
		let cursorPos = {
			line: 1,
			col: 1
		};
		let lastSavedAt = null;
		let leftPanePercent = DEFAULT_LAYOUT.leftPanePercent;
		let bottomPanePercent = DEFAULT_LAYOUT.bottomPanePercent;
		function handleLeftResize(deltaPx) {}
		function handleBottomResize(deltaPx) {}
		function handleCodeChange(newCode) {
			if (!content()) return;
			userCode = newCode;
			saveUserCode(content().id, newCode);
			lastSavedAt = Date.now();
		}
		function handleResetCode() {
			if (!content()) return;
			if (confirm("Reset code to the original starter template for this question?")) {
				resetUserCode(content().id);
				userCode = content().starterCode;
				lastSavedAt = Date.now();
				pyodideService.testResults.set(null);
				pyodideService.consoleOutput.set("");
			}
		}
		function handleReattemptQuestion() {
			if (!content()) return;
			if (confirm("Re-attempt this question? This restores the starter code and marks the question unsolved again.")) {
				resetUserCode(content().id);
				userCode = content().starterCode;
				lastSavedAt = Date.now();
				solved.unmarkSolved(content().id);
				attempted.unmarkAttempted(content().id);
				pyodideService.testResults.set(null);
				pyodideService.consoleOutput.set("");
			}
		}
		async function handleRunCode() {
			if (!session.user) {
				signInPrompt.open();
				return;
			}
			mobileActiveTab = "output";
			if (!content()) {
				activeRightTab = "console";
				try {
					await pyodideService.runCode(userCode);
				} catch (e) {
					console.error("Run failed", e);
					consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
				}
				return;
			}
			activeRightTab = "tests";
			try {
				const result = await pyodideService.runTests(userCode, content().testHarnessCode, content().id, SAMPLE_TEST_COUNT);
				consoleOutput.set(result.rawOutput?.trim() || "(no output)");
			} catch (e) {
				console.error("Run failed", e);
				consoleOutput.set(`[Run failed]: ${e instanceof Error ? e.message : String(e)}`);
			}
		}
		async function handleRunTests() {
			if (!session.user) {
				signInPrompt.open();
				return;
			}
			if (!content()) return;
			activeRightTab = "tests";
			mobileActiveTab = "output";
			try {
				const result = await pyodideService.runTests(userCode, content().testHarnessCode, content().id);
				attempted.markAttempted(result.contentId);
				if (result.allPassed) solved.markSolved(result.contentId);
			} catch (e) {
				console.error("Test run failed", e);
				consoleOutput.set(`[Submit failed]: ${e instanceof Error ? e.message : String(e)}`);
			}
		}
		let runtimeStatusText = derived(() => {
			switch (store_get($$store_subs ??= {}, "$runtimeState", runtimeState)) {
				case "loading_runtime": return "Loading Python runtime…";
				case "loading_packages": return "Loading NumPy…";
				case "running": return "Executing…";
				case "testing": return "Running tests…";
				case "error": return "Runtime error";
				default: return "Python 3.12 • Shift+Enter to run";
			}
		});
		async function handleToggleFullscreen() {
			try {
				if (document.fullscreenElement) await document.exitFullscreen();
				else await void 0;
			} catch (e) {
				console.error("Fullscreen toggle failed", e);
			}
		}
		head("acuut8", $$renderer, ($$renderer) => {
			$$renderer.push(`<meta name="description" content="Build deep learning framework primitives in Python directly in your browser with TrenTorch."/> `);
			if (content()) $$renderer.push(`<!--[0--><link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin="anonymous"/>`);
			else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]-->`);
		});
		if (!content()) {
			$$renderer.push(`<!--[0--><div class="flex h-[calc(100vh-3.5rem)] w-full flex-col items-center justify-center gap-4 bg-background px-6 text-center"><p class="font-mono text-sm text-muted-foreground">No IDE content published yet for <span class="text-foreground">${escape_html(data.id)}</span>.</p> <a${attr("href", backHref())} class="flex items-center gap-1.5 border border-border bg-secondary px-3 py-1.5 font-mono text-xs text-foreground transition-colors hover:border-foreground/30 hover:bg-muted">`);
			Arrow_left($$renderer, { class: "size-3" });
			$$renderer.push(`<!----> Back to Questions</a></div>`);
		} else {
			$$renderer.push(`<!--[-1--><div class="ide-shell flex h-[calc(100vh-3.5rem)] w-full flex-col overflow-hidden bg-black font-mono text-white">`);
			IdeHeader($$renderer, {
				content: content(),
				fromPage: fromPage(),
				runtimeState: store_get($$store_subs ??= {}, "$runtimeState", runtimeState),
				isRunning: store_get($$store_subs ??= {}, "$isRunning", isRunning),
				isFullscreen,
				onResetCode: handleResetCode,
				onReattempt: handleReattemptQuestion,
				onRunCode: handleRunCode,
				onRunTests: handleRunTests,
				onToggleFullscreen: handleToggleFullscreen
			});
			$$renderer.push(`<!----> <div class="flex border-b border-border bg-secondary text-xs md:hidden"><button type="button"${attr_class(`flex flex-1 items-center justify-center gap-1.5 py-2 ${mobileActiveTab === "guide" ? "border-b-2 border-primary bg-primary font-bold text-primary-foreground" : "text-muted-foreground"}`)}>`);
			Book_open($$renderer, { class: "size-3.5" });
			$$renderer.push(`<!----> <span>Guide</span></button> <button type="button"${attr_class(`flex flex-1 items-center justify-center gap-1.5 py-2 ${mobileActiveTab === "editor" ? "border-b-2 border-primary bg-primary font-bold text-primary-foreground" : "text-muted-foreground"}`)}>`);
			Code_xml($$renderer, { class: "size-3.5" });
			$$renderer.push(`<!----> <span>Editor</span></button> <button type="button"${attr_class(`flex flex-1 items-center justify-center gap-1.5 py-2 ${mobileActiveTab === "output" ? "border-b-2 border-primary bg-primary font-bold text-primary-foreground" : "text-muted-foreground"}`)}>`);
			Terminal($$renderer, { class: "size-3.5" });
			$$renderer.push(`<!----> <span>Output</span></button></div> <div class="flex flex-1 overflow-hidden"><div${attr_class(`ide-left-pane h-full shrink-0 overflow-hidden border-r border-border ${mobileActiveTab === "guide" ? "block w-full" : "hidden md:block"}`, "svelte-acuut8")}${attr_style(`--ide-left-pane-percent: ${stringify(leftPanePercent)}%`)}>`);
			GuidePane($$renderer, {
				content: content(),
				isCompleted: solved.isSolved(content().id),
				prevId: adjacentQuestions().prevId,
				nextId: adjacentQuestions().nextId,
				visibleTabs: guideTabs()
			});
			$$renderer.push(`<!----></div> `);
			PaneResizer($$renderer, {
				axis: "x",
				onResize: handleLeftResize,
				valueNow: leftPanePercent,
				valueMin: 20,
				valueMax: 60,
				class: "hidden md:block"
			});
			$$renderer.push(`<!----> <div${attr_class(`flex h-full flex-1 flex-col overflow-hidden ${mobileActiveTab === "guide" ? "hidden md:flex" : "flex w-full"}`)}><div${attr_class(`flex min-h-[40%] flex-1 flex-col overflow-hidden border-b border-border ${mobileActiveTab === "output" ? "hidden md:flex" : "flex w-full"}`)}><div class="flex h-8 items-center justify-between border-b border-border bg-secondary px-3 text-[11px] text-muted-foreground"><div class="flex items-center gap-1.5">`);
			Code_xml($$renderer, { class: "size-3" });
			$$renderer.push(`<!----> <span>${escape_html(content().id)}.py</span></div> <div${attr_class(`flex items-center gap-1.5 text-[10px] ${store_get($$store_subs ??= {}, "$runtimeState", runtimeState) === "loading_runtime" || store_get($$store_subs ??= {}, "$runtimeState", runtimeState) === "loading_packages" ? "text-amber-600 dark:text-amber-500" : store_get($$store_subs ??= {}, "$runtimeState", runtimeState) === "error" ? "text-red-600 dark:text-red-400" : "text-muted-foreground"}`)}>`);
			if (store_get($$store_subs ??= {}, "$runtimeState", runtimeState) === "loading_runtime" || store_get($$store_subs ??= {}, "$runtimeState", runtimeState) === "loading_packages") $$renderer.push(`<!--[0--><span class="size-1.5 animate-pulse rounded-full bg-amber-500" aria-hidden="true"></span>`);
			else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--> ${escape_html(runtimeStatusText())}</div></div> <div class="flex-1 overflow-hidden">`);
			CodeEditor($$renderer, {
				value: userCode,
				onRun: handleRunCode,
				onChange: handleCodeChange,
				onCursorChange: (pos) => cursorPos = pos
			});
			$$renderer.push(`<!----></div> <div class="flex h-6 shrink-0 items-center justify-between border-t border-border bg-secondary px-3 text-[10px] text-muted-foreground"><span>${escape_html(lastSavedAt ? "Saved" : "")}</span> <span class="tabular-nums">Ln ${escape_html(cursorPos.line)}, Col ${escape_html(cursorPos.col)}</span></div></div> `);
			PaneResizer($$renderer, {
				axis: "y",
				onResize: handleBottomResize,
				valueNow: bottomPanePercent,
				valueMin: 15,
				valueMax: 75,
				class: "hidden md:block"
			});
			$$renderer.push(`<!----> <div${attr_class(`ide-bottom-pane flex min-h-[180px] shrink-0 flex-col overflow-hidden ${mobileActiveTab === "editor" ? "hidden md:flex" : "flex h-[42%] w-full"}`, "svelte-acuut8")}${attr_style(`--ide-bottom-pane-percent: ${stringify(bottomPanePercent)}%`)}><div class="flex h-8 items-center border-b border-border bg-secondary px-1 text-xs"><button type="button"${attr_class(`flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors ${activeRightTab === "tests" ? "border-t-2 border-primary bg-primary font-bold text-primary-foreground" : "text-muted-foreground hover:text-foreground"}`)}>`);
			Shield_check($$renderer, { class: "size-3" });
			$$renderer.push(`<!----> <span>Test Result</span></button> <button type="button"${attr_class(`flex items-center gap-1.5 px-3 py-1 font-mono text-[11px] tracking-wider uppercase transition-colors ${activeRightTab === "console" ? "border-t-2 border-primary bg-primary font-bold text-primary-foreground" : "text-muted-foreground hover:text-foreground"}`)}>`);
			Terminal($$renderer, { class: "size-3" });
			$$renderer.push(`<!----> <span>Console</span></button></div> <div class="flex-1 overflow-hidden">`);
			if (activeRightTab === "tests") {
				$$renderer.push("<!--[0-->");
				TestResultsView($$renderer, { results: store_get($$store_subs ??= {}, "$testResults", testResults) });
			} else {
				$$renderer.push("<!--[-1-->");
				OutputConsole($$renderer, {
					output: store_get($$store_subs ??= {}, "$consoleOutput", consoleOutput),
					onClear: () => pyodideService.consoleOutput.set("")
				});
			}
			$$renderer.push(`<!--]--></div></div></div></div></div>`);
		}
		$$renderer.push(`<!--]-->`);
		if ($$store_subs) unsubscribe_stores($$store_subs);
	});
}
//#endregion
export { _page as default };
