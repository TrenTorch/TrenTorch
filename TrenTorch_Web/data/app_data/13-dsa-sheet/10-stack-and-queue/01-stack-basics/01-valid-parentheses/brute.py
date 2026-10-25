def valid_brackets(s):
    while True:
        shorter = s.replace("()", "").replace("[]", "").replace("{}", "")
        if shorter == s:
            return s == ""
        s = shorter
