class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, fn, description=""):
        if name in self._tools:
            raise ValueError(f"tool already registered: {name}")
        self._tools[name] = (fn, description)

    def list_tools(self):
        return [{"name": n, "description": self._tools[n][1]} for n in sorted(self._tools)]

    def call(self, name, args):
        entry = self._tools.get(name)
        if entry is None:
            return {"ok": False, "error": f"unknown tool: {name}"}
        try:
            return {"ok": True, "result": entry[0](**args)}
        except Exception as exc:
            return {"ok": False, "error": f"tool error: {exc}"}
