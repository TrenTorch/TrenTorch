def build_point(x, y):
    return (x, y)


def configure_model(name, dimensions, metric):
    return {"name": name, "dimensions": dimensions, "metric": metric}


def format_record(identifier, value, label):
    return f"{identifier}={value} [{label}]"
