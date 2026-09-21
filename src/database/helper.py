from typing import Any

ColorKey = tuple[Any, ...] | None


def get_color_key(cell: Any) -> ColorKey:
    fill = cell.fill

    if fill.fill_type is None:
        return None

    color = fill.fgColor

    if color.type == "rgb":
        return ("rgb", color.rgb)
    if color.type == "indexed":
        return ("indexed", color.indexed)
    if color.type == "theme":
        return ("theme", color.theme, color.tint)
    if color.type == "auto":
        return ("auto", color.auto)

    return (color.type,)
