export type PaperKind = 'foundational' | 'breakthrough';

export interface PaperImplementation {
	slug: string;
	title: string;
	difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
}

export interface Paper {
	slug: string;
	title: string;
	authors: string;
	year: number;
	kind: PaperKind;
	summary: string;
	arxivId: string;
	implementations: PaperImplementation[];
}

export interface PaperTopic {
	slug: string;
	title: string;
	description: string;
	papers: Paper[];
}
