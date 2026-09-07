import "./server.js";
//#region processes/auth/sign-in-prompt.svelte.ts
var isOpen = false;
var signInPrompt = {
	get isOpen() {
		return isOpen;
	},
	set isOpen(value) {
		isOpen = value;
	},
	open() {
		isOpen = true;
	},
	close() {
		isOpen = false;
	}
};
//#endregion
export { signInPrompt as t };
