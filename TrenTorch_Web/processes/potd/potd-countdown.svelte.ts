import { SvelteDate } from 'svelte/reactivity';
import { localDateString } from './local-date-string';

/**
 * The clock the Problem of the Day shows: time left until the visitor's next midnight (hh:mm:ss) and the day it was last
 * drawn for. Call `start()` from onMount; it ticks every second and returns the function that stops it.
 * `onDayChange` hears about the first day and every rollover after it.
 */
export function createPotdCountdown(onDayChange?: (day: string) => void) {
	let time = $state('');
	let day = $state('');

	function tick() {
		const now = new SvelteDate();
		const current = localDateString(now);
		if (current !== day) {
			day = current;
			onDayChange?.(current);
		}

		const nextMidnight = new SvelteDate(now);
		nextMidnight.setHours(24, 0, 0, 0);
		const seconds = Math.max(0, Math.floor((nextMidnight.getTime() - now.getTime()) / 1000));
		const hours = String(Math.floor(seconds / 3600)).padStart(2, '0');
		const minutes = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
		time = `${hours}:${minutes}:${String(seconds % 60).padStart(2, '0')}`;
	}

	return {
		get time() {
			return time;
		},
		get day() {
			return day;
		},
		start() {
			tick();
			const timer = window.setInterval(tick, 1000);
			return () => window.clearInterval(timer);
		}
	};
}
