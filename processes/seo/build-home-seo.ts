import { buildSiteJsonLd } from './build-site-json-ld';
import { CLAIMS } from './claims';

export function buildHomeSeo() {
	return {
		title: `TrenTorch | ${CLAIMS.freePractice.shortText} & coding problems`,
		description: `${CLAIMS.freePractice.shortText}: ${CLAIMS.fromScratch.shortText}. Explore ${CLAIMS.curriculumCoverage.shortText}; ${CLAIMS.hiddenTestGrading.shortText}; ${CLAIMS.dailyRatedProblem.shortText}.`,
		path: '/',
		jsonLd: buildSiteJsonLd()
	};
}
