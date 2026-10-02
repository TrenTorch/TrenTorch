import { withSiteName } from './with-site-name';
import { CLAIMS } from './claims';

export function buildFaqPageSeo() {
	return {
		title: withSiteName(
			`FAQ: ${CLAIMS.freePractice.shortText}, ${CLAIMS.pytorchStyleImplementations.shortText}`
		),
		description: `Answers about TrenTorch: ${CLAIMS.freePractice.text}, ${CLAIMS.fromScratch.text}, ${CLAIMS.pytorchStyleImplementations.text}, and ${CLAIMS.inferenceSystems.text}.`,
		path: '/faq'
	};
}
