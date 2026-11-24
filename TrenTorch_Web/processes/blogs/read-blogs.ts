// Blogs are read straight from the folders under data/app_data/15-blogs, the same way the research papers
// are, so adding a post means adding a folder, never editing code. One level per folder:
//
//   15-blogs/
//     <NN>-<track>/             meta.json: { "title", "description" }
//       <NN>-<post>/            meta.json: { "title", "post": { title, author, date, summary } } and post.md
//
// The numeric prefixes only set the order of tracks and, inside a track, of posts (newest first is a
// matter of numbering them that way). Everything is validated here, at build time, with an error that
// names the file to fix. See the README in the blogs folder.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import DOMPurify from 'isomorphic-dompurify';
import { Marked } from 'marked';
import { markdownMath } from '../markdown/markdown-math';
import type { BlogPost, BlogTrack } from './types';

export const BLOGS_DIR = join('data', 'app_data', '15-blogs');

const SLUG = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const WORDS_PER_MINUTE = 220;

const stripPrefix = (name: string) => name.replace(/^\d+-/, '');

function contentDirs(dir: string): string[] {
	return readdirSync(dir)
		.filter((name) => !name.startsWith('_') && !name.startsWith('.'))
		.filter((name) => statSync(join(dir, name)).isDirectory())
		.sort();
}

function readJson(path: string): Record<string, unknown> {
	if (!existsSync(path)) throw new Error(`Missing ${path}`);
	try {
		const value: unknown = JSON.parse(readFileSync(path, 'utf8'));
		if (typeof value !== 'object' || value === null || Array.isArray(value)) {
			throw new Error('expected a JSON object');
		}
		return value as Record<string, unknown>;
	} catch (err) {
		throw new Error(`Invalid ${path}: ${(err as Error).message}`, { cause: err });
	}
}

function text(value: unknown, field: string, path: string): string {
	if (typeof value !== 'string' || value.trim() === '') {
		throw new Error(`${path}: "${field}" must be a non-empty string`);
	}
	return value.trim();
}

function readPost(postDir: string, folderName: string): BlogPost {
	const metaPath = join(postDir, 'meta.json');
	const raw = readJson(metaPath).post;
	if (typeof raw !== 'object' || raw === null || Array.isArray(raw)) {
		throw new Error(`${metaPath} needs a "post" object (title, author, date, summary)`);
	}
	const post = raw as Record<string, unknown>;
	const slug =
		post.slug === undefined ? stripPrefix(folderName) : text(post.slug, 'slug', metaPath);
	if (!SLUG.test(slug))
		throw new Error(`${metaPath}: slug "${slug}" must be lower-case words joined by "-"`);
	const date = text(post.date, 'date', metaPath);
	if (!DATE.test(date) || Number.isNaN(Date.parse(date))) {
		throw new Error(`${metaPath}: "date" must look like 2026-11-24`);
	}
	const bodyPath = join(postDir, 'post.md');
	if (!existsSync(bodyPath)) throw new Error(`Missing ${bodyPath}`);
	const words = readFileSync(bodyPath, 'utf8').split(/\s+/).filter(Boolean).length;
	return {
		slug,
		title: text(post.title, 'title', metaPath),
		author: text(post.author, 'author', metaPath),
		date,
		summary: text(post.summary, 'summary', metaPath),
		readingMinutes: Math.max(1, Math.round(words / WORDS_PER_MINUTE))
	};
}

/** The tracks, each with its posts. A site with no posts yet has no tracks (and no blogs folder is fine). */
export function readBlogTracks(baseDir: string = process.cwd()): BlogTrack[] {
	const root = join(baseDir, BLOGS_DIR);
	if (!existsSync(root)) return [];
	const tracks: BlogTrack[] = [];
	const slugs = new Map<string, string>();

	for (const trackName of contentDirs(root)) {
		const trackDir = join(root, trackName);
		const metaPath = join(trackDir, 'meta.json');
		const meta = readJson(metaPath);
		const posts: BlogPost[] = [];
		for (const postName of contentDirs(trackDir)) {
			const postDir = join(trackDir, postName);
			const post = readPost(postDir, postName);
			const earlier = slugs.get(post.slug);
			if (earlier)
				throw new Error(`Post slug "${post.slug}" is used by both ${earlier} and ${postDir}`);
			slugs.set(post.slug, postDir);
			posts.push(post);
		}
		if (posts.length === 0) continue; // an empty track folder is a placeholder
		tracks.push({
			slug: stripPrefix(trackName),
			title: text(meta.title, 'title', metaPath),
			description: text(meta.description, 'description', metaPath),
			posts
		});
	}
	return tracks;
}

export function readBlogPosts(baseDir?: string): BlogPost[] {
	return readBlogTracks(baseDir).flatMap((track) => track.posts);
}

/** A post's body as sanitised HTML (Markdown plus $math$), rendered at build time. */
export function renderPost(slug: string, baseDir: string = process.cwd()): string | null {
	const root = join(baseDir, BLOGS_DIR);
	if (!existsSync(root)) return null;
	for (const trackName of contentDirs(root)) {
		for (const postName of contentDirs(join(root, trackName))) {
			if (stripPrefix(postName) !== slug) continue;
			const marked = new Marked();
			marked.use(markdownMath({ throwOnError: false }));
			const dirty = marked.parse(
				readFileSync(join(root, trackName, postName, 'post.md'), 'utf8')
			) as string;
			return DOMPurify.sanitize(dirty);
		}
	}
	return null;
}
