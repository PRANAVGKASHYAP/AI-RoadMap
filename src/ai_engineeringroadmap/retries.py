from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def call_flaky_service():
    print("Trying the request...")
    raise ConnectionError("temporary failure")


call_flaky_service()
