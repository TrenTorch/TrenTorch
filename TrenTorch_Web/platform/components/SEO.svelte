<script lang="ts">
	import { absoluteUrl } from '$processes/seo/absolute-url';
	import { OG_IMAGE_HEIGHT, OG_IMAGE_PATH, OG_IMAGE_WIDTH, SITE_NAME } from '$processes/seo/site';
	import { toJsonLdScript } from '$processes/seo/to-json-ld-script';

	interface Props {
		// The complete <title>. Callers add the site name via withSiteName().
		title: string;
		description: string;
		path: string;
		type?: 'website' | 'article';
		noindex?: boolean;
		jsonLd?: object | object[];
	}

	let { title, description, path, type = 'website', noindex = false, jsonLd }: Props = $props();

	const canonical = $derived(absoluteUrl(path));
	const image = absoluteUrl(OG_IMAGE_PATH);
	const scripts = $derived([jsonLd ?? []].flat().map(toJsonLdScript));
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={description} />
	<link rel="canonical" href={canonical} />
	{#if noindex}
		<meta name="robots" content="noindex, follow" />
	{/if}

	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:type" content={type} />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={description} />
	<meta property="og:url" content={canonical} />
	<meta property="og:image" content={image} />
	<meta property="og:image:width" content={String(OG_IMAGE_WIDTH)} />
	<meta property="og:image:height" content={String(OG_IMAGE_HEIGHT)} />
	<meta property="og:image:alt" content="TrenTorch: build PyTorch by hand, in your browser" />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={title} />
	<meta name="twitter:description" content={description} />
	<meta name="twitter:image" content={image} />

	{#each scripts as script (script)}
		<!-- Safe: the payload is our own JSON, and toJsonLdScript escapes every `<`
		     so nothing in it can close the script element. -->
		<!-- eslint-disable-next-line svelte/no-at-html-tags -->
		{@html script}
	{/each}
</svelte:head>
