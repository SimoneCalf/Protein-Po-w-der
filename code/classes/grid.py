class Grid:
    def __init__(self, size):
        def create_grid(size):
            grid = []
            for y in range(size):
                row = []
                for x in range(size):
                    row.append(0)
                grid.append(row)
            return grid

        self.grid = create_grid(size)
