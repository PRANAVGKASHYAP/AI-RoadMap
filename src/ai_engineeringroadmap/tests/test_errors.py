# this file is to test out the error handelling written in the errors.py class

import pytest
from ai_engineeringroadmap.llm_service.errors import *


def make_response(
    status: int, body: str = "", headers: dict[str, str] | None = None
) -> httpx.Response:
    return httpx.Response(
        status,
        text=body,
        headers=headers or {},
        request=httpx.Request("POST", "https://llm.test/v1/complete"),
    )


def test_all_errors_inherit_from_llm_error():
    assert issubclass(RateLimitError, LLMError) == True
    assert issubclass(BadRequestError, LLMError) == True


def test_map_http_error_picks_right_class():
    bad_req_response = make_response(400, "bad request made by the client")
    parsed_llm_error = map_http_error(
        bad_req_response.status_code, None, bad_req_response.text
    )
    assert isinstance(parsed_llm_error, BadRequestError)


def test_unknown_status_is_base_llm_error():
    make_unknown_error = make_response(418, " this is an unknown error")
    parsed_llm_error = map_http_error(
        make_unknown_error.status_code, None, make_unknown_error.text
    )
    assert isinstance(parsed_llm_error, LLMError)


def test_rate_limit_error_carries_retry_after():
    retry_error = make_response(
        429, "retry on this request after Retry-Aster time", {"Retry-After": "2"}
    )
    parsed_error = map_http_error(
        retry_error.status_code, retry_error.headers, retry_error.text
    )
    assert isinstance(
        parsed_error, RateLimitError
    )  # checks the type, and narrows it for your editor
    assert parsed_error.retry_after == 2.0
    assert parsed_error.status_code == 429


def test_long_body_is_truncated():
    large_body = "bad request made by the client" * 100  # 3000 chars
    bad_req_response = make_response(400, large_body)
    mapped_error = map_http_error(
        bad_req_response.status_code, bad_req_response.headers, bad_req_response.text
    )
    assert len(str(mapped_error)) <= 200


def test_retry_after_parsing():
    assert parse_retry_after("1.2") == 1.2
    assert parse_retry_after("3") == 3.0
    assert parse_retry_after("abc") is None


def test_raise_for_llm_status_sets_cause():
    response = make_response(429, "rate limited", {"Retry-After": "2"})
    with pytest.raises(RateLimitError) as err:
        raise_for_llm_error(response)
    assert isinstance(err.value.__cause__, httpx.HTTPStatusError)


def test_2xx_does_not_raise():
    good_response = make_response(200, "200Ok", None)
    check_raised_error = raise_for_llm_error(good_response)
    assert check_raised_error == None
    pass


def test_timeout_is_translated():
    original = httpx.ReadTimeout("slow")
    # outer with: we expect LLMTimeoutError to come out
    # inner with: translate_timeouts() should catch the httpx timeout and convert it
    with pytest.raises(LLMTimeoutError) as exc_info:
        with translate_timeouts():
            raise original
    # these checks go AFTER the with block, once the exception has been captured
    assert exc_info.value.__cause__ is original  # `raise ... from exc` set the cause


@pytest.mark.parametrize(
    "err, expected",
    [
        (RateLimitError("slow down", status_code=429), True),
        (ServerError("server down", status_code=500), True),
        (LLMTimeoutError("timed out"), True),
        (AuthError("bad key", status_code=401), False),
        (BadRequestError("bad input", status_code=400), False),
        (LLMError("unknown"), False),
        (ValueError("not an LLM error"), False),
    ],
)
def test_is_retryable(err, expected):
    assert is_retryable(err) is expected
