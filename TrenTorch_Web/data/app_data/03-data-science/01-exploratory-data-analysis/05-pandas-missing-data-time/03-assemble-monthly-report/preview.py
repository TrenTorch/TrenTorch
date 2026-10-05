import pandas as pd

customers = pd.DataFrame({"id": [1, 2, 3], "region": ["west", "east", "west"]})
orders = pd.DataFrame(
    {
        "order_id": range(1, 10),
        "customer_id": [1, 2, 3, 2, 1, 9, 2, 1, 3],
        "order_date": ["2024-01-05", "2024-01-20", "2024-01-31", "2024-03-02", "2024-03-15", "2024-03-16", "not a date", "2024-04-01", "2024-04-30"],
        "amount": [10.0, 30.0, 10.0, 40.0, 20.0, 999.0, 500.0, 5.0, 15.0],
    }
)
print("the orders include a bad date and an unknown customer, both ignored:")
print(monthly_report(orders, customers))
