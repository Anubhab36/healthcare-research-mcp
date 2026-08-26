import pytest

from server.utils.validation import validate_query


def test_valid_query():
    validate_query(
        "artificial intelligence ECG",
        5,
    )


def test_empty_query():
    with pytest.raises(
        ValueError,
        match="query cannot be empty",
    ):
        validate_query(
            "",
            5,
        )


def test_zero_results():
    with pytest.raises(
        ValueError,
        match="at least 1",
    ):
        validate_query(
            "ECG",
            0,
        )


def test_excessive_results():
    with pytest.raises(
        ValueError,
        match="cannot exceed 20",
    ):
        validate_query(
            "ECG",
            21,
        )


def test_non_integer_result_limit():
    with pytest.raises(
        ValueError,
        match="must be an integer",
    ):
        validate_query(
            "ECG",
            "5",
        )
