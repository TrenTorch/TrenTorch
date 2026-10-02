import numpy as np


def clean_and_reorder(data: np.ndarray, row_range: tuple, priority_indices: list) -> dict:
    region = data[row_range[0] : row_range[1], :]
    cleaned = np.where(region < 0, 0, region)
    reordered = cleaned[:, priority_indices]

    return {
        "region": region,
        "cleaned": cleaned,
        "reordered": reordered,
        "region_shares_memory_with_data": bool(np.shares_memory(region, data)),
        "cleaned_shares_memory_with_region": bool(np.shares_memory(cleaned, region)),
    }
