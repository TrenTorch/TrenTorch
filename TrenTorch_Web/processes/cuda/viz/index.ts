// Registry of every theory figure, keyed by the lower-case viz id without the VIZ- prefix.
import type { VizConfig } from './types';
import { partAB } from './part-ab';
import { partCD } from './part-cd';
import { partE } from './part-e';
import { partFG } from './part-fg';

export * from './types';
export const ALL_VIZ: VizConfig[] = [...partAB, ...partCD, ...partE, ...partFG];
export const VIZ_BY_ID: Record<string, VizConfig> = Object.fromEntries(
	ALL_VIZ.map((c) => [c.id, c])
);
