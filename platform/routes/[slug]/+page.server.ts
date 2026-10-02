import { error } from '@sveltejs/kit';
import { curriculum } from '$data/questions';
import { getSeoLandingPage, seoLandingPages } from '$data/seo-landing-pages';
import { buildLandingPageFaqs, buildLandingPageSeo } from '$processes/seo/build-landing-page-seo';
import { getLiveClaimText } from '$processes/seo/claims';
import type { EntryGenerator, PageServerLoad } from './$types';

export const prerender = true;

export const entries: EntryGenerator = () => seoLandingPages.map((page) => ({ slug: page.slug }));

export const load: PageServerLoad = ({ params }) => {
	const page = getSeoLandingPage(params.slug);
	if (!page) error(404, 'Page not found');

	const parts = curriculum.filter((part) => page.partIds.includes(part.id));
	if (parts.length !== page.partIds.length) {
		throw new Error(`SEO landing page "${page.slug}" references an unknown curriculum section`);
	}

	return {
		page,
		parts: parts.map((part) => ({
			...part,
			tracks: part.tracks.map((track) => ({
				...track,
				questions: track.questions.slice(0, 3)
			}))
		})),
		claims: getLiveClaimText(page.claimKeys),
		faqs: buildLandingPageFaqs(page),
		seo: buildLandingPageSeo(page)
	};
};
