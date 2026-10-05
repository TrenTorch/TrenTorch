import json


def parse_tool_call(text):
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("name"), str) and "arguments" in obj:
            args = obj["arguments"]
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError as exc:
                    raise ValueError("arguments are not valid JSON") from exc
            if not isinstance(args, dict):
                raise ValueError("arguments must be an object")
            return obj["name"], args
    raise ValueError("no tool call found")
