<table><tr><td><img src=".github/assets/trentorch-web-logo.jpg" width="50" height="50" alt="TrenTorch-Web logo" /></td><td><h1>TrenTorch-Web</h1></td></tr></table>

[![CI](https://github.com/TrenTorch/TrenTorch-Web/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/TrenTorch/TrenTorch-Web/actions/workflows/ci.yml)
[![Contributors](https://img.shields.io/badge/contributors-0-orange.svg)](#team-engineers)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Learn PyTorch and Frontier ML by building your own PyTorch, in the browser.

The web version of [TrenTorch](https://github.com/TrenTorch/TrenTorch): the same from-scratch, module-by-module curriculum, without a local install.

Built with [SvelteKit](https://svelte.dev/docs/kit).

## Development

```bash
npm install
npm run dev -- --open
```

## Checks before pushing

```bash
npm run check   # svelte-check (types)
npm run lint     # prettier + eslint
npm run test     # vitest
npm run build    # production build
```

CI runs all of the above on every push and pull request.

## Recreating the scaffold

```bash
npx sv@0.17.0 create --template minimal --types ts --add prettier eslint tailwindcss="plugins:typography" vitest="usages:unit" --install npm .
```

---

## Team Engineers

(Recomputed nightly from real issue/PR activity once there's some to count -- see `.github/workflows/update-contributors.yml`.)

---

## License

MIT License - see [LICENSE](LICENSE) for details.
