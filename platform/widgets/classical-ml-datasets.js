import { seededRandom } from '../components/visualizers/seededRandom.js';

const DEFAULT_SEED = 731;

/**
 * @param {number} n
 * @param {number} slope
 * @param {number} intercept
 * @param {number} noise
 * @param {number} [seed]
 */
export function linearNoisy(n, slope = 1.25, intercept = 0.4, noise = 0.75, seed = DEFAULT_SEED) {
	const random = seededRandom(seed);
	return Array.from({ length: n }, (_, index) => {
		const x = -3 + (6 * index) / Math.max(1, n - 1);
		return { x, y: slope * x + intercept + (random() * 2 - 1) * noise };
	});
}

/** @param {number} n @param {number} [seed] */
export function linearWithOutliers(n = 32, seed = DEFAULT_SEED) {
	const points = linearNoisy(n, 1.1, 0.25, 0.5, seed);
	for (const index of [Math.floor(n * 0.28), Math.floor(n * 0.74)]) {
		if (points[index]) points[index].y += index % 2 ? 4.2 : -4.2;
	}
	return points;
}

/** @param {number} separation @param {number} spread @param {number} [seed] */
export function twoBlobs(separation = 2.1, spread = 0.7, seed = DEFAULT_SEED) {
	const random = seededRandom(seed);
	return Array.from({ length: 48 }, (_, index) => {
		const label = index % 2;
		const center = label ? separation / 2 : -separation / 2;
		return {
			x: center + (random() + random() + random() - 1.5) * spread,
			y: (random() + random() + random() - 1.5) * spread + (label ? 0.18 : -0.18),
			label
		};
	});
}

/** @param {number} n @param {number} [noise] @param {number} [seed] */
export function polynomialNoisy(n = 40, noise = 0.35, seed = DEFAULT_SEED) {
	const random = seededRandom(seed);
	return Array.from({ length: n }, (_, index) => {
		const x = -2.5 + (5 * index) / Math.max(1, n - 1);
		return { x, y: 0.7 * x * x - 0.8 * x + (random() * 2 - 1) * noise };
	});
}

/** @param {number} [seed] */
export function tabularWithMissing(seed = DEFAULT_SEED) {
	const random = seededRandom(seed);
	return Array.from({ length: 8 }, (_, row) => [
		(row + 1) * 4 + Math.round(random() * 3),
		Math.round(20 + random() * 35),
		Math.round(1 + random() * 8),
		row % 3 === 0 ? 'north' : row % 3 === 1 ? 'south' : 'west'
	]);
}

/** @param {number} ratio @param {number} [spread] @param {number} [seed] */
export function imbalancedBlobs(ratio = 0.2, spread = 0.7, seed = DEFAULT_SEED) {
	const random = seededRandom(seed);
	const majority = 40;
	const minority = Math.max(1, Math.round(majority * ratio));
	return Array.from({ length: majority + minority }, (_, index) => {
		const label = index < majority ? 0 : 1;
		const center = label ? 1.6 : -1.1;
		return {
			x: center + (random() + random() + random() - 1.5) * spread,
			y: (random() + random() + random() - 1.5) * spread,
			label
		};
	});
}

/** @param {number} n @param {number} [seed] */
export function twoMoons(n = 48, seed = DEFAULT_SEED) {
	const random = seededRandom(seed);
	return Array.from({ length: n }, (_, index) => {
		const label = index % 2;
		const angle = (Math.PI * (index >> 1)) / Math.ceil(n / 2);
		const noise = () => (random() - 0.5) * 0.16;
		return label
			? { x: 0.5 + Math.cos(angle) + noise(), y: 0.25 - Math.sin(angle) + noise(), label }
			: { x: Math.cos(angle), y: Math.sin(angle) + noise(), label };
	});
}
