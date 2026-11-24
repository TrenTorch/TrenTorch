import { describe, it, expect, afterEach } from 'vitest';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { BLOGS_DIR, readBlogTracks, readBlogPosts, renderPost } from './read-blogs';

let dirs: string[] = [];
afterEach(() => {
	for (const dir of dirs) rmSync(dir, { recursive: true, force: true });
	dirs = [];
});

const post = (overrides: Record<string, unknown> = {}) => ({
	title: 'Why the virtual GPU',
	post: {
		title: 'Why the virtual GPU',
		author: 'A. Writer',
		date: '2026-11-24',
		summary: 'How the browser runs CUDA.',
		...overrides
	}
});

function build(
	tracks: {
		folder: string;
		meta?: object;
		posts: { folder: string; meta?: object; md?: string }[];
	}[]
): string {
	const base = mkdtempSync(join(tmpdir(), 'blogs-'));
	dirs.push(base);
	const root = join(base, BLOGS_DIR);
	mkdirSync(root, { recursive: true });
	for (const t of tracks) {
		const trackDir = join(root, t.folder);
		mkdirSync(trackDir, { recursive: true });
		writeFileSync(
			join(trackDir, 'meta.json'),
			JSON.stringify(t.meta ?? { title: 'Engineering', description: 'How we build it' })
		);
		for (const p of t.posts) {
			const dir = join(trackDir, p.folder);
			mkdirSync(dir);
			writeFileSync(join(dir, 'meta.json'), JSON.stringify(p.meta ?? post()));
			if (p.md !== undefined) writeFileSync(join(dir, 'post.md'), p.md);
		}
	}
	return base;
}

describe('readBlogTracks', () => {
	it('is empty when there is no blogs folder', () => {
		const base = mkdtempSync(join(tmpdir(), 'blogs-'));
		dirs.push(base);
		expect(readBlogTracks(base)).toEqual([]);
	});

	it('reads tracks and posts in folder order, slugs without the number', () => {
		const base = build([
			{
				folder: '00-engineering',
				posts: [
					{ folder: '01-virtual-gpu', md: 'one two three' },
					{ folder: '02-second', meta: post({ title: 'Second' }), md: 'x' }
				]
			}
		]);
		const [track] = readBlogTracks(base);
		expect(track.slug).toBe('engineering');
		expect(track.posts.map((p) => p.slug)).toEqual(['virtual-gpu', 'second']);
		expect(track.posts[0].readingMinutes).toBe(1);
		expect(readBlogPosts(base)).toHaveLength(2);
	});

	it('skips a track with no posts', () => {
		expect(readBlogTracks(build([{ folder: '00-empty', posts: [] }]))).toEqual([]);
	});

	it('names the file when the date is wrong', () => {
		const base = build([
			{
				folder: '00-a',
				posts: [{ folder: '01-p', meta: post({ date: 'yesterday' }), md: 'x' }]
			}
		]);
		expect(() => readBlogTracks(base)).toThrow(/meta\.json: "date"/);
	});

	it('refuses a post without post.md', () => {
		const base = build([{ folder: '00-a', posts: [{ folder: '01-p' }] }]);
		expect(() => readBlogTracks(base)).toThrow(/post\.md/);
	});

	it('refuses a slug used twice', () => {
		const base = build([
			{
				folder: '00-a',
				posts: [
					{ folder: '01-same', md: 'x' },
					{ folder: '02-other', meta: post({ slug: 'same' }), md: 'x' }
				]
			}
		]);
		expect(() => readBlogTracks(base)).toThrow(/used by both/);
	});
});

describe('renderPost', () => {
	it('renders Markdown and strips scripts', () => {
		const base = build([
			{
				folder: '00-a',
				posts: [{ folder: '01-p', md: '# Hi\n\nSome *words* <script>alert(1)</script>' }]
			}
		]);
		const html = renderPost('p', base)!;
		expect(html).toContain('<h1>Hi</h1>');
		expect(html).toContain('<em>words</em>');
		expect(html).not.toContain('<script');
	});

	it('is null for an unknown post', () => {
		expect(renderPost('nope', build([{ folder: '00-a', posts: [] }]))).toBeNull();
	});
});
