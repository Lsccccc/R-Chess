def color_print(color, *values, **kwargs):
    if color == 'y':
        print('\033[33m', end='')
    elif color == 'b':
        print('\033[34m', end='')
    elif color == 'w':
        print('\033[0m', end='')
    print(*values, **kwargs)
    print('\033[0m', end='')

board = [['O' for j in range(6)] for i in range(6)]
# 将列表逆时针旋转90°即为棋盘

belong = [[None for j in range(6)] for i in range(6)] # None/T/F

ht = [0] * 6
pieces = {
    True: {
        'Y': 6,
        'T': 3
    }, 
    False: {
        'Y': 6,
        'T': 3
    }
}

def print_board():
    for i in range(5, -1, -1):
        for j in range(6):
            if belong[j][i] == 0:
                print(board[j][i], end=' ')
            if belong[j][i] == 1:
                color_print('y', board[j][i], end=' ')
            elif belong[j][i] == 2:
                color_print('b', board[j][i], end=' ')
        print()

def fall(x):
    n = board[x].count('O')
    for i in range(n):
        board[x].remove('O')
        belong[x].remove(0)
    for i in range(n):
        board[x].append('O')
        belong[x].append(0)

def err():
    print('错误操作。请重试。')

def print_pieces():
    color_print('y', '黄方：')
    for i in pieces[0]:
        color_print('y', f'{i}: {pieces[1][i]}')

    color_print('b', '蓝方：')
    for i in pieces[1]:
        color_print('b', f'{i}: {pieces[1][i]}')

def C(x, y):
    global board, turn
    ht[x] += 1
    board[x][y] = 'C'
    belong[x][y] = turn
    fall(x)

def Y(x, y):
    global board, turn
    if y < ht[x]:
        if board[x][y] == 'C':
            board[x][y] = 'Y'
            belong[x][y] = turn
        else:
            err()
            return
    else:
        ht[x] += 1
        board[x][y] = 'Y'
        belong[x][y] = turn
        fall(x)
    pieces[turn]['Y'] -= 1

def T(x, y):
    global board, turn
    if y < ht[x]:
        if board[x][y] == 'C' or board[x][y] == 'Y':
            board[x][y] = 'T'
            belong[x][y] = turn
        else:
            err()
            return
    else:
        ht[x] += 1
        board[x][y] = 'T'
        belong[x][y] = turn
        fall(x)
    pieces[turn]['T'] -= 1

def put(p_name: str, x, y):
    """
    Put a chess
    """
    map = {
        "C": C,
        "Y": Y,
        "T": T
    }
    func = map[p_name.upper()]
    func(x, y)

turn = True  # T=黄 F=蓝
rd = 1 # 1黄 2蓝
while True:
    print_board()
    print_pieces()
    print(
        'y' if turn else 'b',
        f'第{rd}轮。轮到{"黄" if turn == 1 else "蓝"}方了。'
    )

    p_name = input('请输入要下的子：').upper()
    x, y = map(int, input('请输入要下的位置，用空格分开：').split())
    x -= 1
    y -= 1

    put(p_name)  
    
    turn = not turn
    rd += 1
    
    
