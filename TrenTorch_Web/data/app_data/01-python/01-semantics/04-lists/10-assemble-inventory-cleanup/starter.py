def label_of(row: list) -> str:
    """
    Return the label of an inventory row. A row has the form
    [label, quantity]; the label is the first element.
    """
    pass


def quantity_of(row: list) -> int:
    """
    Return the quantity of an inventory row: the second element.
    """
    pass


def process_inventory(rows: list, min_qty: int) -> list:
    """
    `rows` is a list of rows, each row a list [label, quantity]
    (label is a string, quantity an int).

    Perform these steps, in order:
      1. Take an independent deep copy of `rows` as it is now
         (call it `snapshot`).
      2. Remove IN PLACE every row whose quantity is less than
         `min_qty`. The outer list `rows` must remain the same
         object, and the surviving row objects must remain the
         same row objects (no row is replaced or copied).
      3. Sort `rows` IN PLACE so that quantities are in
         descending order, and rows with equal quantities are in
         ascending order of label. Achieve this with two stable
         sort passes using label_of and quantity_of as key
         functions (least important key first).
      4. Build `top_labels`: a list of the labels of the first
         up to 3 rows of the sorted `rows`.
      5. Build `quantities`: a list of the quantities of all
         remaining rows, in order.

    Return a list of three elements: [snapshot, top_labels,
    quantities].
    """
    pass
