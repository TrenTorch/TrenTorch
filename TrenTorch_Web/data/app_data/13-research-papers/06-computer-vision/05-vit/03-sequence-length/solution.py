def vit_seq_length(img, p):
    return (img // p) ** 2 + 1
