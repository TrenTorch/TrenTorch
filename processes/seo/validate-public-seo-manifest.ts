import { absoluteUrl } from './absolute-url';
import type { SeoRouteManifestEntry } from './build-public-seo-manifest';

export function validatePublicSeoManifest(
	entries: SeoRouteManifestEntry[],
	sitemapPaths: string[]
): string[] {
	const errors: string[] = [];
	const sitemap = new Set(sitemapPaths);
	const seenPaths = new Set<string>();
	const seenCanonicals = new Set<string>();
	const seenTitles = new Set<string>();
	const seenDescriptions = new Set<string>();

	for (const entry of entries) {
		if (seenPaths.has(entry.path)) errors.push(`Duplicate route path: ${entry.path}`);
		seenPaths.add(entry.path);

		if (!entry.title.trim()) errors.push(`Missing title: ${entry.path}`);
		if (!entry.description.trim()) errors.push(`Missing description: ${entry.path}`);
		if (!entry.primaryIntent.trim()) errors.push(`Missing primary intent: ${entry.path}`);
		if (!entry.source.trim()) errors.push(`Missing SEO copy source: ${entry.path}`);
		if (entry.indexable && !entry.prerendered)
			errors.push(`Indexable page is not prerendered: ${entry.path}`);

		try {
			const canonicalUrl = new URL(entry.canonical);
			if (canonicalUrl.protocol !== 'https:' || entry.canonical !== absoluteUrl(entry.path))
				errors.push(`Malformed or noncanonical URL: ${entry.path}`);
		} catch {
			errors.push(`Malformed canonical URL: ${entry.path}`);
		}

		if (seenCanonicals.has(entry.canonical))
			errors.push(`Duplicate canonical URL: ${entry.canonical}`);
		seenCanonicals.add(entry.canonical);

		if (entry.indexable) {
			if (!sitemap.has(entry.path))
				errors.push(`Indexable route missing from sitemap: ${entry.path}`);
			if (seenTitles.has(entry.title)) errors.push(`Duplicate title: ${entry.title}`);
			if (seenDescriptions.has(entry.description))
				errors.push(`Duplicate description: ${entry.path}`);
			seenTitles.add(entry.title);
			seenDescriptions.add(entry.description);
		}
	}

	for (const path of sitemap) {
		if (!seenPaths.has(path)) errors.push(`Sitemap route has no manifest entry: ${path}`);
	}

	return errors;
}
