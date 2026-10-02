def build_sales_report(raw: str) -> str:
    lines_out = [f"{'ITEM':<12}{'QTY':>4}{'PRICE':>10}{'TOTAL':>12}"]

    rows = 0
    bytes_total = 0
    grand_total = 0.0

    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue

        fields = line.split(",")
        if len(fields) != 3:
            continue

        item_field, qty_field, price_field = (field.strip() for field in fields)
        if not qty_field.isdigit():
            continue

        quantity = int(qty_field)
        price = float(price_field)
        item = item_field.title()[:12]
        line_total = quantity * price

        lines_out.append(f"{item:<12}{quantity:>4}{price:>10.2f}{line_total:>12,.2f}")
        rows += 1
        bytes_total += len(item.encode("utf-8"))
        grand_total += line_total

    lines_out.append("-" * 38)
    lines_out.append(f"{'TOTAL':<26}{grand_total:>12,.2f}")
    lines_out.append(f"Rows: {rows} | UTF-8 bytes in items: {bytes_total}")

    return "\n".join(lines_out)
