def summarize_orders(orders: list) -> dict:
    """
    `orders` is a list of order dictionaries. Each has the form
      {"customer": <string>, "items": {<sku string>: <quantity int>, ...}}
    The "items" dictionary may be empty. Some orders may be for
    the same customer, and different orders may include the same
    sku.

    Return a dictionary with exactly these keys:

      "units_by_customer": dict mapping each customer to the
          total quantity across ALL of that customer's orders.
          A customer whose orders are all empty is still
          present, with 0.
      "units_by_sku": dict mapping each sku to its total
          quantity across all orders.
      "top_sku": the sku with the largest total quantity. If
          several tie, the one that is alphabetically first. If
          there are no skus at all, None.
      "customers_by_sku": dict mapping each sku to a SORTED list
          of the distinct customers who ordered it (each
          customer listed once).
      "customers_by_initial": dict mapping the UPPERCASE first
          letter of each customer to a SORTED list of the
          distinct customers with that initial. Customers with
          an empty string as their label are ignored here.

    `orders` and everything inside it must not be modified, and
    no list in the result may be shared between two keys.
    """
    pass
