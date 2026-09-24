import type { ProfileForm } from './validate-profile';

// The signed-in person's saved profile, shared between the account page's
// identity card and the profile form so a save shows up in the card at once.
let current = $state<ProfileForm | null>(null);

export const profileState = {
	get data(): ProfileForm | null {
		return current;
	},
	set(value: ProfileForm | null) {
		current = value;
	}
};
