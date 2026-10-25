import posixpath


def simplify_path(path):
    return posixpath.normpath("/" + path.lstrip("/"))
