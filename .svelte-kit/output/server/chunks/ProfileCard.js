import { a as derived, d as spread_props, k as escape_html } from "./server.js";
import { t as Icon } from "./Icon.js";
import { n as Avatar_image, r as Avatar_fallback, t as Avatar } from "./avatar.js";
//#region node_modules/@lucide/svelte/dist/icons/arrow-right.svelte
function Arrow_right($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "arrow-right",
		"size": 24,
		"node": [["path", { "d": "M5 12h14" }], ["path", { "d": "m12 5 7 7-7 7" }]]
	} }]));
}
//#endregion
//#region platform/components/ProfileCard.svelte
function ProfileCard($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { name, avatarUrl } = $$props;
		const initials = derived(() => name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase());
		$$renderer.push(`<div class="flex items-center gap-3">`);
		if (Avatar) {
			$$renderer.push("<!--[-->");
			Avatar($$renderer, {
				children: ($$renderer) => {
					if (avatarUrl) {
						$$renderer.push("<!--[0-->");
						if (Avatar_image) {
							$$renderer.push("<!--[-->");
							Avatar_image($$renderer, {
								src: avatarUrl,
								alt: name
							});
							$$renderer.push("<!--]-->");
						} else {
							$$renderer.push("<!--[!-->");
							$$renderer.push("<!--]-->");
						}
					} else $$renderer.push("<!--[-1-->");
					$$renderer.push(`<!--]--> `);
					if (Avatar_fallback) {
						$$renderer.push("<!--[-->");
						Avatar_fallback($$renderer, {
							class: "font-mono",
							children: ($$renderer) => {
								$$renderer.push(`<!---->${escape_html(initials())}`);
							},
							$$slots: { default: true }
						});
						$$renderer.push("<!--]-->");
					} else {
						$$renderer.push("<!--[!-->");
						$$renderer.push("<!--]-->");
					}
				},
				$$slots: { default: true }
			});
			$$renderer.push("<!--]-->");
		} else {
			$$renderer.push("<!--[!-->");
			$$renderer.push("<!--]-->");
		}
		$$renderer.push(` <span class="font-mono font-medium">${escape_html(name)}</span></div>`);
	});
}
//#endregion
export { Arrow_right as n, ProfileCard as t };
