import { toBase64 } from '../code-execution/to-base64';

// tests.py files reach other code through `load_solution(...)` and a module
// variable (`_module.helper`, `plain_gb.train(...)`, or
// `load_solution("path").entropy` inside a test body). On disk each call loads
// a real module, with its own namespace. In the browser there are no files, so
// this stands in for one:
//
// - load_solution("path") runs that solution, together with the solutions it
//   depends on, in a namespace of its own and returns it. A helper the student
//   happens to define under the same name can no longer change how the
//   reference solution behaves, which is what a flat, shared namespace allowed
//   (a reference loss of 10.9 instead of 6.98 in the beam search question).
// - `_module = load_solution(f"...")` (the question's own solution) reads and
//   writes the live namespace, i.e. whatever the student wrote. Assigning to it
//   patches the student's function, the way assigning to a real module does.
//
// Only added when the cleaned tests still refer to load_solution or to a bare
// module variable, so tests that need neither are unchanged. Names that are
// plain aliases (`find_best_split = load_solution(...).find_best_split`) are
// not bound to these objects: the dependency's real function is already
// defined.
export function buildLoadSolutionShim(sourcesByPath: Record<string, string>): string {
	const sources = Object.entries(sourcesByPath)
		.map(([path, code]) => `    ${JSON.stringify(path)}: ${JSON.stringify(toBase64(code))},`)
		.join('\n');

	return `
import base64 as _base64


class _Namespace:
    def __init__(self, names):
        self.__dict__["_names"] = names

    def __getattr__(self, name):
        names = self.__dict__["_names"]
        if name in names:
            return names[name]
        raise AttributeError("module has no attribute " + repr(name))

    def __setattr__(self, name, value):
        self.__dict__["_names"][name] = value


_dependency_sources = {
${sources}
}
_dependency_modules = {}


def load_solution(path):
    if path not in _dependency_modules:
        if path not in _dependency_sources:
            raise RuntimeError("load_solution(" + repr(path) + ") is not available in the browser")
        namespace = {"__name__": path}
        exec(_base64.b64decode(_dependency_sources[path]).decode("utf-8"), namespace)
        _dependency_modules[path] = _Namespace(namespace)
    return _dependency_modules[path]
`;
}
