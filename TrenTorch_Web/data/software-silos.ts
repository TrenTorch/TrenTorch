// The Software Engineering domain is broader than data structures and algorithms (scripting, automation,
// version control, production-grade practice are to come), so the DSA sheet is shelved here as four silos
// rather than one flat list. A silo groups the sheet's steps by id; new silos sit beside these.
export type SoftwareSilo = {
	id: string;
	title: string;
	/** Ids of the DSA sheet steps it holds, in reading order. */
	steps: string[];
};

export const softwareSilos: SoftwareSilo[] = [
	{
		id: 'foundations',
		title: 'Foundations',
		steps: ['basics', 'maths', 'bit-manipulation', 'recursion-and-backtracking']
	},
	{
		id: 'data-structures',
		title: 'Data Structures',
		steps: [
			'arrays',
			'linked-list',
			'stack-and-queue',
			'hashing',
			'heaps',
			'binary-trees',
			'binary-search-trees',
			'tries'
		]
	},
	{
		id: 'algorithms',
		title: 'Algorithms',
		steps: [
			'sorting',
			'binary-search',
			'sliding-window-and-two-pointers',
			'greedy',
			'graphs',
			'dynamic-programming'
		]
	},
	{
		id: 'strings-and-design',
		title: 'Strings and Design',
		steps: ['strings', 'advanced-strings', 'design']
	}
];
