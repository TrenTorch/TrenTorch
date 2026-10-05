class ToolRegistry:
    """Registers tools and dispatches calls by name with structured results."""

    def __init__(self):
        # TODO
        pass

    def register(self, name: str, fn, description: str = "") -> None:
        """Add a tool; raises ValueError if the name is taken."""
        # TODO
        pass

    def list_tools(self) -> list[dict]:
        """[{'name', 'description'}, ...] sorted by name."""
        # TODO
        pass

    def call(self, name: str, args: dict) -> dict:
        """{'ok': True, 'result': ...} or {'ok': False, 'error': ...}; never raises."""
        # TODO
        pass
