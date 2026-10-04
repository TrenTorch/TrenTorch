import { getSupabaseClient } from '$processes/auth/supabase-client';

export async function fetchPublicProblemsetSolved(username: string): Promise<Set<string> | null> {
	try {
		const { data, error } = await getSupabaseClient()
			.rpc('get_public_problemset_solved', { p_username: username })
			.abortSignal(AbortSignal.timeout(15_000));

		if (error) {
			console.error('Failed to load public Problemset progress', error);
			return null;
		}

		const rows = (data ?? []) as { question_id: string }[];
		return new Set(rows.map((row) => row.question_id));
	} catch (error) {
		console.error('Failed to load public Problemset progress', error);
		return null;
	}
}
