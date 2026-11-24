import { readBlogTracks } from '$processes/blogs/read-blogs';
import type { PageServerLoad } from './$types';

// Runs at build time (the page is prerendered). The posts are read from the folders under
// data/app_data/15-blogs, so adding one needs no code change.
export const load: PageServerLoad = () => ({ tracks: readBlogTracks() });
