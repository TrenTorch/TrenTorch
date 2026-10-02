import { absoluteUrl } from './absolute-url';
import { escapeXml } from './escape-xml';
import { listSitemapPaths } from './list-sitemap-paths';

export function buildSitemapXml(today?: string): string {
	const urls = listSitemapPaths(today)
		.map((path) => `\t<url><loc>${escapeXml(absoluteUrl(path))}</loc></url>`)
		.join('\n');

	return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
}
