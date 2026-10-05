def is_hallucinated(call_name, api_list):
    return call_name not in api_list
