from __future__ import annotations
import json

class GateError(ValueError):
    pass

_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list, "null": type(None)}

class SchemaGate:
    def __init__(self, schema: dict[str, object], *, max_bytes: int = 1_000_000) -> None:
        if schema.get("type") != "object" or not isinstance(schema.get("properties", {}), dict):
            raise ValueError("v0.1 requires a top-level object schema")
        if max_bytes < 2:
            raise ValueError("max_bytes must be at least 2")
        self.schema = schema
        self.max_bytes = max_bytes
        self.text = ""
        self._seen_keys: set[str] = set()

    def feed(self, chunk: str) -> None:
        if not isinstance(chunk, str):
            raise TypeError("chunk must be text")
        self.text += chunk
        if len(self.text.encode("utf-8")) > self.max_bytes:
            raise GateError("stream exceeds max_bytes")
        self._scan()

    def _scan(self) -> None:
        depth = 0
        in_string = escape = False
        start = -1
        root_closed = False
        for index, char in enumerate(self.text):
            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                    if depth == 1:
                        tail = self.text[index + 1:].lstrip()
                        if tail.startswith(":"):
                            try:
                                key = json.loads(self.text[start:index + 1])
                            except json.JSONDecodeError as exc:
                                raise GateError("invalid JSON object key") from exc
                            self._check_key(key)
                continue
            if char == '"':
                in_string = True
                start = index
            elif char in "[{":
                if root_closed:
                    raise GateError("data appears after the root value")
                depth += 1
            elif char in "]}":
                depth -= 1
                if depth < 0:
                    raise GateError("closing delimiter has no opener")
                if depth == 0:
                    root_closed = True
            elif root_closed and not char.isspace():
                raise GateError("data appears after the root value")

    def _check_key(self, key: object) -> None:
        if not isinstance(key, str):
            raise GateError("object key is not text")
        properties = self.schema.get("properties", {})
        assert isinstance(properties, dict)
        if key not in properties and self.schema.get("additionalProperties", True) is False:
            raise GateError(f"unknown property: {key}")
        self._seen_keys.add(key)

    def finish(self) -> dict[str, object]:
        try:
            value = json.loads(self.text)
        except json.JSONDecodeError as exc:
            raise GateError(f"incomplete or invalid JSON: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise GateError("root value must be an object")
        required = self.schema.get("required", [])
        if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
            raise ValueError("required must be an array of property names")
        missing = [key for key in required if key not in value]
        if missing:
            raise GateError("missing required properties: " + ", ".join(missing))
        properties = self.schema.get("properties", {})
        assert isinstance(properties, dict)
        for key, item in value.items():
            rule = properties.get(key)
            if not isinstance(rule, dict) or "type" not in rule:
                continue
            expected = _TYPES.get(rule["type"])
            if expected is None:
                raise ValueError(f"unsupported schema type for {key}: {rule['type']}")
            if rule["type"] in ("integer", "number") and isinstance(item, bool):
                raise GateError(f"property {key} has wrong type")
            if not isinstance(item, expected):
                raise GateError(f"property {key} has wrong type")
        return value
