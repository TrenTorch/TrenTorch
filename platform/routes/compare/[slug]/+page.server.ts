import { error } from '@sveltejs/kit';
import { curriculum } from '$data/questions';
import { competitors, getCompetitor } from '$data/competitors';
import { seoLandingPages } from '$data/seo-landing-pages';
import { buildComparisonFaqs, buildComparisonSeo } from '$processes/seo/build-comparison-seo';
import type { EntryGenerator, PageServerLoad } from './$types';

export const prerender = true;

export const entries: EntryGenerator = () =>
	competitors.map((competitor) => ({ slug: competitor.slug }));

export const load: PageServerLoad = ({ params }) => {
	const competitor = getCompetitor(params.slug);
	if (!competitor) error(404, 'Comparison not found');

	return {
		competitor,
		parts: curriculum.filter((part) =>
			['part-classical-linear', 'part-dl-core', 'part-transformers-llm', 'part-inference'].includes(
				part.id
			)
		),
		otherComparisons: competitors.filter((item) => item.slug !== competitor.slug),
		landingPages: seoLandingPages,
		faqs: buildComparisonFaqs(competitor),
		seo: buildComparisonSeo(competitor)
	};
};
