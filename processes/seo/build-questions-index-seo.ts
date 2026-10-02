import { curriculum, getProgressStats } from '$data/questions';
import { buildBreadcrumbJsonLd } from './build-breadcrumb-json-ld';
import { CLAIMS } from './claims';
import { withSiteName } from './with-site-name';

export function buildQuestionsIndexSeo() {
	const stats = getProgressStats();

	return {
		title: withSiteName('Machine learning practice questions'),
		description: `Browse ${stats.total} questions across ${curriculum.length} sections. TrenTorch offers ${CLAIMS.freePractice.shortText} and ${CLAIMS.hiddenTestGrading.shortText}, from math foundations to transformers, inference, and production ML.`,
		path: '/questions',
		jsonLd: buildBreadcrumbJsonLd([
			{ name: 'Home', path: '/' },
			{ name: 'Questions', path: '/questions' }
		])
	};
}
