import type { QuestionSeo } from '$processes/seo/build-question-seo';
import { absoluteUrl } from '$processes/seo/absolute-url';
import { SITE_NAME } from '$processes/seo/site';
import { withSiteName } from '$processes/seo/with-site-name';
import { findCudaProblem } from './read-problems';

// SEO for /ide/cuda-<slug>: same shape as the curriculum questions' (processes/seo/build-question-seo.ts).
export function buildCudaSeo(ideId: string): QuestionSeo | null {
	const p = findCudaProblem(ideId);
	if (!p) return null;
	const path = `/ide/${ideId}`;
	return {
		title: withSiteName(`${p.title}: CUDA kernel problem`),
		description:
			`${p.title} (${p.id}): a ${p.difficulty.toLowerCase()} CUDA kernel exercise on ${SITE_NAME}. ${p.lesson} Write the kernel and run it in your browser, free.`.slice(
				0,
				160
			),
		path,
		indexable: true,
		jsonLd: [
			{
				'@context': 'https://schema.org',
				'@type': 'LearningResource',
				name: p.title,
				url: absoluteUrl(path),
				educationalLevel: p.difficulty,
				teaches: p.lesson,
				isAccessibleForFree: true
			}
		]
	};
}
