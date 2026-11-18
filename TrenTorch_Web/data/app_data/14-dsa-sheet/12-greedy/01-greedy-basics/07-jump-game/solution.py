def can_jump(nums):
    far = 0
    for i, jump in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + jump)
    return True
