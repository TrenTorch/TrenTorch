// One shared "please sign in" dialog, opened from wherever an action needs
// an account first (Run/Submit in the IDE, opening Questions or the Problem
// of the Day) rather than each call site owning its own modal instance --
// SignInDialog.svelte (mounted once in the root layout) is the only thing
// that reads `isOpen` and `reason`.
export type SignInReason = 'run' | 'browse';

let isOpen = $state(false);
let reason = $state<SignInReason>('run');

export const signInPrompt = {
	get isOpen(): boolean {
		return isOpen;
	},
	set isOpen(value: boolean) {
		isOpen = value;
	},
	get reason(): SignInReason {
		return reason;
	},
	open(why: SignInReason = 'run') {
		reason = why;
		isOpen = true;
	},
	close() {
		isOpen = false;
	}
};
