import { verifiedUserId } from '../../_lib/auth';
import { decryptToken } from '../../_lib/crypto';
import { connectionKey, json, type PagesHandler, type StoredConnection } from '../../_lib/env';
import { putFile } from '../../_lib/github';
import { parseSolutionInput, solutionFiles } from '../../_lib/solution-files';

export const onRequestPost: PagesHandler = async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);

	const input = parseSolutionInput(await request.json().catch(() => null));
	if (!input) return json({ error: 'invalid' }, 400);

	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	if (!raw) return json({ error: 'not_connected' }, 409);
	const { tokenEnc, login } = JSON.parse(raw) as StoredConnection;
	const token = await decryptToken(tokenEnc, env.TOKEN_SECRET);
	if (!token) return json({ error: 'not_connected' }, 409);

	// Sequential on purpose: two parallel writes to one repo race on the branch
	// head and GitHub answers one of them with a conflict.
	const results = [];
	for (const file of solutionFiles(input)) {
		const result = await putFile(token, login, file.path, file.content, `Solve ${input.title}`);
		if (result === 'unauthorized') {
			// The user revoked access on GitHub: drop the dead token.
			await env.GITHUB_TOKENS.delete(connectionKey(userId));
			return json({ error: 'not_connected' }, 409);
		}
		if (result === 'error') return json({ error: 'github_failed' }, 502);
		results.push(result);
	}
	return json({ ok: true, changed: results.some((r) => r !== 'unchanged') });
};
