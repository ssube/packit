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
    str_items = [str(item).replace("\n", " ").replace("\r", "") for item in items]
    return "\n".join(f"{start + i}. {item}" for i, item in enumerate(str_items))


def join_list(items: list[str], separator=", ") -> str:
    return separator.join(items)


def join_sentences(items: list[str]) -> str:
    return join_list(items, separator=". ") + "."


def join_lines(items: list[str]) -> str:
    return join_list(items, separator="\n")


def join_paragraphs(items: list[str]) -> str:
    return join_list(items, separator="\n\n")
