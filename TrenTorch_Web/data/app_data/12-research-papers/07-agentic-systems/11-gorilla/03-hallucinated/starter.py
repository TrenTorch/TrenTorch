def is_hallucinated(call_name, api_list):
    """
    call_name: the API name the model called
    api_list: the names of APIs that actually exist

    Returns:
        True if the called API does not exist in the list.
    """
    # TODO: Report whether the called name is missing from the known APIs (see Theory).
    pass
