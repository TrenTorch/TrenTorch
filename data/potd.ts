// Problem of the Day entries. Each is a date paired with the id of a
// real, published IDE question (data/app_data/.../README.md's
// frontmatter `name`, see data/curriculum/generated-curriculum.json) --
// POTD doesn't need its own separate content pipeline, it just features
// one already-published question on a given day. Deliberately NOT
// data/questions.ts: a POTD pick shows up on the /potd page only, not
// folded into the main Questions page listing.
//
// To add a new day: append { date: 'YYYY-MM-DD', questionId: '...' }
// below. questionId must match a real question id in
// data/curriculum/generated-curriculum.json, or it's silently dropped
// (see processes/potd/get-potd-part.ts).
export interface PotdEntry {
	date: string;
	questionId: string;
}

export const potdEntries: PotdEntry[] = [
	{
		date: '2026-09-14',
		questionId: 'regularized-linear-models-ridge-regression-gaussian-elimination'
	},
	{
		date: '2026-09-15',
		questionId: 'ensembles-surge-gradient-boosted-trees'
	},
	{
		date: '2026-09-16',
		questionId: 'support-vector-machines-the-margin-deterministic-smo'
	},
	{
		date: '2026-09-17',
		questionId: 'variational-circuits-the-ansatz-parameter-shift-vqc'
	},
	{
		date: '2026-09-18',
		questionId: 'instance-based-probabilistic-spectral-drift-gp-calibration'
	},
	{
		date: '2026-09-19',
		questionId: 'txf-modern-linear-attention-netflix-fast-forward'
	},
	{
		date: '2026-09-20',
		questionId: 'instance-based-probabilistic-amazon-item-to-item-cf'
	}
];
