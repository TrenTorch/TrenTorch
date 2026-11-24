import { error } from '@sveltejs/kit';
import { readBlogPosts, renderPost } from '$processes/blogs/read-blogs';
import type { EntryGenerator, PageServerLoad } from './$types';

export const prerender = true;

// One prerendered page per post folder; a new post gets its page automatically.
export const entries: EntryGenerator = () => readBlogPosts().map((post) => ({ slug: post.slug }));

export const load: PageServerLoad = ({ params }) => {
	const post = readBlogPosts().find((p) => p.slug === params.slug);
	const html = renderPost(params.slug);
	if (!post || html === null) error(404, 'Post not found');
	return { post, html };
};
