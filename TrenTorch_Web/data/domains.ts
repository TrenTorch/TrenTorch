import type { Pathname } from '$app/types';
import { curriculum } from './questions';

// The domains /modules is organised by. A domain without an href is planned
// and shows as "soon" on the hub.
export type DomainId = 'aisys' | 'gpu' | 'software' | 'system-design' | 'robotics';

export interface Domain {
	id: DomainId;
	title: string;
	blurb: string;
	href?: Pathname;
}

export const domains: Domain[] = [
	{
		id: 'aisys',
		title: 'AI Systems',
		blurb: 'Python to production ML, one subsystem at a time',
		href: '/questions'
	},
	{
		id: 'gpu',
		title: 'GPU Programming',
		blurb: 'Understand the GPU from ground-up, and write the kernels that run on it',
		href: '/cuda'
	},
	{
		id: 'software',
		title: 'Software Engineering',
		blurb: 'From data structures and algorithms, towards the craft of shipping real software',
		href: '/dsa'
	},
	{
		id: 'system-design',
		title: 'System Design & Architecture',
		blurb: 'Productionizing engineering systems across domains'
	},
	{
		id: 'robotics',
		title: 'Robotics',
		blurb: 'From dynamics and control to vision-language-action models'
	}
];

// Research papers are listed on /papers, not as an AI Systems module.
const NOT_AI_SYSTEMS = new Set(['part-research-papers']);

export const aiSystemsParts = curriculum.filter((part) => !NOT_AI_SYSTEMS.has(part.id));
