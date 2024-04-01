from json import dumps


def format_str_or_json(value: str | dict | list) -> str:
    if isinstance(value, (dict, list)):
        return dumps(value)

    return value


def format_bullet_list(items: list[str], bullet="-") -> str:
    # remove newlines within each item
    items = [str(item).replace("\n", " ").replace("\r", "") for item in items]
    return "\n".join(f"{bullet} {item}" for item in items)


def format_number_list(items: list[int], start=1) -> str:
    items = [str(item).replace("\n", " ").replace("\r", "") for item in items]
    return "\n".join(f"{start + i}. {item}" for i, item in enumerate(items))
