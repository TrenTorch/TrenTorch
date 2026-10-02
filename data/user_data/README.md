# User Data: Storage Contract

Documentation only. There are no real files in this folder. It records what the app persists per visitor, so the shape of that data is versioned next to the curriculum it describes.

Two layers hold user data:

1. **Browser storage** (this file's keys). Always available, works signed out, and is the copy the current tab reads.
2. **Supabase**, only when signed in. A cross device copy that is synced in the background. Sync never blocks the UI and never rolls local state back. See `docs/internal/02-flows.md` for the sync flows and `docs/internal/06-database.md` for the tables.

Every browser storage read and write is wrapped in try/catch. Private browsing, blocked storage and a first visit all look the same: no saved state, not an error.

## localStorage keys

| Key                               | Owner                                                                | Shape and meaning                                                                                                              |
| --------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `trentorch-solved-questions`      | `processes/progress-tracking/solved.svelte.ts`                       | JSON array of question ids that passed the full suite through Submit. Mirrored to `solved_questions`.                          |
| `trentorch-attempted-questions`   | `processes/progress-tracking/attempted.svelte.ts`                    | JSON array of ids where Submit ran, pass or fail. Mirrored to `attempted_questions`. Re-attempt removes an id from both lists. |
| `trentorch-collapsed-parts`       | `processes/progress-tracking/collapsed-sections.svelte.ts`           | JSON array of Part ids the visitor collapsed on the questions page. UI only.                                                   |
| `trentorch_code_<questionId>`     | `processes/code-execution/save-user-code.ts` (`CODE_KEY_PREFIX`)     | Editor contents as a plain string. Reset removes it, falling back to the starter code. Mirrored to `code_drafts`.              |
| `trentorch_codemeta_<questionId>` | `processes/code-execution/draft-sync.svelte.ts` (`CODE_META_PREFIX`) | Timestamp of the last local edit. Used so the newest edit wins when syncing drafts across devices.                             |
| `trentorch_ide_layout`            | `processes/code-execution/save-ide-layout.ts` (`LAYOUT_KEY`)         | JSON `{ leftPanePercent, bottomPanePercent }`, shared by every question.                                                       |
| `theme`                           | `platform/components/ModeToggle.svelte`                              | `"dark"` or `"light"`. Read before hydration by the script in `platform/app.html`.                                             |

## sessionStorage keys

| Key                       | Owner                                         | Meaning                                                                                                             |
| ------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `trentorch-after-sign-in` | `processes/auth/after-sign-in-destination.ts` | Same-site path to open once a gated visitor finishes signing in. Cleared when used or when the dialog is dismissed. |

## Cleanup

`processes/auth/delete-account.ts` removes every `trentorch*` localStorage key when an account is deleted.

## Adding a new persisted field

Add the key here first (name, shape, owning module, what empty means), then implement it. Use the `trentorch_` prefix so account deletion clears it.
