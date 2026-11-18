def compression_ratio(h, w, c_img, f, c_lat):
    return (h * w * c_img) / ((h // f) * (w // f) * c_lat)
