import { getSupabaseClient } from '$processes/auth/supabase-client';

// One module-level $state, same shape as session.svelte.ts -- the
// signed-in student's current profiles.user_rating, refreshed on sign-in
// (see RatingSettle.svelte) and pushed directly after a solve (see the
// IDE page's handleRunTests) so the account page's badge updates instantly
// without a refetch round trip.
let rating = $state<number | null>(null);

export const ratingStore = {
	get rating(): number | null {
		return rating;
	},
	setRating(value: number) {
		rating = value;
	},
	async refresh(userId: string): Promise<void> {
		const supabase = getSupabaseClient();
		const { data, error } = await supabase
			.from('profiles')
			.select('user_rating')
			.eq('id', userId)
			.single();
		if (error) {
			console.error('Failed to fetch rating', error);
			return;
		}
		rating = data.user_rating;
	},
	clear() {
		rating = null;
	}
};
