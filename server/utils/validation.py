def validate_query(
    query: str,
    max_results: int,
    max_allowed: int = 20,
) -> None:
    """
    Validate research search parameters.
    """

    if not isinstance(query, str):
        raise ValueError(
            "query must be a string."
        )

    if not query.strip():
        raise ValueError(
            "query cannot be empty."
        )

    if not isinstance(max_results, int):
        raise ValueError(
            "max_results must be an integer."
        )

    if max_results < 1:
        raise ValueError(
            "max_results must be at least 1."
        )

    if max_results > max_allowed:
        raise ValueError(
            f"max_results cannot exceed {max_allowed}."
        )
