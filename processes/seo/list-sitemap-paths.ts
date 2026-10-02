import { buildPublicSeoManifest } from './build-public-seo-manifest';

export function listSitemapPaths(today?: string): string[] {
	return buildPublicSeoManifest(today)
		.filter((entry) => entry.indexable)
		.map((entry) => entry.path);
}
