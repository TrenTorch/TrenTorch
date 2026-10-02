import { CLAIMS } from './claims';
import { withSiteName } from './with-site-name';

export function buildPotdSeo() {
	return {
		title: withSiteName('Problem of the Day'),
		description: `${CLAIMS.dailyRatedProblem.text}. Each published problem has a permanent page. ${CLAIMS.hiddenTestGrading.shortText}.`,
		path: '/potd'
	};
}
