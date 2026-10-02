import { buildBreadcrumbJsonLd } from './build-breadcrumb-json-ld';
import { buildSiteJsonLd } from './build-site-json-ld';
import { withSiteName } from './with-site-name';

export function buildComparisonIndexSeo() {
	return {
		title: withSiteName('Machine-learning practice alternatives'),
		description:
			'Review neutral, source-linked information about TrenTorch and other machine-learning practice platforms.',
		path: '/compare',
		indexable: true,
		prerendered: true,
		primaryIntent: 'machine-learning practice alternatives',
		source: 'platform/routes/compare/+page.svelte',
		jsonLd: [
			buildSiteJsonLd(),
			buildBreadcrumbJsonLd([
				{ name: 'Home', path: '/' },
				{ name: 'Alternatives', path: '/compare' }
			])
		]
	};
}
