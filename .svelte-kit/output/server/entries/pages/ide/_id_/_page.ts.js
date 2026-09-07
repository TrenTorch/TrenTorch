import { t as curriculum } from "../../../../chunks/questions.js";
import { n as questionsById, t as questionsByFullPath } from "../../../../chunks/curriculum-index.js";
//#region processes/ide-content/collapse-signatures.ts
function collapseSignatures(code) {
	return code.replace(/^(def \w+\()\n([\s\S]*?)\n(\)(?:\s*->[^\n:]+)?:)/gm, (_, open, params, close) => {
		return `${open}${params.split("\n").map((line) => line.trim()).filter(Boolean).join(" ").replace(/,$/, "")}${close}`;
	});
}
//#endregion
//#region processes/ide-content/extract-starter-code.ts
function extractStarterCode(statementMarkdown) {
	const match = statementMarkdown.match(/```python\n([\s\S]*?)```/);
	if (!match) return "";
	return `import numpy as np\n\n\n${collapseSignatures(match[1].trimEnd())}\n`;
}
//#endregion
//#region processes/ide-content/strip-load-solution-boilerplate.ts
function stripLoadSolutionBoilerplate(testsCode) {
	const lines = testsCode.split("\n");
	const startIdx = lines.findIndex((line) => line.trim().startsWith("from _load import load_solution"));
	if (startIdx === -1) return {
		cleaned: testsCode,
		dependencyPaths: []
	};
	const moduleVarNames = /* @__PURE__ */ new Set();
	const removedLineIdx = /* @__PURE__ */ new Set([startIdx]);
	function bracketDelta(line) {
		let delta = 0;
		for (const ch of line) if (ch === "(" || ch === "[" || ch === "{") delta++;
		else if (ch === ")" || ch === "]" || ch === "}") delta--;
		return delta;
	}
	let i = startIdx + 1;
	while (i < lines.length) {
		const line = lines[i];
		const trimmed = line.trim();
		if (trimmed === "" || trimmed.startsWith("#")) {
			i++;
			continue;
		}
		let j = i;
		let balance = bracketDelta(line);
		while (balance > 0 && j + 1 < lines.length) {
			j++;
			balance += bracketDelta(lines[j]);
		}
		const statementText = lines.slice(i, j + 1).join("\n");
		const loadCallMatch = /^\s*([A-Za-z_]\w*)\s*=\s*load_solution\s*\(/.exec(statementText);
		if (loadCallMatch) {
			moduleVarNames.add(loadCallMatch[1]);
			for (let k = i; k <= j; k++) removedLineIdx.add(k);
			i = j + 1;
			continue;
		}
		const eqIdx = statementText.indexOf("=");
		if (eqIdx !== -1 && isPureModuleAttributeAlias(statementText, eqIdx, moduleVarNames)) {
			for (let k = i; k <= j; k++) removedLineIdx.add(k);
			i = j + 1;
			continue;
		}
		break;
	}
	const removedText = [...removedLineIdx].sort((a, b) => a - b).map((idx) => lines[idx]).join("\n");
	const dependencyPaths = [...new Set([...removedText.matchAll(/load_solution\(\s*f?["']([^"']+)["']\s*\)/g)].map((m) => m[1]).filter((arg) => !arg.includes("{") && !arg.includes("__file__")))];
	return {
		cleaned: lines.filter((_, idx) => !removedLineIdx.has(idx)).filter((line) => !/^\s*sys\.path\.insert\s*\(/.test(line)).join("\n"),
		dependencyPaths
	};
}
function isPureModuleAttributeAlias(statementText, eqIdx, moduleVarNames) {
	if (moduleVarNames.size === 0) return false;
	const lhs = statementText.slice(0, eqIdx).trim();
	const rhs = statementText.slice(eqIdx + 1).trim();
	const lhsTargets = stripOuterParens(lhs).split(",").map((s) => s.trim()).filter((s) => s.length > 0);
	if (lhsTargets.length === 0) return false;
	if (!lhsTargets.every((t) => /^[A-Za-z_]\w*$/.test(t))) return false;
	const rhsValues = stripOuterParens(rhs).split(",").map((s) => s.trim()).filter((s) => s.length > 0);
	if (rhsValues.length === 0) return false;
	return rhsValues.every((value) => {
		const stripped = stripOuterParens(value);
		const match = /^([A-Za-z_]\w*)\.[A-Za-z_]\w*$/.exec(stripped);
		return match !== null && moduleVarNames.has(match[1]);
	});
}
function stripOuterParens(text) {
	let result = text.trim();
	while (result.startsWith("(") && result.endsWith(")")) result = result.slice(1, -1).trim();
	return result;
}
//#endregion
//#region processes/ide-content/collect-cleaned-dependencies.ts
function collectCleanedDependencies(question) {
	const resolved = /* @__PURE__ */ new Map();
	const visiting = /* @__PURE__ */ new Set();
	function visit(paths) {
		for (const depPath of paths) {
			if (resolved.has(depPath) || visiting.has(depPath)) continue;
			const dep = questionsByFullPath.get(depPath);
			if (!dep) {
				resolved.set(depPath, {
					cleanedCode: "",
					missing: [depPath]
				});
				continue;
			}
			visiting.add(depPath);
			const { cleaned, dependencyPaths } = stripLoadSolutionBoilerplate(dep.oracleSolutionCode);
			visit(dependencyPaths);
			visiting.delete(depPath);
			resolved.set(depPath, {
				cleanedCode: cleaned,
				missing: []
			});
		}
	}
	const fromTests = stripLoadSolutionBoilerplate(question.testsCode).dependencyPaths;
	const fromSolution = stripLoadSolutionBoilerplate(question.oracleSolutionCode).dependencyPaths;
	visit([...fromTests, ...fromSolution]);
	return [...resolved.values()];
}
//#endregion
//#region processes/ide-content/test-collector.ts
var TEST_COLLECTOR = `

def run_tests(limit=None):
    _test_fns = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    if limit is not None:
        _test_fns = _test_fns[:limit]
    tests = []
    for name, fn in _test_fns:
        try:
            fn()
            tests.append({"name": name, "passed": True, "error": None})
        except Exception as e:
            tests.append({"name": name, "passed": False, "error": str(e)})
    return tests
`;
//#endregion
//#region processes/ide-content/build-test-harness.ts
function buildTestHarness(question) {
	const { cleaned } = stripLoadSolutionBoilerplate(question.testsCode);
	return [
		collectCleanedDependencies(question).map(({ cleanedCode, missing }) => missing.length > 0 ? `raise RuntimeError(${JSON.stringify(`Missing dependency '${missing[0]}' for question '${question.id}'`)})` : cleanedCode).join("\n\n"),
		cleaned,
		TEST_COLLECTOR
	].filter(Boolean).join("\n\n");
}
//#endregion
//#region processes/ide-content/to-question-content.ts
function toQuestionContent(question) {
	return {
		id: question.id,
		metadata: {
			name: question.id,
			title: question.title,
			tags: question.tags,
			difficulty: question.difficulty
		},
		descriptionMarkdown: question.statementMarkdown,
		theoryMarkdown: question.theoryMarkdown,
		starterCode: question.starterCode?.trim() ? `${question.starterCode.trimEnd()}\n` : extractStarterCode(question.statementMarkdown),
		solutionCode: question.oracleSolutionCode,
		explanationMarkdown: question.oracleExplanationMarkdown,
		testHarnessCode: buildTestHarness(question)
	};
}
//#endregion
//#region processes/ide-content/load-ide-content.ts
async function loadIdeContent(id) {
	const question = questionsById.get(id);
	return question ? toQuestionContent(question) : null;
}
//#endregion
//#region platform/routes/ide/[id]/+page.ts
var prerender = true;
var entries = () => {
	const ids = /* @__PURE__ */ new Set();
	for (const part of curriculum) for (const track of part.tracks) for (const q of track.questions) ids.add(q.slug);
	return [...ids].map((id) => ({ id }));
};
var load = async ({ params }) => {
	return {
		content: await loadIdeContent(params.id),
		id: params.id
	};
};
//#endregion
export { entries, load, prerender };
