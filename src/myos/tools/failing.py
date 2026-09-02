def failing_tool(
        value: str
) -> str:

    raise ValueError(
        f"Intentional failure: {value}"
    )
