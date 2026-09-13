// One shared "please sign in" dialog, opened from wherever an action needs
// an account first (Run/Submit in the IDE) rather than each call site owning
// its own modal instance -- SignInDialog.svelte (mounted once in the root
// layout) is the only thing that reads `isOpen`.
let isOpen = $state(false);

export const signInPrompt = {
	get isOpen(): boolean {
		return isOpen;
	},
	set isOpen(value: boolean) {
		isOpen = value;
	},
	open() {
		isOpen = true;
	},
	close() {
		isOpen = false;
	}
};
