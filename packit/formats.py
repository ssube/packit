from json import dumps


def format_str_or_json(value: str | dict | list) -> str:
    if isinstance(value, (dict, list)):
        return dumps(value)

    return value


def format_bullet_list(items: list[str]) -> str:
    # remove newlines within each item
    items = [str(item).replace("\n", " ").replace("\r", "") for item in items]
    return "\n".join(f"- {item}" for item in items)
