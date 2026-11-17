def and_of_range(left, right):
    shift = (left ^ right).bit_length()
    return left >> shift << shift
