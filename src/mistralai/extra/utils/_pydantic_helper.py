from typing import Any


def rec_strict_json_schema(schema_node: Any) -> Any:
    """
    Recursively set the additionalProperties property to False for all objects in the JSON Schema
    that do not already define it.
    This makes the JSON Schema strict (i.e. no additional properties are allowed).
    """
    # Include int and float as terminal types to handle JSON Schema constraint keywords
    # like minLength, maxLength, minItems, maxItems, minimum, maximum, etc.
    if isinstance(schema_node, (str, bool, int, float)) or schema_node is None:
        return schema_node
    if isinstance(schema_node, dict):
        # Keep an explicit additionalProperties (e.g. the value schema of a dict[str, T]
        # field): overwriting it would forbid every key of that field.
        if schema_node.get("type") == "object" and "additionalProperties" not in schema_node:
            schema_node["additionalProperties"] = False
        for key, value in schema_node.items():
            schema_node[key] = rec_strict_json_schema(value)
    elif isinstance(schema_node, list):
        for i, value in enumerate(schema_node):
            schema_node[i] = rec_strict_json_schema(value)
    else:
        raise ValueError(f"Unexpected type: {schema_node}")
    return schema_node
