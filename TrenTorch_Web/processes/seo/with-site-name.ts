import { SITE_NAME } from './site';

export function withSiteName(pageTitle: string): string {
	return `${pageTitle} | ${SITE_NAME}`;
}
