def bool_result(value: str, **kwargs) -> bool:
    value = value.replace("Rating:", "")
    value = value.replace("Rank:", "")
    value = value.strip()

    # take the first phrase from longer answers
    if "." in value:
        value = value.split(".")[0]

    if "," in value:
        value = value.split(",")[0]

    # take the first word from longer answers
    if " " in value:
        value = value.split(" ")[0]

    return value.lower() == "yes"


def int_result(value: str, **kwargs) -> int:
    value = value.replace("Rating:", "")
    value = value.replace("Rank:", "")
    value = value.strip()

    return int(value)


def str_result(value: str, **kwargs) -> str:
    return str(value).strip()
