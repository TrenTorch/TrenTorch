def summarize_orders(orders: list) -> dict:
    units_by_customer = {}
    units_by_sku = {}
    customers_by_sku = {}
    customers_by_initial = {}

    for order in orders:
        customer = order["customer"]
        items = order["items"]
        units_by_customer.setdefault(customer, 0)

        for sku, quantity in items.items():
            units_by_customer[customer] += quantity
            units_by_sku[sku] = units_by_sku.get(sku, 0) + quantity
            customers_by_sku.setdefault(sku, set()).add(customer)

        if customer != "":
            initial = customer[0].upper()
            customers_by_initial.setdefault(initial, set()).add(customer)

    customers_by_sku = {sku: sorted(customers) for sku, customers in customers_by_sku.items()}
    customers_by_initial = {
        initial: sorted(customers) for initial, customers in customers_by_initial.items()
    }

    if units_by_sku:
        max_quantity = max(units_by_sku.values())
        top_sku = min(sku for sku, quantity in units_by_sku.items() if quantity == max_quantity)
    else:
        top_sku = None

    return {
        "units_by_customer": units_by_customer,
        "units_by_sku": units_by_sku,
        "top_sku": top_sku,
        "customers_by_sku": customers_by_sku,
        "customers_by_initial": customers_by_initial,
    }
