// Pane sizes for the resizable IDE layout (left guide/code split, code/
// console split). Shared across every question -- a student who drags the
// panes to a comfortable size shouldn't have to redo it each time.
export const LAYOUT_KEY = 'trentorch_ide_layout';

export interface IdeLayout {
	leftPanePercent: number;
	bottomPanePercent: number;
}
