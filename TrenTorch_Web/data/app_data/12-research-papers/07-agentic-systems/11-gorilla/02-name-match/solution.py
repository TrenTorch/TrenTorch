def api_name_matches(call, api):
    return call.split("(", 1)[0].strip() == api
