def format_ascii(ascii_str, width):
    return "\n".join(
        [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
    )