import { t as curriculum } from "../../../../chunks/questions.js";
import { error } from "@sveltejs/kit";
//#region platform/routes/questions/[partId]/+page.ts
var prerender = true;
var entries = () => curriculum.map((part) => ({ partId: part.id }));
var load = ({ params }) => {
	const part = curriculum.find((p) => p.id === params.partId);
	if (!part) error(404, "Track not found");
	return { part };
};
//#endregion
export { entries, load, prerender };
