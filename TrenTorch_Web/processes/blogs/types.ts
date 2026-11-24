export interface BlogPost {
	slug: string;
	title: string;
	author: string;
	/** ISO date, YYYY-MM-DD. */
	date: string;
	summary: string;
	readingMinutes: number;
}

export interface BlogTrack {
	slug: string;
	title: string;
	description: string;
	posts: BlogPost[];
}
