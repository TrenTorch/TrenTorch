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
	},
	{
		date: '2026-09-21',
		questionId: 'vision-pool-metaconstellation-downsampling'
	},
	{
		date: '2026-09-22',
		questionId: 'vision-pool-uber-surge-demand-smoothing'
	},
	{
		date: '2026-09-23',
		questionId: 'potd-shelf-sentinel-relu'
	},
	{
		date: '2026-09-24',
		questionId: 'potd-torque-minimizer-gd-step'
	},
	{
		date: '2026-09-25',
		questionId: 'potd-zomato-speed-run-ols-pinv'
	},
	{
		date: '2026-09-26',
		questionId: 'potd-skip-predictor-precision-recall'
	},
	{
		date: '2026-09-27',
		questionId: 'potd-first-fraud-score-bce'
	},
	{
		date: '2026-09-28',
		questionId: 'potd-thumbnail-normalize'
	},
	{
		date: '2026-09-29',
		questionId: 'potd-amenity-encoder-one-hot'
	},
	{
		date: '2026-09-30',
		questionId: 'potd-eta-scorecard-mae'
	},
	{
		date: '2026-10-01',
		questionId: 'potd-caption-splitter-tokenizer'
	},
	{
		date: '2026-10-02',
		questionId: 'potd-sensor-fusion-linear-layer'
	},
	{
		date: '2026-10-03',
		questionId: 'potd-utilization-nudge-sgd-step'
	},
	{
		date: '2026-10-04',
		questionId: 'potd-click-rate-band-wald-ci'
	},
	{
		date: '2026-10-05',
		questionId: 'potd-engagement-slope-linreg'
	},
	{
		date: '2026-10-06',
		questionId: 'potd-raw-embedding-lookup'
	},
	{
		date: '2026-10-07',
		questionId: 'potd-fraud-label-surprise-entropy'
	},
	{
		date: '2026-10-08',
		questionId: 'potd-profile-similarity-cosine'
	},
	{
		date: '2026-10-09',
		questionId: 'potd-pin-image-downsample-maxpool'
	},
	{
		date: '2026-10-10',
		questionId: 'potd-run-logger-json'
	},
	{
		date: '2026-10-11',
		questionId: 'potd-cart-category-encoder'
	},
	{
		date: '2026-10-12',
		questionId: 'potd-cancellation-sanity-check-accuracy'
	},
	{
		date: '2026-10-13',
		questionId: 'potd-brightness-dial-sigmoid'
	},
	{
		date: '2026-10-14',
		questionId: 'potd-lead-score-error-mse'
	},
	{
		date: '2026-10-15',
		questionId: 'potd-telemetry-gap-check'
	},
	{
		date: '2026-10-16',
		questionId: 'potd-top-hashtags'
	},
	{
		date: '2026-10-17',
		questionId: 'potd-rollout-check-two-proportion-z'
	},
	{
		date: '2026-10-18',
		questionId: 'potd-stockout-threshold-sweep-f1'
	},
	{
		date: '2026-10-19',
		questionId: 'potd-review-model-dropout'
	},
	{
		date: '2026-10-20',
		questionId: 'potd-menu-photo-padding-1d-conv'
	},
	{
		date: '2026-10-21',
		questionId: 'potd-collaborative-score-matrix'
	},
	{
		date: '2026-10-22',
		questionId: 'potd-gradient-seatbelt-clipping'
	}
];
