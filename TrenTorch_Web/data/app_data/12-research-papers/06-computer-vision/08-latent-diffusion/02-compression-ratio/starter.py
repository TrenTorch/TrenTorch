def compression_ratio(h, w, c_img, f, c_lat):
    """
    h, w: image height and width
    c_img: channels in the image (3 for RGB)
    f: spatial downsampling factor of the autoencoder
    c_lat: channels in the latent

    Returns:
        The ratio of image values to latent values: (h * w * c_img) / (latent_h * latent_w * c_lat).
    """
    # TODO: Divide the number of image values by the number of latent values (see Theory).
    pass
