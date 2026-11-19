# CUDA theory: notes and open questions

- **Svelte, not React.** The brief says React components; the site is SvelteKit, so each figure is `platform/components/cuda/viz/<id>/View.svelte`, a thin wrapper over the shared `Explorer` driven by a `VizConfig` in `processes/cuda/viz/`. Hand-drawn diagrams live in `platform/components/cuda/diagrams/`.
- **Extension figures** (OCCUPANCY-STAIRCASE, ROOFLINE-LADDER, BANK-STRIDE-SWEEP) are modes of their parent figure, as the addendum says.
- **Problem numbers.** The proposed CU-053/054/056/057 are "Coming soon" cards with no link; the problems already shipped in the bank as CU-053..061 were renumbered where they collided (mine are CU-058..061).
- **Measured data.** No Colab/T4 measurement exists yet, so the float4 figure shows "No measured data yet". Simulator timings are labelled as a model, never as hardware.
- **Illustrative numbers.** T4/H100 latencies, PCIe-tree cross-socket rate and the launch-overhead and scaling curves are labelled "illustrative numbers".
- **Diagrams replace ASCII.** The box-drawing tree in chapter A3 ("The tree") is now a figure; its heading is unchanged. The validator knows about this one exception.
- **G1 intro.** The agent-facing paragraph was replaced by one learner-facing sentence.
- **Pre-existing:** `e2e/build-output.spec.ts` client-JS budget already fails on the base branch (unrelated).
- **Not yet done:** measured-vs-simulator data for float4; per-chapter "read" progress.
