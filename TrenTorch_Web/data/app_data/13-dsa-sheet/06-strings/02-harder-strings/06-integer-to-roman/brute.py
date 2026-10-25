def integer_to_roman(num):
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    thousands = ["", "M", "MM", "MMM"]
    return (
        thousands[num // 1000]
        + hundreds[num // 100 % 10]
        + tens[num // 10 % 10]
        + ones[num % 10]
    )
