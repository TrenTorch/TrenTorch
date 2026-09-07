<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./priv/static/phoenix-orange.png" />
  <source media="(prefers-color-scheme: light)" srcset="./priv/static/phoenix.png" />
  <img src="./priv/static/phoenix.png" alt="Phoenix logo" />
</picture>

> Peace of mind from prototype to production.

[![Build Status](https://github.com/supabase/phoenix/workflows/CI/badge.svg)](https://github.com/supabase/phoenix/actions/workflows/ci.yml) [![npm version](https://img.shields.io/npm/v/@supabase/phoenix.svg)](https://www.npmjs.com/package/@supabase/phoenix)

## Supabase Fork

This is a Supabase fork of Phoenix Framework, published to npm as `@supabase/phoenix`.

**Installation:**
```bash
npm install @supabase/phoenix
```

**Releases**: This fork uses automated releases via [release-please](https://github.com/googleapis/release-please). See [RELEASE.md](RELEASE.md) for details.

**Upstream**: Based on [phoenixframework/phoenix](https://github.com/phoenixframework/phoenix)

## Versioning

This package uses **independent semantic versioning** for the JavaScript client.

- **Based on**: Phoenix Framework 1.8.3 JS client
- **Last synced**: 2026-07-09

We version based on **JS API changes only**, not upstream Phoenix framework releases.
When we merge upstream Phoenix changes, we evaluate the JS API impact and version accordingly.

## Getting started

See the official site at <https://www.phoenixframework.org/>.

Install the latest version of Phoenix by following the instructions at <https://phoenix.hexdocs.pm/installation.html#phoenix>.

## Documentation

API documentation is available at <https://phoenix.hexdocs.pm>.

Phoenix.js documentation is available at <https://phoenix.hexdocs.pm/js>.

## Contributing

We appreciate any contribution to Phoenix. Check our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [CONTRIBUTING.md](CONTRIBUTING.md) guides for more information. We usually keep a list of features and bugs in the [issue tracker][4].

### Generating a Phoenix project from unreleased versions

You can create a new project using the latest Phoenix source installer (the `phx.new` Mix task) with the following steps:

1. Remove any previously installed `phx_new` archives so that Mix will pick up the local source code. This can be done with `mix archive.uninstall phx_new` or by simply deleting the file, which is usually in `~/.mix/archives/`.
2. Copy this repo via `git clone https://github.com/phoenixframework/phoenix` or by downloading it
3. Run the `phx.new` Mix task from within the `installer` directory, for example:

```bash
cd phoenix/installer
mix phx.new dev_app --dev
```

The `--dev` flag will configure your new project's `:phoenix` dep as a relative path dependency, pointing to your local Phoenix checkout:

```elixir
defp deps do
  [{:phoenix, path: "../..", override: true},
```

To create projects outside of the `installer/` directory, add the latest archive to your machine by following the instructions in [installer/README.md](https://github.com/phoenixframework/phoenix/blob/main/installer/README.md)

### Building from source

To build the documentation:

```bash
MIX_ENV=docs mix docs
```

To build Phoenix:

```bash
mix deps.get
mix compile
```

To build the Phoenix installer:

```bash
mix deps.get
mix compile
mix archive.build
```

To build Phoenix.js:

```bash
mix assets.build
```

## Important links

* [#elixir][1] on [Libera][2] IRC
* [elixir-lang Slack channel][3]
* [Issues tracker][4]
* [Phoenix Forum (questions and proposals)][5]
* Visit Phoenix's sponsor, DockYard, for expert [Phoenix Consulting](https://dockyard.com/phoenix-consulting)

  [1]: https://web.libera.chat/?channels=#elixir
  [2]: https://libera.chat/
  [3]: https://elixir-lang.slack.com/
  [4]: https://github.com/phoenixframework/phoenix/issues
  [5]: https://elixirforum.com/c/phoenix-forum

## Copyright and License

Copyright (c) 2014, Chris McCord.

Phoenix source code is licensed under the [MIT License](LICENSE.md).
