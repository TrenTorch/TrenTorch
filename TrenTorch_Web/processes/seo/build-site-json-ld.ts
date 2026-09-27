import { absoluteUrl } from './absolute-url';
import { GITHUB_URL, LOGO_PATH, SITE_NAME, SITE_URL } from './site';

export function buildSiteJsonLd() {
	return [
		{
			'@context': 'https://schema.org',
			'@type': 'Organization',
			name: SITE_NAME,
			url: SITE_URL,
			logo: absoluteUrl(LOGO_PATH),
			sameAs: [GITHUB_URL]
		},
		{
			'@context': 'https://schema.org',
			'@type': 'WebSite',
			name: SITE_NAME,
			url: absoluteUrl('/'),
			inLanguage: 'en'
		}
	];
}
