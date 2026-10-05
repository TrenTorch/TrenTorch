import { SETUP_SCRIPT } from './pyodide-setup-script';

// The Python the worker runs for a 'preview' request, and the Node Pyodide check
// (pyodide-check/questions.spec.ts) runs for every question that has a preview,
// so the two cannot drift apart.
//
// A question may ship an optional preview.py. It runs *after* the student's code,
// in the same namespace, with a `show()` helper available, so it can call the
// student's function on example data and put the result in the Console:
//
//   fig, ax = line_chart([1, 2, 3], [4, 5, 6], "Revenue", "Month", "EUR")
//   show(fig)
//
// show() understands matplotlib figures and axes (and arrays of axes), seaborn
// grids, and plotly figures; anything else is printed. Matplotlib figures become
// PNG images (the worker has no screen, so the Agg backend draws them); plotly
// figures are sent as JSON and drawn interactively in the page. Any pyplot figure
// still open at the end is shown too, so a preview does not have to call show().
export const PREVIEW_HELPERS = `
import base64 as _tt_base64

def _tt_figure_of(obj):
    """The matplotlib Figure behind obj, or None."""
    try:
        import matplotlib.axes as _axes
        import matplotlib.figure as _figure
    except ImportError:
        return None
    if isinstance(obj, _figure.Figure):
        return obj
    if isinstance(obj, _axes.Axes):
        return obj.figure
    if isinstance(getattr(obj, "ndim", None), int) and getattr(obj, "size", 0):
        first = obj.flat[0]
        if isinstance(first, _axes.Axes):
            return first.figure
    for attribute in ("figure", "fig"):  # seaborn FacetGrid / PairGrid / JointGrid
        inner = getattr(obj, attribute, None)
        if isinstance(inner, _figure.Figure):
            return inner
    return None

def _tt_png(figure):
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=110, bbox_inches="tight")
    return {"kind": "png", "data": _tt_base64.b64encode(buffer.getvalue()).decode("ascii")}

def _tt_make_show(figures, seen):
    def show(*objects):
        """Show charts in the Console; print anything else."""
        for obj in objects:
            if obj is None:
                print("(nothing to show: the value is None)")
            elif type(obj).__module__.startswith("plotly") and hasattr(obj, "to_json"):
                figures.append({"kind": "plotly", "json": obj.to_json()})
            elif isinstance(obj, (tuple, list)):
                show(*[item for item in obj if _tt_figure_of(item) is not None or hasattr(item, "to_json")])
            else:
                figure = _tt_figure_of(obj)
                if figure is None:
                    print(obj)
                elif id(figure) not in seen:
                    seen.add(id(figure))
                    figures.append(_tt_png(figure))
    return show

def _tt_remaining_pyplot_figures(figures, seen):
    try:
        import matplotlib.pyplot as _plt
    except ImportError:
        return
    for number in _plt.get_fignums():
        figure = _plt.figure(number)
        if id(figure) not in seen:
            seen.add(id(figure))
            figures.append(_tt_png(figure))
    _plt.close("all")
`;

export function buildPreviewScript(options: { codeB64: string; previewB64: string }): string {
	const { codeB64, previewB64 } = options;
	return `${SETUP_SCRIPT}
${PREVIEW_HELPERS}

def __run_preview():
    figures = []
    seen = set()
    with OutputCapture() as cap:
        namespace = {"__name__": "__main__"}
        error = None
        try:
            # Figures left open by the sample tests that ran just before are not the preview's.
            if "matplotlib.pyplot" in sys.modules:
                sys.modules["matplotlib.pyplot"].close("all")
            exec(base64.b64decode("${codeB64}").decode("utf-8"), namespace)
            namespace["show"] = _tt_make_show(figures, seen)
            exec(base64.b64decode("${previewB64}").decode("utf-8"), namespace)
            _tt_remaining_pyplot_figures(figures, seen)
        except Exception:
            error = traceback.format_exc()
    return {
        "stdout": cap.get_stdout(),
        "stderr": cap.get_stderr().replace("Matplotlib is building the font cache; this may take a moment.\\n", ""),
        "error": error,
        "figures": figures,
    }

json.dumps(__run_preview())
`;
}
