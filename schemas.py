from jsonschema import Draft7Validator

# Простая схема для JSON ответов демостенда
add_to_cart_resp_schema = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "message": {"type": "string"},
    },
    "required": ["success"]
}

login_resp_schema = {
    "type": "object",
    "properties": {
        "redirect": {"type": "string"},
        "success": {"type": "boolean"}
    }
}


def validate_json(instance: dict, schema: dict):
    errors = sorted(Draft7Validator(schema).iter_errors(instance), key=lambda e: e.path)
    assert not errors, "Schema validation errors: \n" + "\n".join(
        f"- {'/'.join(map(str, e.path))}: {e.message}" for e in errors)
