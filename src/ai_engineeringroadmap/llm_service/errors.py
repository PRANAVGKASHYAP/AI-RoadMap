# this is going to serve as the base class for all errors in the LLM service
from collections.abc import Generator, Mapping
from contextlib import contextmanager

import httpx


class LLMError(Exception):
    """Base class for all errors in the LLM service."""

    def __init__(self, message: str, *, status_code: int | None = None):
        # the params in this init means the messge is a positional arg , and the status code is a key word arg
        super().__init__(message)
        self.status_code = status_code


# all the below erros are going to inherit from these errors


class BadRequestError(LLMError):
    """
    for response types
    400,404,413,422
    i.e the request being made by the client is wrong
    """


class AuthError(LLMError):
    """
    for response types
    401,403
    i.e the client is not authorized to make the request
    """


class RateLimitError(LLMError):
    """
    for response types
    429
    i.e the client is making too many requests in a short period of time
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        retry_after: float | None = None,
    ):
        super().__init__(message, status_code=status_code)
        self.retry_after = retry_after


class ServerError(LLMError):
    """
    for response types
    500,502,503,504
    i.e the server is having issues and cannot process the request
    """


class LLMTimeoutError(LLMError):
    """
    for response types
    408
    i.e the request took too long to process and timed out
    """


# adding utility functions


def parse_retry_after(retry_after: str) -> float | None:
    """
    Parse the Retry-After header value and return the number of seconds to wait before retrying.
    If the value is not a valid integer, return None.
    """
    try:
        return float(retry_after)
    except ValueError:
        return None


def map_http_error(status: int, headers: Mapping[str, str], body: str) -> LLMError:
    """
    Map HTTP status codes to corresponding LLMError subclasses.
    """
    body = body[:200]
    if status in (400, 404, 413, 422):
        return BadRequestError(body, status_code=status)
    elif status in (401, 403):
        return AuthError(body, status_code=status)
    elif status == 429:
        # get the value of the retry after form one of the header mappings
        retry_after_value = parse_retry_after(headers.get("Retry-After", ""))
        return RateLimitError(body, status_code=status, retry_after=retry_after_value)
    elif status in (500, 502, 503, 504):
        return ServerError(body, status_code=status)
    elif status == 408:
        return LLMTimeoutError(body, status_code=status)
    else:
        return LLMError(body, status_code=status)


# httpx has a built in method that can be called that throws exception for any http response other that 2xx


def raise_for_llm_error(response: httpx.Response) -> None:
    try:
        response.raise_for_status()  # this call with raise an exception only if the response if of any http code other than 2xx
    except httpx.HTTPStatusError as ex:
        # we are going to chain the exceptions here , and the ex is the original error
        # so its gonna say that the custom exception happened because the httpx request had this exception
        raise map_http_error(
            response.status_code, response.headers, response.text
        ) from ex


# this is a new way to use the context manager , the below function is going ot be used in a with call
@contextmanager
def translate_timeouts() -> Generator[None]:
    try:
        yield
    except httpx.TimeoutException as exc:
        raise LLMTimeoutError("LLM request timed out") from exc


def is_retryable(ex: BaseException) -> bool:
    return isinstance(ex, (RateLimitError, ServerError, LLMTimeoutError))
