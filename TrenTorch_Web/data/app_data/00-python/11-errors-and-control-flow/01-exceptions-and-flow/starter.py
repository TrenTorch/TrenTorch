def validate_age(age: int) -> int:
    """
    Return `age` if it is an int from 0 to 150 inclusive.
    Otherwise raise a ValueError whose message is exactly
      "age must be between 0 and 150"
    """
    pass


def level_three(log: list) -> None:
    """
    Do these steps, in order:
      1. Append the string "L3 start" to `log`.
      2. Raise a RuntimeError with the message "boom".
      3. Append the string "L3 end" to `log`.
    (Step 3 must be written, and it must never run.)
    """
    pass


def level_two(log: list) -> None:
    """
    Append "L2 start" to `log`, call level_three(log), then
    append "L2 end" to `log`.
    """
    pass


def level_one(log: list) -> None:
    """
    Append "L1 start" to `log`, call level_two(log), then
    append "L1 end" to `log`.
    """
    pass


def first_element(items: list):
    """
    Return the first element of `items` by indexing position 0.
    Do not check for an empty list: an empty list should make
    Python itself raise an IndexError.
    """
    pass
