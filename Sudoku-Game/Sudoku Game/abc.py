board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - ")
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


# Kiểm tra ràng buộc
def valid(bo, num, pos):
    # Check row
    for i in range(len(bo)):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


# Trả về ds chứa các vị trí chưa có giá trị
def find_empty(bo):
    b = []
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                b.append([i * len(bo[0]) + j])
    return b


# Trả về mảng 2 chiều chứa các vị trí chưa có giá trị và các giá trị thỏa mãn ô đó
def graph(bo):
    b = find_empty(bo)
    for i in range(len(b)):
        row = b[i][0] // len(bo[0])
        col = b[i][0] % len(bo[0])
        for j in range(1, len(bo[0]) + 1):
            if valid(bo, j, (row, col)):
                b[i].append(j)
    return b


# Trả về hàng cột và giá trị của ô cần thêm
def choose(bo, b):
    for i in range(len(b)):
        if len(b[i]) == 2:
            row = b[i][0] // len(bo[0])
            col = b[i][0] % len(bo[0])
            return row, col, i
    return False


# Hàm chính
def a123(bo):
    b = graph(bo)
    if len(b) == 0:
        return 0
    while (choose(bo, b) != 'False'):
        past = choose(bo, b)
        row = past[0]
        col = past[1]
        bo[row][col] = b[past[2]][1]
        b = graph(bo)
        if len(b) == 0:
            break
        else:
            a123(bo)
    return 0


print_board(board)
a123(board)
print("______________________")
print_board(board)
