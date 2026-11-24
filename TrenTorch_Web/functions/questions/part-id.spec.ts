import { describe, expect, it } from 'vitest';
import type { PagesContext } from '../_lib/env';
import { onRequestGet } from './[partId]';

const go = async (path: string, partId: string) => {
	const context = { request: new Request(`https://trentorch.com${path}`), params: { partId } };
	return onRequestGet(context as unknown as PagesContext);
};

describe('/questions/[partId] redirect', () => {
	it('goes to the module and keeps the topic filter', async () => {
		const res = await go('/questions/part-1?topic=Arrays', 'part-1');
		expect(res.status).toBe(301);
		expect(res.headers.get('location')).toBe(
			'https://trentorch.com/modules/aisys?part=part-1&topic=Arrays'
		);
	});

	it('sends research papers to /papers', async () => {
		const res = await go('/questions/part-research-papers', 'part-research-papers');
		expect(res.headers.get('location')).toBe('https://trentorch.com/papers');
	});
});
