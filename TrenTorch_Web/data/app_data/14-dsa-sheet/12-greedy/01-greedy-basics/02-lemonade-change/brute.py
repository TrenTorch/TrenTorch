from functools import lru_cache


def lemonade_change(bills):
    bills = tuple(bills)

    @lru_cache(maxsize=None)
    def go(i, fives, tens):
        if i == len(bills):
            return True
        bill = bills[i]
        if bill == 5:
            return go(i + 1, fives + 1, tens)
        if bill == 10:
            return fives >= 1 and go(i + 1, fives - 1, tens + 1)
        return (tens >= 1 and fives >= 1 and go(i + 1, fives - 1, tens - 1)) or (
            fives >= 3 and go(i + 1, fives - 3, tens)
        )

    return go(0, 0, 0)
