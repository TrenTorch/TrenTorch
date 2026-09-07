import { D as attr, p as stringify, r as attributes, t as attr_class } from "./server.js";
//#region platform/components/Button.svelte
function Button($$renderer, $$props) {
	let { variant = "default", size = "default", href, target, rel, type = "button", class: className = "", children, $$slots, $$events, ...rest } = $$props;
	const variants = {
		default: "bg-primary text-primary-foreground hover:bg-primary/90",
		outline: "border border-border bg-background hover:bg-accent hover:text-accent-foreground",
		ghost: "hover:bg-accent hover:text-accent-foreground"
	};
	const sizes = {
		default: "h-9 px-4 py-2 text-sm",
		sm: "h-8 px-3 text-sm",
		lg: "h-10 px-6 text-sm",
		icon: "size-9"
	};
	if (href) {
		$$renderer.push(`<!--[0--><a${attr("href", href)}${attr("target", target)}${attr("rel", rel)}${attr_class(`inline-flex shrink-0 items-center justify-center gap-2 rounded-md font-medium whitespace-nowrap transition-colors outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4 ${stringify(variants[variant])} ${stringify(sizes[size])} ${stringify(className)}`)}>`);
		children($$renderer);
		$$renderer.push(`<!----></a>`);
	} else {
		$$renderer.push(`<!--[-1--><button${attributes({
			type,
			class: `inline-flex shrink-0 items-center justify-center gap-2 rounded-md font-medium whitespace-nowrap transition-colors outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg]:size-4 ${stringify(variants[variant])} ${stringify(sizes[size])} ${stringify(className)}`,
			...rest
		})}>`);
		children($$renderer);
		$$renderer.push(`<!----></button>`);
	}
	$$renderer.push(`<!--]-->`);
}
//#endregion
export { Button as t };
