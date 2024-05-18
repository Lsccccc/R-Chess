YELLOW = True
BLUE = False

board = [['O' for j in range(6)] for i in range(6)]
# 列表第一维是列（从左往右），第二维是行（从下往上）
# 将列表逆时针旋转90°即为棋盘

belong = [[None for j in range(6)] for i in range(6)] # None/T/F

ht = [0] * 6 # height 每一列的高度

# 拥有棋子数
pieces = {
    YELLOW: {
        'Y': 6,
        'T': 3
    }, 
    BLUE: {
        'Y': 6,
        'T': 3
    }
}

# printing
def color_print(color, *values, **kwargs):
    if color == 'y':
        print('\033[33m', end='')
    elif color == 'b':
        print('\033[34m', end='')
    elif color == 'w':
        print('\033[0m', end='')
    print(*values, **kwargs)
    print('\033[0m', end='')

def print_board():
    for i in range(5, -1, -1):
        for j in range(6):
            if belong[j][i] == None:
                color_print('w', board[j][i], end=' ')
            if belong[j][i] == YELLOW:
                color_print('y', board[j][i], end=' ')
            elif belong[j][i] == BLUE:
                color_print('b', board[j][i], end=' ')
        print()

def print_pieces():
    color_print('y', '黄方：')
    for i in pieces[YELLOW]:
        color_print('y', f'{i}: {pieces[YELLOW][i]}')

    color_print('b', '蓝方：')
    for i in pieces[BLUE]:
        color_print('b', f'{i}: {pieces[BLUE][i]}')

# error
def err():
    print('错误操作。请重试。')

# game functions
def put(p_name: str, x, y):
    """
    放置棋子
    """
    map = {
        "C": C,
        "Y": Y,
        "T": T
    }
    func = map[p_name.upper()]
    func(x, y)

def fall(x):
    """
    处理第x列的下落
    """
    n = board[x].count('O')
    for i in range(n):
        board[x].remove('O')
        belong[x].remove(None)
    for i in range(n):
        board[x].append('O')
        belong[x].append(None)

def C(x, y):
    """
    Chenxi
    棋子数量：无限个
    可吃：有，之后更新
    技能：无
    """
    global board, turn
    ht[x] += 1
    board[x][y] = 'C'
    belong[x][y] = turn
    fall(x)

def Y(x, y):
    """
    Yang
    棋子数量：6个
    可吃：C
    技能：无
    """
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
    """
    Tang
    棋子数量：3个
    可吃：C, Y
    技能：无
    """
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

turn = YELLOW  # True=黄 False=蓝
rd = 1 # round
while True:
    print_board()
    print_pieces()
    color_print(
        'y' if turn else 'b',
        f'第{rd}轮。轮到{"黄" if turn else "蓝"}方了。'
    )

    p_name = input('请输入要下的子：').upper()
    x, y = map(int, input('请输入要下的位置，用空格分开：').split())
    x -= 1
    y -= 1

    put(p_name, x, y)  
    
    turn = not turn
    rd += 1
