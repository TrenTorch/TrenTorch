import { D as attr, c as head, k as escape_html, s as ensure_array_like } from "../../../chunks/server.js";
import { t as Mail } from "../../../chunks/mail.js";
import { t as X } from "../../../chunks/x.js";
//#region platform/routes/contact/+page.svelte
function _page($$renderer) {
	const X_ACCOUNTS = [
		{
			handle: "@Rocky_T07",
			url: "https://x.com/Rocky_T07"
		},
		{
			handle: "@maanas_tyagi",
			url: "https://x.com/maanas_tyagi"
		},
		{
			handle: "@aadityansha_06",
			url: "https://x.com/aadityansha_06"
		},
		{
			handle: "@ShivtejG236",
			url: "https://x.com/ShivtejG236"
		}
	];
	head("qvq1zc", $$renderer, ($$renderer) => {
		$$renderer.push(`<meta name="description" content="Get in touch with the TrenTorch team."/>`);
	});
	$$renderer.push(`<div class="container max-w-3xl px-4 py-12 md:px-6"><h1 class="mb-1 font-mono text-2xl font-bold tracking-tight">Contact</h1> <p class="mb-8 text-sm text-muted-foreground">Found a bug, have feedback, or want to reach out?</p> <h2 class="mb-3 font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase">Email</h2> <a href="mailto:engineering@trentorch.com" class="mb-8 flex items-center gap-3 rounded-md border border-border p-4 transition-colors hover:border-foreground/30 hover:bg-secondary"><span class="flex size-9 shrink-0 items-center justify-center rounded-md border border-border bg-secondary">`);
	Mail($$renderer, {
		class: "size-4 text-foreground/80",
		"aria-hidden": "true"
	});
	$$renderer.push(`<!----></span> <span class="font-medium">engineering@trentorch.com</span></a> <h2 class="mb-3 font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase">Follow us on X</h2> <div class="grid gap-3 sm:grid-cols-2"><!--[-->`);
	const each_array = ensure_array_like(X_ACCOUNTS);
	for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
		let account = each_array[$$index];
		$$renderer.push(`<a${attr("href", account.url)} target="_blank" rel="noopener noreferrer external" class="flex items-center gap-3 rounded-md border border-border p-4 transition-colors hover:border-foreground/30 hover:bg-secondary"><span class="flex size-9 shrink-0 items-center justify-center rounded-full border border-border bg-secondary">`);
		X($$renderer, {
			class: "size-4 text-foreground/80",
			"aria-hidden": "true"
		});
		$$renderer.push(`<!----></span> <span class="font-medium">${escape_html(account.handle)}</span></a>`);
	}
	$$renderer.push(`<!--]--></div></div>`);
}
//#endregion
export { _page as default };
