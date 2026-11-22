import json

# this module is to read and streram the file that is supposed ot represent the lls calls

# write a function that is a generator and gives one line of a file at a time


def iter_records(path: str):
    # this function yields a line
    with open(path) as f:  # with is used as its a built in context manager
        for line in f:
            try:
                curr_line = json.loads(line)
                yield curr_line
            except json.JSONDecodeError as e:
                print(f"jSON DECODER ERROR: {e} in line: {line}")
                continue  # skip to the next line if there's an error


def summarize(path: str) -> dict:
    total_tokens = 0
    models = {}
    iterator = iter_records(path)
    for line in iterator:
        parsed_llm_response = line
        model = parsed_llm_response.get("model", "unknown_model")
        tokens = parsed_llm_response.get("tokens", 0)
        if model not in models:
            models[model] = tokens
        else:
            models[model] += tokens
        total_tokens += tokens
    summarized_records = {"total_tokens": total_tokens, "models": models}
    return summarized_records
