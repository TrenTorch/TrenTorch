import numpy as np


def make_tensor_record(
    data: np.ndarray, device: str = "cpu", requires_grad: bool = False
) -> dict:
    return {"data": data, "device": device, "requires_grad": requires_grad}


def add_records(a: dict, b: dict) -> dict:
    if a["device"] != b["device"]:
        raise ValueError(f"devices differ: {a['device']} vs {b['device']}")
    return {
        "data": a["data"] + b["data"],
        "device": a["device"],
        "requires_grad": a["requires_grad"] or b["requires_grad"],
    }


def detach_record(rec: dict) -> dict:
    return {"data": rec["data"], "device": rec["device"], "requires_grad": False}


def to_device_record(rec: dict, device: str) -> dict:
    if rec["device"] == device:
        return rec
    return {
        "data": rec["data"].copy(),
        "device": device,
        "requires_grad": rec["requires_grad"],
    }
