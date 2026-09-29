import { potdEntries } from '$data/potd';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { absoluteUrl } from './absolute-url';
import { buildBreadcrumbJsonLd } from './build-breadcrumb-json-ld';
import { findQuestionLocation } from './find-question-location';
import { latestLiveDate } from './latest-live-date';
import { SITE_NAME, SITE_URL } from './site';
import { truncate } from './truncate';
import { withSiteName } from './with-site-name';

export interface QuestionSeo {
	title: string;
	description: string;
	path: string;
	// False for a slug that is in the curriculum list but has no authored
	// content yet: that page renders a "not published yet" state, which
	// would count as a thin, near-duplicate page if indexed.
	indexable: boolean;
	jsonLd: object[];
}

export function buildQuestionSeo(slug: string, today: string = latestLiveDate()): QuestionSeo {
	const path = `/ide/${slug}`;
	const authored = questionsById.get(slug);
	const location = findQuestionLocation(slug);

	if (!authored) {
		return {
			title: withSiteName('Question not published yet'),
			description: `This ${SITE_NAME} question is not published yet.`,
			path,
			indexable: false,
			jsonLd: []
		};
	}

	const partTitle = location?.part.title;
	const where = partTitle ? ` in the ${partTitle} section` : '';
	const description = truncate(
		`${authored.title}: a ${authored.difficulty.toLowerCase()} ${authored.track} practice problem${where}. Implement it in Python and run the tests in your browser, free.`,
		160
	);

	// A Problem of the Day scheduled for a future date stays out of search
	// results until a build on or after that date, so it is not surfaced
	// before its day.
	const scheduledForLater = potdEntries.some(
		(entry) => entry.questionId === slug && entry.date > today
	);

	const breadcrumbs = [
		{ name: 'Home', path: '/' },
		{ name: 'Questions', path: '/questions' },
		...(location ? [{ name: location.part.title, path: `/questions/${location.part.id}` }] : []),
		{ name: authored.title, path }
	];

	return {
		title: withSiteName(authored.title),
		description,
		path,
		indexable: !scheduledForLater,
		jsonLd: [
			{
				'@context': 'https://schema.org',
				'@type': 'LearningResource',
				name: authored.title,
				description,
				url: absoluteUrl(path),
				inLanguage: 'en',
				isAccessibleForFree: true,
				educationalLevel: authored.difficulty,
				learningResourceType: 'Practice problem',
				about: authored.tags,
				...(location && {
					isPartOf: {
						'@type': 'Course',
						name: location.part.title,
						url: absoluteUrl(`/questions/${location.part.id}`),
						provider: { '@type': 'Organization', name: SITE_NAME, url: SITE_URL }
					}
				})
			},
			buildBreadcrumbJsonLd(breadcrumbs)
		]
	};
}
