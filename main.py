from collections import deque


class TestCase:
    def __init__(self, row, column, distance) -> None:
        self.row = row
        self.column = column
        self.distance = distance

class Main:
    def __init__(self) -> None:
        self.visited = set()
        self.grid = []

    def bfs(self, rows, columns):
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

        


    def isValid(self, rows, columns, visited, grid):
        for row in range(rows):
            for column in range(columns):
                if grid[row][column] == '0' and (row, column) not in self.visited:
                    self.bfs(row, column)
                    
# Phuc an cut
            
      
