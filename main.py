from collections import deque


class TestCase:
    def __init__(self, row, column, distance) -> None:
        self.row = row
        self.column = column

class Main:
    def __init__(self, value) -> None:
        self.visited = set()
        self.grid = [value]
        self.chair, self.stick, self.banana = (0, 0), (0, 0), (0, 0)

    def bfs(self, rows, columns):
        can_take_banana = False  
        queue = deque()
        self.visited.add((rows, columns))
        queue.append((rows, columns))
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        while queue:
            temp_row, temp_column = queue.popleft()
            for direct_row, direct_column in directions:
                r, c = temp_row + direct_row, temp_column + direct_column
                if (r in range(len(rows))
                        and c in range(len(columns))
                        and self.grid[r][c] == '0'
                        and (r, c) not in self.visited):
                    queue.append((r, c))
                    self.visited.add((r, c))

                if self.grid[r, c] == 1:
                    self.chair = (r, c)
                if self.grid[r, c] == 2:
                    self.stick = (r, c)
                if self.grid[r, c] == 3:
                    self.banana = (r, c)
                if self.chair != (0, 0) and self.stick != (0, 0) and self.banana != (0, 0):
                    break
                



    def isValid(self, rows, columns):
        for row in range(rows):
            for column in range(columns):
                if self.grid[row][column] == '0' and (row, column) not in self.visited:
                    self.bfs(row, column)

      
