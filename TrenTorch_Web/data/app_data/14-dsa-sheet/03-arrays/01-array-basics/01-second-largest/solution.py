def second_largest(nums):
    largest = second = None
    for x in nums:
        if largest is None or x > largest:
            second = largest
            largest = x
        elif x < largest and (second is None or x > second):
            second = x
    return -1 if second is None else second
