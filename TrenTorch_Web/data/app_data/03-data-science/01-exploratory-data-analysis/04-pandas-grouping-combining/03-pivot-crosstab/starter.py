import pandas as pd


def revenue_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Regions down, quarters across, each cell the sum of `revenue` (0 when
    there is no row). Both axes sorted ascending.
    """
    # TODO: Pivot with a sum and fill the empty cells.
    pass


def add_totals(grid: pd.DataFrame) -> pd.DataFrame:
    """
    A new grid with a "Total" row (column sums) and a "Total" column (row sums),
    including the grand total in the corner. The input is not changed.
    """
    # TODO: Append the margins by hand.
    pass


def count_table(df: pd.DataFrame, row: str, col: str) -> pd.DataFrame:
    """Counts of rows for every pair of values of `row` (down) and `col` (across)."""
    # TODO: Cross-tabulate the two columns.
    pass


def row_percentages(table: pd.DataFrame) -> pd.DataFrame:
    """Each cell as a percentage of its row total (rows sum to 100); zero rows -> NaN."""
    # TODO: Divide each row by its own total.
    pass


def to_long(wide: pd.DataFrame, id_col: str, var_name: str, value_name: str) -> pd.DataFrame:
    """
    Melt all columns except id_col. Columns: id_col, var_name, value_name.
    Ordered by id (original row order) then original column order; fresh index.
    """
    # TODO: Unpivot and order the rows.
    pass
