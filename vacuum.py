import sys
import heapq


algorithm = sys.argv[1]
world_file = sys.argv[2]

file = open(world_file, "r", encoding="utf-16")

width = int(file.readline().strip())
height = int(file.readline().strip())
world_str = file.readlines()

world_str = [line.strip() for line in world_str]

file.close()

direction_vector_row = [0, 1, 0, -1]
direction_vector_column = [-1, 0, 1, 0]

stack = [[0,0]]
visited_cells = [[False for i in range(width)] for j in range(height)]

def valid_cell(row, column):
    global width
    global height
    global visited_cells
    global world_str

    if (row < 0 or column < 0 or row >= height or column >= width):
        return False

    if (visited_cells[row][column]):
        return False

    if (world_str[row][column] == "#"):
        return False

    return True

def DFS(start_row, start_column, world):
    need_to_clean = False
    global visited_cells
    nodes_generated = 0
    nodes_expanded = 0

    stack = []
    stack.append((start_row, start_column, '', False))

    while(len(stack) != 0):
        if (need_to_clean):
            print("V")
            need_to_clean = False

        current_row, current_column, direction, is_backtracking = stack.pop()
        if not (0 <= current_row < height and 0 <= current_column < width):
            continue

        if is_backtracking:
            # Now we're backtracking — print reverse direction
            if direction == 'N':
                print("S")
            elif direction == 'S':
                print("N")
            elif direction == 'E':
                print("W")
            elif direction == 'W':
                print("E")
            continue

        if (valid_cell(current_row, current_column) == False):
            continue


        visited_cells[current_row][current_column] = True


        if world[current_row][current_column] == '*':
            need_to_clean = True

        if direction:
            print(direction)

        nodes_expanded += 1

        stack.append((current_row, current_column, direction, True))


        for i in range(3, -1, -1):
            x_next = current_row + direction_vector_row[i]
            y_next = current_column + direction_vector_column[i]

            if i == 0:
                next_direction = 'W'
            elif i == 1:
                next_direction = 'S'
            elif i == 2:
                next_direction = 'E'
            elif i == 3:
                next_direction = 'N'

            stack.append((x_next, y_next, next_direction, False))
            nodes_generated += 1
    print(f"{nodes_generated} nodes generated")
    print(f"{nodes_expanded} nodes expanded")


def UCS(start_row, start_column, world):
    global visited_cells

    total_nodes_generated = 0
    total_nodes_expanded = 0
    current_row, current_col = start_row, start_column

    while True:
        visited_cells = []
        for row_index in range(height):
            row = []
            for col_index in range(width):
                row.append(False)
            visited_cells.append(row)

        cost_map = []
        for row_index in range(height):
            row = []
            for col_index in range(width):
                row.append(float('inf'))
            cost_map.append(row)

        cost_map[current_row][current_col] = 0

        pq = []
        heapq.heappush(pq, (0, current_row, current_col, ""))

        found_goal = False
        direction_vector_row = [0, 1, 0, -1]
        direction_vector_column = [-1, 0, 1, 0]
        direction_labels = ['W', 'S', 'E', 'N']

        while pq:
            cost, row, col, path = heapq.heappop(pq)

            if visited_cells[row][col]:
                continue
            visited_cells[row][col] = True

            total_nodes_expanded += 1

            if world[row][col] == '*':
                # Print the full path to this goal
                for step in path:
                    print(step)
                print("V")
                current_row, current_col = row, col
                world[row] = world[row][:col] + '_' + world[row][col + 1:]
                found_goal = True
                break

            for i in range(3, -1, -1):
                new_row = row + direction_vector_row[i]
                new_col = col + direction_vector_column[i]

                if 0 <= new_row < height and 0 <= new_col < width:
                    if valid_cell(new_row, new_col):
                        new_cost = cost + 1
                        if new_cost < cost_map[new_row][new_col]:
                            cost_map[new_row][new_col] = new_cost
                            new_path = path + direction_labels[i]
                            heapq.heappush(pq, (new_cost, new_row, new_col, new_path))
                            total_nodes_generated += 1

        if not found_goal:
            break

    print(f"{total_nodes_generated} nodes generated")
    print(f"{total_nodes_expanded} nodes expanded")


if __name__ == '__main__':
    #finding location of @
    start_coordinates = []
    for row, column in enumerate(world_str):
        for index, character in enumerate(column):
            if character == "@":
                start_coordinates.append((row, index))


    if (algorithm == "depth-first"):
        DFS(start_coordinates[0][0], start_coordinates[0][1], world_str)
    elif (algorithm == "uniform-cost"):
        UCS(start_coordinates[0][0], start_coordinates[0][1], world_str)
    else:
        print("invalid alrgorithm")

