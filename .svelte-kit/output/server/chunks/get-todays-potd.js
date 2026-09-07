import { n as potdEntries } from "./solved.svelte.js";
import { n as questionsById } from "./curriculum-index.js";
//#region processes/potd/to-display-question.ts
var DIFFICULTY_MAP = {
	Beginner: "Easy",
	Intermediate: "Medium",
	Advanced: "Hard",
	Mastery: "Hard"
};
function humanize(kebabCase) {
	return kebabCase.split("-").map((word) => word[0].toUpperCase() + word.slice(1)).join(" ");
}
var POTD_DATE_FORMAT = new Intl.DateTimeFormat("en-US", {
	month: "long",
	day: "numeric",
	year: "numeric"
});
function toDisplayQuestion(generated, date) {
	const title = date ? `${generated.title} (${POTD_DATE_FORMAT.format(new Date(date))})` : generated.title;
	return {
		question: {
			slug: generated.id,
			title,
			difficulty: DIFFICULTY_MAP[generated.difficulty],
			topics: generated.tags
		},
		sectionLabel: humanize(generated.section),
		trackLabel: humanize(generated.track)
	};
}
//#endregion
//#region processes/potd/get-todays-potd.ts
function localDateString(date) {
	return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}
function getTodaysPotd(now = /* @__PURE__ */ new Date()) {
	const today = localDateString(now);
	const entry = potdEntries.find((e) => e.date === today);
	if (!entry) return void 0;
	const generated = questionsById.get(entry.questionId);
	return generated ? toDisplayQuestion(generated, entry.date) : void 0;
}
//#endregion
export { localDateString as n, toDisplayQuestion as r, getTodaysPotd as t };
