import copy


class Matrix:
    instances_created = 0

    def __init__(self, rows):
        self.rows = copy.deepcopy(rows)
        Matrix.instances_created += 1

    def shape(self):
        return (len(self.rows), len(self.rows[0]))

    def __repr__(self):
        return f"Matrix({self.rows!r})"

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        return list(self.rows[index])

    def transpose(self):
        num_rows, num_cols = self.shape()
        new_rows = [[self.rows[i][j] for i in range(num_rows)] for j in range(num_cols)]
        return Matrix(new_rows)

    def scale(self, k):
        new_rows = [[value * k for value in row] for row in self.rows]
        return Matrix(new_rows)


class IdentityMatrix(Matrix):
    def __init__(self, n):
        rows = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        super().__init__(rows)
