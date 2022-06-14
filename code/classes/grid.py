class Grid:
    def __init__(self, size):
        self.grid = self.create_grid(size)

    def create_grid(self, size):
        grid = []
        for y in range(size):
            row = []
            for x in range(size):
                row.append(0)
            grid.append(row)
        return grid