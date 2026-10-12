import { json, type PagesHandler } from '../_lib/env';

const BUG_REPORT_REPO = 'TrenTorch/TrenTorch-Web';
const MAX_FIELD_LENGTH = 10_000;
const MAX_TOKEN_LENGTH = 2048;

interface ReportBugInput {
	whatIsWrong: string;
	profile: string;
	correction: string;
	turnstileToken: string;
	questionId: string;
	questionTitle: string;
	questionUrl: string;
}

function isNonEmptyString(value: unknown, maxLength: number): value is string {
	return typeof value === 'string' && value.trim().length > 0 && value.length <= maxLength;
}

function parseInput(body: unknown): ReportBugInput | null {
	if (typeof body !== 'object' || body === null) return null;
	const b = body as Record<string, unknown>;
	if (
		!isNonEmptyString(b.whatIsWrong, MAX_FIELD_LENGTH) ||
		!isNonEmptyString(b.profile, MAX_FIELD_LENGTH) ||
		!isNonEmptyString(b.correction, MAX_FIELD_LENGTH) ||
		!isNonEmptyString(b.turnstileToken, MAX_TOKEN_LENGTH) ||
		!isNonEmptyString(b.questionId, MAX_FIELD_LENGTH) ||
		!isNonEmptyString(b.questionTitle, MAX_FIELD_LENGTH) ||
		!isNonEmptyString(b.questionUrl, MAX_FIELD_LENGTH)
	) {
		return null;
	}
	return {
		whatIsWrong: b.whatIsWrong as string,
		profile: b.profile as string,
		correction: b.correction as string,
		turnstileToken: b.turnstileToken as string,
		questionId: b.questionId as string,
		questionTitle: b.questionTitle as string,
		questionUrl: b.questionUrl as string
	};
}

// Browser -> this endpoint -> siteverify, never the other way around. Any
// network error, non-2xx, or malformed response fails closed.
async function verifyTurnstile(
	secret: string,
	token: string,
	remoteip: string | null
): Promise<boolean> {
	try {
		const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
			method: 'POST',
			headers: { 'content-type': 'application/x-www-form-urlencoded' },
			signal: AbortSignal.timeout(10_000),
			body: new URLSearchParams({
				secret,
				response: token,
				...(remoteip ? { remoteip } : {})
			})
		});
		if (!response.ok) return false;
		const result = (await response.json()) as { success?: boolean };
		return result.success === true;
	} catch {
		return false;
	}
}

function issueBody(input: ReportBugInput, userAgent: string): string {
	return [
		'## What is wrong',
		input.whatIsWrong,
		'',
		'## Suggested correction',
		input.correction,
		'',
		'## Reported by',
		input.profile,
		'',
		'---',
		`Reported from question: [${input.questionTitle}](${input.questionUrl}) (\`${input.questionId}\`)`,
		`Environment: ${userAgent}`,
		`Submitted: ${new Date().toISOString()}`
	].join('\n');
}

function issueTitle(whatIsWrong: string): string {
	const trimmed = whatIsWrong.trim();
	const truncated = trimmed.length > 80 ? `${trimmed.slice(0, 80)}...` : trimmed;
	return `[Bug] ${truncated}`;
}

export const onRequestPost: PagesHandler = async (context) => {
	try {
		return await handle(context);
	} catch {
		return json({ error: 'unavailable' }, 502);
	}
};

const handle: PagesHandler = async ({ request, env }) => {
	let parsed: unknown;
	try {
		parsed = await request.json();
	} catch {
		return json({ error: 'invalid' }, 400);
	}
	const input = parseInput(parsed);
	if (!input) return json({ error: 'invalid' }, 400);

	const remoteip = request.headers.get('cf-connecting-ip');
	const verified = await verifyTurnstile(
		env.BUG_REPORT_TURNSTILE_SECRET,
		input.turnstileToken,
		remoteip
	);
	if (!verified) return json({ error: 'turnstile_failed' }, 403);

	const response = await fetch(`https://api.github.com/repos/${BUG_REPORT_REPO}/issues`, {
		method: 'POST',
		headers: {
			authorization: `Bearer ${env.BUG_REPORT_GITHUB_TOKEN}`,
			accept: 'application/vnd.github+json',
			'content-type': 'application/json',
			'user-agent': 'trentorch-website-bug-report'
		},
		body: JSON.stringify({
			title: issueTitle(input.whatIsWrong),
			body: issueBody(input, request.headers.get('user-agent') ?? 'unknown'),
			labels: ['bug', 'user-report']
		})
	});
	if (!response.ok) return json({ error: 'github_failed' }, 502);
	const created = (await response.json()) as { html_url?: string };
	if (!created.html_url) return json({ error: 'github_failed' }, 502);

	return json({ issueUrl: created.html_url });
};
