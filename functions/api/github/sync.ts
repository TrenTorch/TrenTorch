import { verifiedUserId } from '../../_lib/auth';
import { decryptToken } from '../../_lib/crypto';
import { connectionKey, json, readConnection, type PagesHandler } from '../../_lib/env';
import { putFile } from '../../_lib/github';
import { commitMessage, parseSolutionInput, solutionFiles } from '../../_lib/solution-files';

const MAX_BODY_BYTES = 120_000;

export const onRequestPost: PagesHandler = async (context) => {
	try {
		return await handle(context);
	} catch {
		// A timeout or network failure talking to Supabase, KV or GitHub.
		return json({ error: 'github_failed' }, 502);
	}
};

const handle: PagesHandler = async ({ request, env }) => {
	const userId = await verifiedUserId(request, env);
	if (!userId) return json({ error: 'unauthorized' }, 401);

	const declared = Number(request.headers.get('content-length') ?? 0);
	if (declared > MAX_BODY_BYTES) return json({ error: 'invalid' }, 413);
	const text = await request.text();
	if (text.length > MAX_BODY_BYTES) return json({ error: 'invalid' }, 413);
	let parsed: unknown = null;
	try {
		parsed = JSON.parse(text);
	} catch {
		// Falls through to the invalid response below.
	}
	const input = parseSolutionInput(parsed);
	if (!input) return json({ error: 'invalid' }, 400);

	const raw = await env.GITHUB_TOKENS.get(connectionKey(userId));
	if (!raw) return json({ error: 'not_connected' }, 409);
	const stored = readConnection(raw);
	if (!stored) return json({ error: 'not_connected' }, 409);
	const { tokenEnc, login } = stored;
	const token = await decryptToken(tokenEnc, env.TOKEN_SECRET);
	if (!token) return json({ error: 'not_connected' }, 409);

	// Sequential on purpose: two parallel writes to one repo race on the branch
	// head and GitHub answers one of them with a conflict.
	const results = [];
	for (const file of solutionFiles(input)) {
		const result = await putFile(token, login, file.path, file.content, commitMessage(input.title));
		if (result === 'unauthorized') {
			// The user revoked access on GitHub: drop the dead token.
			await env.GITHUB_TOKENS.delete(connectionKey(userId));
			return json({ error: 'not_connected' }, 409);
		}
		if (result === 'rate_limited') return json({ error: 'rate_limited' }, 429);
		if (result === 'error') return json({ error: 'github_failed' }, 502);
		results.push(result);
	}
	return json({ ok: true, changed: results.some((r) => r !== 'unchanged') });
};
