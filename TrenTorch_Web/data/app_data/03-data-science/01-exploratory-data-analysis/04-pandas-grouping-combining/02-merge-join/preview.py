import pandas as pd

customers = pd.DataFrame({"id": [3, 1, 2, 4], "name": ["Cara", "Asha", "Ben", "Dev"], "city": ["Goa", "Pune", "Delhi", "Agra"]})
orders = pd.DataFrame({"order_id": [105, 101, 102, 103, 104], "customer_id": [1, 1, 3, 9, 3], "amount": [20.0, 10.0, 5.0, 99.0, 7.5]})
print("orders with their customer (inner join; order 103 has an unknown customer):")
print(orders_with_customers(customers, orders))
print("\ncustomer totals (everyone, even without orders):")
print(customer_totals(customers, orders))
print("\ncustomers without orders:")
print(customers_without_orders(customers, orders))
try:
    safe_merge(customers, pd.DataFrame({"id": [1, 1], "x": [1, 2]}), "id")
except ValueError as error:
    print("\nsafe_merge refused a duplicated key:", type(error).__name__)
