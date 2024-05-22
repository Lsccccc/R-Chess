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
    color_codes = {
        'r': '31',
        'y': '33',
        'b': '34',
        'w': '0'
    }
    print(f'\033[{color_codes[color]}m', end='')
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
class GameError(Exception):
    def __init__(self, msg='错误操作。请重试。'):
        self.msg = msg

    def __str__(self):
        return self.msg

def err(msg='错误操作。请重试。'):
    raise GameError(msg)

# game functions
def put(p_name: str, x):
    """
    放置棋子
    """
    if ht[x] >= 6:
        err('本列已满。')
        return
    
    map = {
        "C": C,
        "Y": Y,
        "T": T
    }
    func = map[p_name.upper()]
    func(x)

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
    ht[x] = 6 - n

def eat_down(p_name, x, eat_list):
    """
    往下吃一个棋子，C、Y、T技能
    """
    global board, turn
    if ht[x] == 0:
        board[x][0] = p_name
        belong[x][0] = turn
        ht[x] += 1
    else:
        board[x][ht[x]] = p_name
        belong[x][ht[x]] = turn
        if board[x][ht[x] - 1] in eat_list:
            board[x][ht[x] - 1] = 'O'
            belong[x][ht[x] - 1] = None
        fall(x)

def C(x):
    """
    Chenxi
    棋子数量：无限个
    可吃：有，之后更新
    技能：无
    """
    eat_down('C', x, [])

def Y(x):
    """
    Yang
    棋子数量：6个
    可吃：C
    技能：无
    """
    if pieces[turn]['Y'] == 0:
        err('棋子耗尽。')
        return
    
    eat_down('Y', x, ['C'])
    
    pieces[turn]['Y'] -= 1

def T(x):
    """
    Tang
    棋子数量：3个
    可吃：C, Y
    技能：无
    """

    if pieces[turn]['T'] == 0:
        err('棋子耗尽。')
        return
    eat_down('T', x, ['C', 'Y'])
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

    while True:
        try:
            x = int(input('请输入要下的列：')) - 1
            p_name = input('请输入要下的子：').upper()
            put(p_name, x)
        except KeyError:
            color_print('r', '输入错误。请重试。')
        except ValueError:
            color_print('r', '输入错误。请重试。')
        except GameError as e:
            color_print('r', e)
        else:
            break
    
    turn = not turn
    rd += 1
