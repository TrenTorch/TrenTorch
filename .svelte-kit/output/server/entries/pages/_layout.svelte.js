import { D as attr, a as derived, c as head, d as spread_props, i as bind_props, k as escape_html, l as props_id, r as attributes, s as ensure_array_like, t as attr_class } from "../../chunks/server.js";
import { t as resolve } from "../../chunks/paths.js";
import { t as page } from "../../chunks/state.js";
import { n as LogoBadge, r as trentorch_logo_default, t as GithubIcon } from "../../chunks/GithubIcon.js";
import { t as Icon } from "../../chunks/Icon.js";
import { t as Log_out } from "../../chunks/log-out.js";
import { t as Mail } from "../../chunks/mail.js";
import { t as X } from "../../chunks/x.js";
import { a as signInWithGitHub, d as cn, i as session, o as signInWithGoogle, r as Badge, s as signOut } from "../../chunks/solved.svelte.js";
import { E as boxWith, a as boolToEmptyStrOrUndef, b as mergeProps, d as getDataTransitionAttrs, f as attachRef, i as createId, l as createBitsAttrs, n as Avatar_image, r as Avatar_fallback, t as Avatar, u as getDataOpenClosed, v as watch, y as Context } from "../../chunks/avatar.js";
import { a as Escape_layer, c as noop, i as Focus_scope, l as PresenceManager, o as Dismissible_layer, r as Text_selection_layer, s as Portal, t as Scroll_lock } from "../../chunks/scroll-lock.js";
import { t as Button } from "../../chunks/Button.js";
import { t as signInPrompt } from "../../chunks/sign-in-prompt.svelte.js";
//#region node_modules/@lucide/svelte/dist/icons/menu.svelte
function Menu($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "menu",
		"size": 24,
		"node": [
			["path", { "d": "M4 5h16" }],
			["path", { "d": "M4 12h16" }],
			["path", { "d": "M4 19h16" }]
		]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/moon.svelte
function Moon($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "moon",
		"size": 24,
		"node": [["path", { "d": "M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/sun.svelte
function Sun($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "sun",
		"size": 24,
		"node": [
			["circle", {
				"cx": "12",
				"cy": "12",
				"r": "4"
			}],
			["path", { "d": "M12 2v2" }],
			["path", { "d": "M12 20v2" }],
			["path", { "d": "m4.93 4.93 1.41 1.41" }],
			["path", { "d": "m17.66 17.66 1.41 1.41" }],
			["path", { "d": "M2 12h2" }],
			["path", { "d": "M20 12h2" }],
			["path", { "d": "m6.34 17.66-1.41 1.41" }],
			["path", { "d": "m19.07 4.93-1.41 1.41" }]
		]
	} }]));
}
//#endregion
//#region platform/components/ModeToggle.svelte
function ModeToggle($$renderer) {
	$$renderer.push(`<button type="button" aria-label="Toggle theme" class="inline-flex size-9 shrink-0 items-center justify-center rounded-md transition-colors hover:bg-accent hover:text-accent-foreground">`);
	Sun($$renderer, { class: "size-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" });
	$$renderer.push(`<!----> `);
	Moon($$renderer, { class: "absolute size-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0" });
	$$renderer.push(`<!----></button>`);
}
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/dialog.svelte.js
var dialogAttrs = createBitsAttrs({
	component: "dialog",
	parts: [
		"content",
		"trigger",
		"overlay",
		"title",
		"description",
		"close",
		"cancel",
		"action"
	]
});
var DialogRootContext = new Context("Dialog.Root | AlertDialog.Root");
var DialogRootState = class DialogRootState {
	static create(opts) {
		const parent = DialogRootContext.getOr(null);
		return DialogRootContext.set(new DialogRootState(opts, parent));
	}
	opts;
	triggerNode = null;
	contentNode = null;
	overlayNode = null;
	descriptionNode = null;
	contentId = void 0;
	titleId = void 0;
	triggerId = void 0;
	descriptionId = void 0;
	cancelNode = null;
	nestedOpenCount = 0;
	depth;
	parent;
	contentPresence;
	overlayPresence;
	constructor(opts, parent) {
		this.opts = opts;
		this.parent = parent;
		this.depth = parent ? parent.depth + 1 : 0;
		this.handleOpen = this.handleOpen.bind(this);
		this.handleClose = this.handleClose.bind(this);
		this.contentPresence = new PresenceManager({
			ref: boxWith(() => this.contentNode),
			open: this.opts.open,
			enabled: true,
			onComplete: () => {
				this.opts.onOpenChangeComplete.current(this.opts.open.current);
			}
		});
		this.overlayPresence = new PresenceManager({
			ref: boxWith(() => this.overlayNode),
			open: this.opts.open,
			enabled: true
		});
		watch(() => this.opts.open.current, (isOpen) => {
			if (!this.parent) return;
			if (isOpen) this.parent.incrementNested();
			else this.parent.decrementNested();
		}, { lazy: true });
	}
	handleOpen() {
		if (this.opts.open.current) return;
		this.opts.open.current = true;
	}
	handleClose() {
		if (!this.opts.open.current) return;
		this.opts.open.current = false;
	}
	getBitsAttr = (part) => {
		return dialogAttrs.getAttr(part, this.opts.variant.current);
	};
	incrementNested() {
		this.nestedOpenCount++;
		this.parent?.incrementNested();
	}
	decrementNested() {
		if (this.nestedOpenCount === 0) return;
		this.nestedOpenCount--;
		this.parent?.decrementNested();
	}
	#sharedProps = derived(() => ({ "data-state": getDataOpenClosed(this.opts.open.current) }));
	get sharedProps() {
		return this.#sharedProps();
	}
	set sharedProps($$value) {
		return this.#sharedProps($$value);
	}
};
var DialogCloseState = class DialogCloseState {
	static create(opts) {
		return new DialogCloseState(opts, DialogRootContext.get());
	}
	opts;
	root;
	attachment;
	constructor(opts, root) {
		this.opts = opts;
		this.root = root;
		this.attachment = attachRef(this.opts.ref);
		this.onclick = this.onclick.bind(this);
		this.onkeydown = this.onkeydown.bind(this);
	}
	onclick(e) {
		if (this.opts.disabled.current) return;
		if (e.button > 0) return;
		this.root.handleClose();
	}
	onkeydown(e) {
		if (this.opts.disabled.current) return;
		if (e.key === " " || e.key === "Enter") {
			e.preventDefault();
			this.root.handleClose();
		}
	}
	#props = derived(() => ({
		id: this.opts.id.current,
		[this.root.getBitsAttr(this.opts.variant.current)]: "",
		onclick: this.onclick,
		onkeydown: this.onkeydown,
		disabled: this.opts.disabled.current ? true : void 0,
		tabindex: 0,
		...this.root.sharedProps,
		...this.attachment
	}));
	get props() {
		return this.#props();
	}
	set props($$value) {
		return this.#props($$value);
	}
};
var DialogTitleState = class DialogTitleState {
	static create(opts) {
		return new DialogTitleState(opts, DialogRootContext.get());
	}
	opts;
	root;
	attachment;
	constructor(opts, root) {
		this.opts = opts;
		this.root = root;
		this.root.titleId = this.opts.id.current;
		this.attachment = attachRef(this.opts.ref);
		watch.pre(() => this.opts.id.current, (id) => {
			this.root.titleId = id;
		});
	}
	#props = derived(() => ({
		id: this.opts.id.current,
		role: "heading",
		"aria-level": this.opts.level.current,
		[this.root.getBitsAttr("title")]: "",
		...this.root.sharedProps,
		...this.attachment
	}));
	get props() {
		return this.#props();
	}
	set props($$value) {
		return this.#props($$value);
	}
};
var DialogDescriptionState = class DialogDescriptionState {
	static create(opts) {
		return new DialogDescriptionState(opts, DialogRootContext.get());
	}
	opts;
	root;
	attachment;
	constructor(opts, root) {
		this.opts = opts;
		this.root = root;
		this.root.descriptionId = this.opts.id.current;
		this.attachment = attachRef(this.opts.ref, (v) => {
			this.root.descriptionNode = v;
		});
		watch.pre(() => this.opts.id.current, (id) => {
			this.root.descriptionId = id;
		});
	}
	#props = derived(() => ({
		id: this.opts.id.current,
		[this.root.getBitsAttr("description")]: "",
		...this.root.sharedProps,
		...this.attachment
	}));
	get props() {
		return this.#props();
	}
	set props($$value) {
		return this.#props($$value);
	}
};
var DialogContentState = class DialogContentState {
	static create(opts) {
		return new DialogContentState(opts, DialogRootContext.get());
	}
	opts;
	root;
	attachment;
	constructor(opts, root) {
		this.opts = opts;
		this.root = root;
		this.attachment = attachRef(this.opts.ref, (v) => {
			this.root.contentNode = v;
			this.root.contentId = v?.id;
		});
	}
	#snippetProps = derived(() => ({ open: this.root.opts.open.current }));
	get snippetProps() {
		return this.#snippetProps();
	}
	set snippetProps($$value) {
		return this.#snippetProps($$value);
	}
	#props = derived(() => ({
		id: this.opts.id.current,
		role: this.root.opts.variant.current === "alert-dialog" ? "alertdialog" : "dialog",
		"aria-modal": "true",
		"aria-describedby": this.root.descriptionId,
		"aria-labelledby": this.root.titleId,
		[this.root.getBitsAttr("content")]: "",
		style: {
			pointerEvents: "auto",
			outline: this.root.opts.variant.current === "alert-dialog" ? "none" : void 0,
			"--bits-dialog-depth": this.root.depth,
			"--bits-dialog-nested-count": this.root.nestedOpenCount,
			contain: "layout style"
		},
		tabindex: this.root.opts.variant.current === "alert-dialog" ? -1 : void 0,
		"data-nested-open": boolToEmptyStrOrUndef(this.root.nestedOpenCount > 0),
		"data-nested": boolToEmptyStrOrUndef(this.root.parent !== null),
		...getDataTransitionAttrs(this.root.contentPresence.transitionStatus),
		...this.root.sharedProps,
		...this.attachment
	}));
	get props() {
		return this.#props();
	}
	set props($$value) {
		return this.#props($$value);
	}
	get shouldRender() {
		return this.root.contentPresence.shouldRender;
	}
};
var DialogOverlayState = class DialogOverlayState {
	static create(opts) {
		return new DialogOverlayState(opts, DialogRootContext.get());
	}
	opts;
	root;
	attachment;
	constructor(opts, root) {
		this.opts = opts;
		this.root = root;
		this.attachment = attachRef(this.opts.ref, (v) => this.root.overlayNode = v);
	}
	#snippetProps = derived(() => ({ open: this.root.opts.open.current }));
	get snippetProps() {
		return this.#snippetProps();
	}
	set snippetProps($$value) {
		return this.#snippetProps($$value);
	}
	#props = derived(() => ({
		id: this.opts.id.current,
		[this.root.getBitsAttr("overlay")]: "",
		style: {
			pointerEvents: "auto",
			"--bits-dialog-depth": this.root.depth,
			"--bits-dialog-nested-count": this.root.nestedOpenCount
		},
		"data-nested-open": boolToEmptyStrOrUndef(this.root.nestedOpenCount > 0),
		"data-nested": boolToEmptyStrOrUndef(this.root.parent !== null),
		...getDataTransitionAttrs(this.root.overlayPresence.transitionStatus),
		...this.root.sharedProps,
		...this.attachment
	}));
	get props() {
		return this.#props();
	}
	set props($$value) {
		return this.#props($$value);
	}
	get shouldRender() {
		return this.root.overlayPresence.shouldRender;
	}
};
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/components/dialog-title.svelte
function Dialog_title$1($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const uid = props_id($$renderer);
		let { id = createId(uid), ref = null, child, children, level = 2, $$slots, $$events, ...restProps } = $$props;
		const titleState = DialogTitleState.create({
			id: boxWith(() => id),
			level: boxWith(() => level),
			ref: boxWith(() => ref, (v) => ref = v)
		});
		const mergedProps = derived(() => mergeProps(restProps, titleState.props));
		if (child) {
			$$renderer.push("<!--[0-->");
			child($$renderer, { props: mergedProps() });
			$$renderer.push(`<!---->`);
		} else {
			$$renderer.push(`<!--[-1--><div${attributes({ ...mergedProps() })}>`);
			children?.($$renderer);
			$$renderer.push(`<!----></div>`);
		}
		$$renderer.push(`<!--]-->`);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/components/dialog-overlay.svelte
function Dialog_overlay$1($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const uid = props_id($$renderer);
		let { id = createId(uid), forceMount = false, child, children, ref = null, $$slots, $$events, ...restProps } = $$props;
		const overlayState = DialogOverlayState.create({
			id: boxWith(() => id),
			ref: boxWith(() => ref, (v) => ref = v)
		});
		const mergedProps = derived(() => mergeProps(restProps, overlayState.props));
		if (overlayState.shouldRender || forceMount) {
			$$renderer.push("<!--[0-->");
			if (child) {
				$$renderer.push("<!--[0-->");
				child($$renderer, {
					props: mergeProps(mergedProps()),
					...overlayState.snippetProps
				});
				$$renderer.push(`<!---->`);
			} else {
				$$renderer.push(`<!--[-1--><div${attributes({ ...mergeProps(mergedProps()) })}>`);
				children?.($$renderer, overlayState.snippetProps);
				$$renderer.push(`<!----></div>`);
			}
			$$renderer.push(`<!--]-->`);
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]-->`);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/components/dialog-description.svelte
function Dialog_description$1($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const uid = props_id($$renderer);
		let { id = createId(uid), children, child, ref = null, $$slots, $$events, ...restProps } = $$props;
		const descriptionState = DialogDescriptionState.create({
			id: boxWith(() => id),
			ref: boxWith(() => ref, (v) => ref = v)
		});
		const mergedProps = derived(() => mergeProps(restProps, descriptionState.props));
		if (child) {
			$$renderer.push("<!--[0-->");
			child($$renderer, { props: mergedProps() });
			$$renderer.push(`<!---->`);
		} else {
			$$renderer.push(`<!--[-1--><div${attributes({ ...mergedProps() })}>`);
			children?.($$renderer);
			$$renderer.push(`<!----></div>`);
		}
		$$renderer.push(`<!--]-->`);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/components/dialog.svelte
function Dialog$1($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { open = false, onOpenChange = noop, onOpenChangeComplete = noop, children } = $$props;
		DialogRootState.create({
			variant: boxWith(() => "dialog"),
			open: boxWith(() => open, (v) => {
				open = v;
				onOpenChange(v);
			}),
			onOpenChangeComplete: boxWith(() => onOpenChangeComplete)
		});
		children?.($$renderer);
		$$renderer.push(`<!---->`);
		bind_props($$props, { open });
	});
}
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/components/dialog-close.svelte
function Dialog_close($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const uid = props_id($$renderer);
		let { children, child, id = createId(uid), ref = null, disabled = false, $$slots, $$events, ...restProps } = $$props;
		const closeState = DialogCloseState.create({
			variant: boxWith(() => "close"),
			id: boxWith(() => id),
			ref: boxWith(() => ref, (v) => ref = v),
			disabled: boxWith(() => Boolean(disabled))
		});
		const mergedProps = derived(() => mergeProps(restProps, closeState.props));
		if (child) {
			$$renderer.push("<!--[0-->");
			child($$renderer, { props: mergedProps() });
			$$renderer.push(`<!---->`);
		} else {
			$$renderer.push(`<!--[-1--><button${attributes({ ...mergedProps() })}>`);
			children?.($$renderer);
			$$renderer.push(`<!----></button>`);
		}
		$$renderer.push(`<!--]-->`);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region node_modules/bits-ui/dist/bits/dialog/components/dialog-content.svelte
function Dialog_content$1($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const uid = props_id($$renderer);
		let { id = createId(uid), children, child, ref = null, forceMount = false, onCloseAutoFocus = noop, onOpenAutoFocus = noop, onEscapeKeydown = noop, onInteractOutside = noop, trapFocus = true, preventScroll = true, restoreScrollDelay = null, $$slots, $$events, ...restProps } = $$props;
		const contentState = DialogContentState.create({
			id: boxWith(() => id),
			ref: boxWith(() => ref, (v) => ref = v)
		});
		const mergedProps = derived(() => mergeProps(restProps, contentState.props));
		if (contentState.shouldRender || forceMount) {
			$$renderer.push("<!--[0-->");
			{
				function focusScope($$renderer, { props: focusScopeProps }) {
					Escape_layer($$renderer, spread_props([mergedProps(), {
						enabled: contentState.root.opts.open.current,
						ref: contentState.opts.ref,
						onEscapeKeydown: (e) => {
							onEscapeKeydown(e);
							if (e.defaultPrevented) return;
							contentState.root.handleClose();
						},
						children: ($$renderer) => {
							Dismissible_layer($$renderer, spread_props([mergedProps(), {
								ref: contentState.opts.ref,
								enabled: contentState.root.opts.open.current,
								onInteractOutside: (e) => {
									onInteractOutside(e);
									if (e.defaultPrevented) return;
									contentState.root.handleClose();
								},
								children: ($$renderer) => {
									Text_selection_layer($$renderer, spread_props([mergedProps(), {
										ref: contentState.opts.ref,
										enabled: contentState.root.opts.open.current,
										children: ($$renderer) => {
											if (child) {
												$$renderer.push("<!--[0-->");
												if (contentState.root.opts.open.current) {
													$$renderer.push("<!--[0-->");
													Scroll_lock($$renderer, {
														preventScroll,
														restoreScrollDelay
													});
												} else $$renderer.push("<!--[-1-->");
												$$renderer.push(`<!--]--> `);
												child($$renderer, {
													props: mergeProps(mergedProps(), focusScopeProps),
													...contentState.snippetProps
												});
												$$renderer.push(`<!---->`);
											} else {
												$$renderer.push("<!--[-1-->");
												Scroll_lock($$renderer, { preventScroll });
												$$renderer.push(`<!----> <div${attributes({ ...mergeProps(mergedProps(), focusScopeProps) })}>`);
												children?.($$renderer);
												$$renderer.push(`<!----></div>`);
											}
											$$renderer.push(`<!--]-->`);
										},
										$$slots: { default: true }
									}]));
								},
								$$slots: { default: true }
							}]));
						},
						$$slots: { default: true }
					}]));
				}
				Focus_scope($$renderer, {
					ref: contentState.opts.ref,
					loop: true,
					trapFocus,
					enabled: contentState.root.opts.open.current,
					onOpenAutoFocus,
					onCloseAutoFocus,
					focusScope,
					$$slots: { focusScope: true }
				});
			}
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]-->`);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region platform/components/AccountButton.svelte
function AccountButton($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const initial = derived(() => (session.user?.email ?? session.user?.user_metadata?.full_name)?.[0]?.toUpperCase() ?? "?");
		$$renderer.push(`<a${attr("href", resolve("/account"))} class="inline-flex size-9 items-center justify-center rounded-md transition-colors hover:bg-accent hover:text-accent-foreground"${attr("aria-label", session.user ? "Your account" : "Sign in")}>`);
		if (Avatar) {
			$$renderer.push("<!--[-->");
			Avatar($$renderer, {
				class: "size-7",
				children: ($$renderer) => {
					if (session.user?.user_metadata?.avatar_url) {
						$$renderer.push("<!--[0-->");
						if (Avatar_image) {
							$$renderer.push("<!--[-->");
							Avatar_image($$renderer, {
								src: session.user.user_metadata.avatar_url,
								alt: ""
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
							class: "font-mono text-xs",
							children: ($$renderer) => {
								$$renderer.push(`<!---->${escape_html(initial())}`);
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
		$$renderer.push(`</a>`);
	});
}
//#endregion
//#region platform/components/Navbar.svelte
function Navbar($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const GITHUB_URL = "https://github.com/TrenTorch/TrenTorch";
		const routes = [
			{
				href: resolve("/"),
				label: "Home"
			},
			{
				href: resolve("/questions"),
				label: "Questions"
			},
			{
				href: resolve("/potd"),
				label: "Problem of the day",
				pill: "new"
			}
		];
		$$renderer.push(`<header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"><div class="container flex h-14 items-center justify-between px-4 md:px-6"><a${attr("href", resolve("/"))} class="group flex items-center gap-2">`);
		LogoBadge($$renderer, { class: "size-7" });
		$$renderer.push(`<!----> <span class="font-mono text-base font-bold tracking-wide text-foreground sm:inline-block">TrenTorch</span></a> <div class="hidden flex-1 items-center justify-end space-x-6 md:flex"><nav class="flex items-center space-x-6 font-mono text-xs tracking-wider uppercase"><!--[-->`);
		const each_array = ensure_array_like(routes);
		for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
			let route = each_array[$$index];
			$$renderer.push(`<a${attr("href", route.href)}${attr_class(`flex items-center gap-1.5 transition-colors hover:text-primary ${page.url.pathname === route.href ? "text-primary" : "text-foreground/60"}`)}>${escape_html(route.label)} `);
			if (route.pill === "new") {
				$$renderer.push("<!--[0-->");
				Badge($$renderer, {
					variant: "destructive",
					class: "h-4 px-1 text-[9px] normal-case",
					children: ($$renderer) => {
						$$renderer.push(`<!---->new`);
					},
					$$slots: { default: true }
				});
			} else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--></a>`);
		}
		$$renderer.push(`<!--]--> <span class="flex cursor-not-allowed items-center gap-1.5 text-foreground/30" title="Coming soon">Roadmap `);
		Badge($$renderer, {
			variant: "outline",
			class: "h-4 px-1 text-[9px] text-foreground/40 normal-case",
			children: ($$renderer) => {
				$$renderer.push(`<!---->soon`);
			},
			$$slots: { default: true }
		});
		$$renderer.push(`<!----></span></nav> `);
		Button($$renderer, {
			variant: "outline",
			size: "sm",
			href: GITHUB_URL,
			target: "_blank",
			rel: "noopener noreferrer",
			children: ($$renderer) => {
				GithubIcon($$renderer, { class: "size-4" });
				$$renderer.push(`<!----> GitHub `);
				$$renderer.push("<!--[-1-->");
				$$renderer.push(`<!--]-->`);
			},
			$$slots: { default: true }
		});
		$$renderer.push(`<!----> `);
		ModeToggle($$renderer, {});
		$$renderer.push(`<!----> `);
		AccountButton($$renderer, {});
		$$renderer.push(`<!----></div> <div class="flex items-center space-x-2 md:hidden">`);
		Button($$renderer, {
			variant: "ghost",
			size: "icon",
			href: GITHUB_URL,
			target: "_blank",
			rel: "noopener noreferrer",
			children: ($$renderer) => {
				GithubIcon($$renderer, { class: "size-5" });
				$$renderer.push(`<!----> <span class="sr-only">GitHub</span>`);
			},
			$$slots: { default: true }
		});
		$$renderer.push(`<!----> `);
		ModeToggle($$renderer, {});
		$$renderer.push(`<!----> `);
		AccountButton($$renderer, {});
		$$renderer.push(`<!----> <button type="button" class="inline-flex size-9 items-center justify-center rounded-md hover:bg-accent hover:text-accent-foreground md:hidden"><span class="sr-only">Toggle menu</span> `);
		$$renderer.push("<!--[-1-->");
		Menu($$renderer, { class: "size-5" });
		$$renderer.push(`<!--]--></button></div></div> `);
		$$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></header>`);
	});
}
//#endregion
//#region platform/components/Footer.svelte
function Footer($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		$$renderer.push(`<footer class="border-t py-6 md:px-8"><div class="container flex flex-col items-center justify-between gap-3 md:flex-row"><p class="text-center text-sm leading-loose text-balance text-muted-foreground md:text-left">© ${escape_html((/* @__PURE__ */ new Date()).getFullYear())} TrenTorch. Source-available, free for <a href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/LICENSE" class="font-medium underline underline-offset-4 hover:text-foreground">personal and educational use</a> , and follows a <a href="https://github.com/TrenTorch/TrenTorch-Web/blob/main/CODE_OF_CONDUCT.md" class="font-medium underline underline-offset-4 hover:text-foreground">Code of Conduct</a> .</p> <nav class="flex items-center gap-4 font-mono text-sm text-muted-foreground"><a href="https://github.com/TrenTorch" class="transition-colors hover:text-foreground">github.com/TrenTorch</a> <a${attr("href", resolve("/terms"))} class="transition-colors hover:text-foreground">Terms</a> <a${attr("href", resolve("/privacy"))} class="transition-colors hover:text-foreground">Privacy</a> <a${attr("href", resolve("/contact"))} class="transition-colors hover:text-foreground">Contact</a> <a href="https://discord.gg/2hSsftQCZ9" target="_blank" rel="noopener noreferrer" class="transition-colors hover:text-foreground">Discord</a></nav></div></footer>`);
	});
}
//#endregion
//#region platform/components/ui/dialog/dialog-overlay.svelte
function Dialog_overlay($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { ref = null, class: className, $$slots, $$events, ...restProps } = $$props;
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			if (Dialog_overlay$1) {
				$$renderer.push("<!--[-->");
				Dialog_overlay$1($$renderer, spread_props([
					{
						"data-slot": "dialog-overlay",
						class: cn("data-open:animate-in data-open:fade-in-0 data-closed:animate-out data-closed:fade-out-0 fixed inset-0 z-50 bg-black/50", className)
					},
					restProps,
					{
						get ref() {
							return ref;
						},
						set ref($$value) {
							ref = $$value;
							$$settled = false;
						}
					}
				]));
				$$renderer.push("<!--]-->");
			} else {
				$$renderer.push("<!--[!-->");
				$$renderer.push("<!--]-->");
			}
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region platform/components/ui/dialog/dialog-portal.svelte
function Dialog_portal($$renderer, $$props) {
	let { $$slots, $$events, ...restProps } = $$props;
	if (Portal) {
		$$renderer.push("<!--[-->");
		Portal($$renderer, spread_props([restProps]));
		$$renderer.push("<!--]-->");
	} else {
		$$renderer.push("<!--[!-->");
		$$renderer.push("<!--]-->");
	}
}
//#endregion
//#region platform/components/ui/dialog/dialog-content.svelte
function Dialog_content($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { ref = null, class: className, children, $$slots, $$events, ...restProps } = $$props;
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			Dialog_portal($$renderer, {
				children: ($$renderer) => {
					Dialog_overlay($$renderer, {});
					$$renderer.push(`<!----> `);
					if (Dialog_content$1) {
						$$renderer.push("<!--[-->");
						Dialog_content$1($$renderer, spread_props([
							{
								"data-slot": "dialog-content",
								class: cn("data-open:animate-in data-open:fade-in-0 data-open:zoom-in-95 data-closed:animate-out data-closed:fade-out-0 data-closed:zoom-out-95 fixed top-1/2 left-1/2 z-50 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-md border border-border bg-popover p-7 text-popover-foreground shadow-lg duration-100", className)
							},
							restProps,
							{
								get ref() {
									return ref;
								},
								set ref($$value) {
									ref = $$value;
									$$settled = false;
								},
								children: ($$renderer) => {
									children?.($$renderer);
									$$renderer.push(`<!----> `);
									if (Dialog_close) {
										$$renderer.push("<!--[-->");
										Dialog_close($$renderer, {
											class: "absolute top-4 right-4 rounded-xs text-muted-foreground opacity-70 transition-opacity hover:opacity-100 focus:outline-none",
											children: ($$renderer) => {
												X($$renderer, { class: "size-4" });
												$$renderer.push(`<!----> <span class="sr-only">Close</span>`);
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
							}
						]));
						$$renderer.push("<!--]-->");
					} else {
						$$renderer.push("<!--[!-->");
						$$renderer.push("<!--]-->");
					}
				},
				$$slots: { default: true }
			});
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region platform/components/ui/dialog/dialog-description.svelte
function Dialog_description($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { ref = null, class: className, $$slots, $$events, ...restProps } = $$props;
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			if (Dialog_description$1) {
				$$renderer.push("<!--[-->");
				Dialog_description$1($$renderer, spread_props([
					{
						"data-slot": "dialog-description",
						class: cn("text-sm text-muted-foreground", className)
					},
					restProps,
					{
						get ref() {
							return ref;
						},
						set ref($$value) {
							ref = $$value;
							$$settled = false;
						}
					}
				]));
				$$renderer.push("<!--]-->");
			} else {
				$$renderer.push("<!--[!-->");
				$$renderer.push("<!--]-->");
			}
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region platform/components/ui/dialog/dialog-title.svelte
function Dialog_title($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { ref = null, class: className, $$slots, $$events, ...restProps } = $$props;
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			if (Dialog_title$1) {
				$$renderer.push("<!--[-->");
				Dialog_title$1($$renderer, spread_props([
					{
						"data-slot": "dialog-title",
						class: cn("font-mono text-base font-semibold", className)
					},
					restProps,
					{
						get ref() {
							return ref;
						},
						set ref($$value) {
							ref = $$value;
							$$settled = false;
						}
					}
				]));
				$$renderer.push("<!--]-->");
			} else {
				$$renderer.push("<!--[!-->");
				$$renderer.push("<!--]-->");
			}
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
		bind_props($$props, { ref });
	});
}
//#endregion
//#region platform/components/ui/dialog/dialog.svelte
function Dialog($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { open = false, $$slots, $$events, ...restProps } = $$props;
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			if (Dialog$1) {
				$$renderer.push("<!--[-->");
				Dialog$1($$renderer, spread_props([restProps, {
					get open() {
						return open;
					},
					set open($$value) {
						open = $$value;
						$$settled = false;
					}
				}]));
				$$renderer.push("<!--]-->");
			} else {
				$$renderer.push("<!--[!-->");
				$$renderer.push("<!--]-->");
			}
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
		bind_props($$props, { open });
	});
}
//#endregion
//#region platform/components/AuthPanel.svelte
function AuthPanel($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let email = "";
		let isSendingLink = false;
		if (session.isLoading) $$renderer.push(`<!--[0--><div class="text-sm text-muted-foreground">Checking sign-in status...</div>`);
		else if (session.user) {
			$$renderer.push(`<!--[1--><div class="flex items-center justify-between gap-4"><p class="text-sm text-muted-foreground">Signed in as <span class="font-medium text-foreground">${escape_html(session.user.email)}</span></p> `);
			Button($$renderer, {
				variant: "outline",
				size: "sm",
				onclick: signOut,
				children: ($$renderer) => {
					Log_out($$renderer, { class: "size-3.5" });
					$$renderer.push(`<!----> Sign out`);
				},
				$$slots: { default: true }
			});
			$$renderer.push(`<!----></div>`);
		} else {
			$$renderer.push(`<!--[-1--><div class="flex flex-col gap-3"><div class="grid grid-cols-1 gap-3 sm:grid-cols-2">`);
			Button($$renderer, {
				variant: "outline",
				class: "w-full",
				onclick: signInWithGitHub,
				children: ($$renderer) => {
					GithubIcon($$renderer, { class: "size-4" });
					$$renderer.push(`<!----> Continue with GitHub`);
				},
				$$slots: { default: true }
			});
			$$renderer.push(`<!----> `);
			Button($$renderer, {
				variant: "outline",
				class: "w-full",
				onclick: signInWithGoogle,
				children: ($$renderer) => {
					$$renderer.push(`<svg viewBox="0 0 24 24" class="size-4" aria-hidden="true"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"></path><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"></path><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93z"></path><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"></path></svg> Continue with Google`);
				},
				$$slots: { default: true }
			});
			$$renderer.push(`<!----></div> <div class="flex items-center gap-3 text-xs text-muted-foreground"><div class="h-px flex-1 bg-border"></div> <span>or</span> <div class="h-px flex-1 bg-border"></div></div> `);
			$$renderer.push(`<!--[-1--><form class="flex flex-col gap-2 sm:flex-row"><input type="email" required="" placeholder="you@example.com"${attr("value", email)} class="flex-1 rounded-md border border-input bg-background px-3 py-1.5 text-sm outline-none focus-visible:ring-1 focus-visible:ring-ring"/> `);
			Button($$renderer, {
				type: "submit",
				variant: "outline",
				size: "sm",
				disabled: isSendingLink,
				children: ($$renderer) => {
					Mail($$renderer, { class: "size-3.5" });
					$$renderer.push(`<!----> ${escape_html("Email me a link")}`);
				},
				$$slots: { default: true }
			});
			$$renderer.push(`<!----></form> `);
			$$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]-->`);
			$$renderer.push(`<!--]--></div>`);
		}
		$$renderer.push(`<!--]-->`);
	});
}
//#endregion
//#region platform/components/SignInDialog.svelte
function SignInDialog($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			if (Dialog) {
				$$renderer.push("<!--[-->");
				Dialog($$renderer, {
					get open() {
						return signInPrompt.isOpen;
					},
					set open($$value) {
						signInPrompt.isOpen = $$value;
						$$settled = false;
					},
					children: ($$renderer) => {
						if (Dialog_content) {
							$$renderer.push("<!--[-->");
							Dialog_content($$renderer, {
								children: ($$renderer) => {
									if (Dialog_title) {
										$$renderer.push("<!--[-->");
										Dialog_title($$renderer, {
											children: ($$renderer) => {
												$$renderer.push(`<!---->Sign in to run your code`);
											},
											$$slots: { default: true }
										});
										$$renderer.push("<!--]-->");
									} else {
										$$renderer.push("<!--[!-->");
										$$renderer.push("<!--]-->");
									}
									$$renderer.push(` `);
									if (Dialog_description) {
										$$renderer.push("<!--[-->");
										Dialog_description($$renderer, {
											class: "mb-4",
											children: ($$renderer) => {
												$$renderer.push(`<!---->Running and submitting solutions needs an account, so your progress can actually be saved.`);
											},
											$$slots: { default: true }
										});
										$$renderer.push("<!--]-->");
									} else {
										$$renderer.push("<!--[!-->");
										$$renderer.push("<!--]-->");
									}
									$$renderer.push(` `);
									AuthPanel($$renderer, {});
									$$renderer.push(`<!---->`);
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
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
	});
}
//#endregion
//#region platform/components/ProgressSync.svelte
function ProgressSync($$renderer, $$props) {
	$$renderer.component(($$renderer) => {});
}
//#endregion
//#region platform/routes/+layout.svelte
function _layout($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { children } = $$props;
		let showFooter = derived(() => page.url.pathname === "/");
		head("1op4q0a", $$renderer, ($$renderer) => {
			$$renderer.title(($$renderer) => {
				$$renderer.push(`<title>TrenTorch</title>`);
			});
			$$renderer.push(`<link rel="icon" type="image/webp"${attr("href", trentorch_logo_default)}/> <meta name="description" content="TrenTorch: an educational ML framework you build by hand, running straight in your browser."/>`);
		});
		$$renderer.push(`<div class="relative flex min-h-screen flex-col">`);
		Navbar($$renderer, {});
		$$renderer.push(`<!----> <div class="w-full flex-1">`);
		children($$renderer);
		$$renderer.push(`<!----></div> `);
		if (showFooter()) {
			$$renderer.push("<!--[0-->");
			Footer($$renderer, {});
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></div> `);
		SignInDialog($$renderer, {});
		$$renderer.push(`<!----> `);
		ProgressSync($$renderer, {});
		$$renderer.push(`<!---->`);
	});
}
//#endregion
export { _layout as default };
