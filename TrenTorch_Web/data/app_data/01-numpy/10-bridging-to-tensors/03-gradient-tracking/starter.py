import numpy as np


def make_tensor_record(
    data: np.ndarray, device: str = "cpu", requires_grad: bool = False
) -> dict:
    """
    Return a dictionary modelling a tensor:
      {"data": data, "device": device, "requires_grad": requires_grad}
    `data` is stored as given (no copy).
    """
    pass


def add_records(a: dict, b: dict) -> dict:
    """
    Element-wise add two tensor records.

    Raise ValueError if their devices differ.
    Otherwise return a NEW record with:
      "data":          a["data"] + b["data"]   (NumPy broadcasting applies)
      "device":        the shared device
      "requires_grad": True if a OR b requires grad, else False
    """
    pass


def detach_record(rec: dict) -> dict:
    """
    Return a new record with the same device as `rec` and
    requires_grad=False, whose "data" is THE SAME buffer as
    rec["data"] (no copy — writing through one must be visible through
    the other). `rec` is not modified.
    """
    pass


def to_device_record(rec: dict, device: str) -> dict:
    """
    Return a record on `device`.
      - If `rec` is already on `device`, return `rec` itself.
      - Otherwise return a NEW record on `device` whose "data" is an
        independent COPY of rec["data"] (values equal, memory not
        shared), preserving requires_grad.
    `rec` is not modified.
    """
    pass
