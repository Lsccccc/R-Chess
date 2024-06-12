from colorama import Fore
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
        'C': '∞',
        'Y': 6,
        'T': 3,
        'A': 2,
        'H': 2,
        'R': 1,
        'B': 1,
        'X': 1,
        'Z': 1
    }, 
    BLUE: {
        'C': '∞',
        'Y': 6,
        'T': 3,
        'A': 2,
        'H': 2,
        'R': 1,
        'B': 1,
        'X': 1,
        'Z': 1
    }
}

# printing
def color_print(color, *values, **kwargs):
    color_codes = {
        'r': Fore.RED,
        'y': Fore.YELLOW,
        'b': Fore.BLUE,
        'w': Fore.WHITE
    }
    print(color_codes[color], end='')
    print(*values, **kwargs)
    print(Fore.WHITE, end='')

def print_board():
    print('----------------------')
    for i in range(5, -1, -1):
        print('|', end='  ')
        for j in range(6):
            if belong[j][i] == None:
                color_print('w', board[j][i], end=' ' * (3 - len(board[j][i])))
            if belong[j][i] == YELLOW:
                color_print('y', board[j][i], end=' ' * (3 - len(board[j][i])))
            elif belong[j][i] == BLUE:
                color_print('b', board[j][i], end=' ' * (3 - len(board[j][i])))
        print('|')
    print('----------------------')

def print_pieces():
    color_print('y', '黄方：', end='')
    for i in pieces[YELLOW]:
        color_print('y', f'{pieces[YELLOW][i]}{i}', end=' ')

    color_print('b', '\n蓝方：', end='')
    for i in pieces[BLUE]:
        color_print('b', f'{pieces[BLUE][i]}{i}', end=' ')
    print()

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
    """放置棋子"""
    if ht[x] >= 6:
        err('本列已满。')
        return
    
    map = {
        "C": C,
        "Y": Y,
        "T": T,
        "A": A,
        "H": H,
        "R": R,
        "B": B,
        "X": X,
        "Z": Z
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

def judge():
    """判定胜者""" 
    # 横四个
    for x in range(3):
        for y in range(6):
            if belong[x][y] == belong[x+1][y] == belong[x+2][y] == belong[x+3][y] != None:
                return belong[x][y]

    # 纵四个
    for x in range(6):
        for y in range(3):
            if belong[x][y] == belong[x][y+1] == belong[x][y+2] == belong[x][y+3] != None:
                return belong[x][y]

    # "/"斜四个
    for x in range(3):
        for y in range(3):
            if belong[x][y] == belong[x+1][y+1] == belong[x+2][y+2] == belong[x+3][y+3] != None:
                return belong[x][y]
    
    # "\"斜四个
    for x in range(3):
        for y in range(3, 6):
            if belong[x][y] == belong[x+1][y-1] == belong[x+2][y-2] == belong[x+3][y-3] != None:
                return belong[x][y]

def eat(x, y):
    board[x][y] = 'O'
    belong[x][y] = None

def eat_down(p_name, x, eat_list):
    """
    往下吃一个棋子，C、Y、T、A技能
    """
    global board, turn
    if ht[x] == 0:
        board[x][0] = p_name
        belong[x][0] = turn
        ht[x] += 1
    else:
        board[x][ht[x]] = p_name
        belong[x][ht[x]] = turn
        if board[x][ht[x] - 1] in eat_list and belong[x][ht[x] - 1] != turn:
            eat(x, ht[x] - 1)
        fall(x)

def C(x):
    """
    Chenxi
    棋子数量：无限个
    可吃：H, B, X, Z
    技能：向下吃一个能吃的子，仅吃对方
    """
    eat_down('C' if rd != 2 else 'C+', x, 'H B X Z'.split())

def Y(x):
    """
    Yang
    棋子数量：6个
    可吃：C, H(+), B(+), X(+), Z(+)
    技能：向下吃一个能吃的子，仅吃对方
    """
    if pieces[turn]['Y'] == 0:
        err('棋子耗尽。')
        return
    
    eat_down('Y', x, 'C H H+ B B+ X X+ Z Z+'.split())
    
    pieces[turn]['Y'] -= 1

def T(x):
    """
    Tang
    棋子数量：3个
    可吃：C(+), Y
    技能：向下吃一个能吃的子，仅吃对方
    """

    if pieces[turn]['T'] == 0:
        err('棋子耗尽。')
        return
    eat_down('T', x, 'C C+ Y'.split())
    pieces[turn]['T'] -= 1

def A(x):
    """
    Tang
    棋子数量：2个
    可吃：R
    技能：向下吃一个子，仅吃R
    """

    if pieces[turn]['A'] == 0:
        err('棋子耗尽。')
        return
    eat_down('A', x, ['R'])
    pieces[turn]['A'] -= 1

def H(x):
    """
    Hao
    棋子数量：2个
    可吃：C(+) Y(+) T H(+) B(+) X(+) Z(+)
    技能：炸掉周围八个棋子中能吃的，包括本方棋子
    """
    global board, turn
    eat_list = 'C C+ Y Y+ T H H+ B B+ X X+ Z Z+'.split()
    if pieces[turn]['H'] == 0:
        err('棋子耗尽。')
        return
    
    h = ht[x]
    board[x][h] = 'H'
    belong[x][h] = turn

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= x + i < 6 and 0 <= h + j < 6 and board[x + i][h + j] in eat_list:
                eat(x + i, h + j)
    
    for i in range(max(0, x - 1), min(5, x + 1)):
        fall(i)
    
    pieces[turn]['H'] -= 1

def R(x):
    """
    Rui
    棋子数量：1个
    可吃：C(+) Y(+) T H(+) B(+) X(+) Z(+) A
    技能：向下连续吃子，直到碰到不能吃的，包括本方棋子
    """
    global board, turn
    eat_list = 'C C+ Y Y+ T H H+ B B+ X X+ Z Z+ A'.split()
    if pieces[turn]['R'] == 0:
        err('棋子耗尽。')
        return
    
    h = ht[x]
    board[x][h] = 'R'
    belong[x][h] = turn

    eat_h = h - 1
    while eat_h >= 0 and board[x][eat_h] in eat_list:
        eat(x, eat_h)
        eat_h -= 1
    
    fall(x)
    
    pieces[turn]['R'] -= 1

def B(x):
    """
    Behaviour
    棋子数量：1个
    可吃：C(+) Y(+) T H(+) B(+) X(+) Z(+) A
    技能：分别向左、右连续吃子，直到碰到不能吃的，包括本方棋子
    """
    global board, turn
    eat_list = 'C C+ Y Y+ T H H+ B B+ X X+ Z Z+ A'.split()
    if pieces[turn]['B'] == 0:
        err('棋子耗尽。')
        return
    
    h = ht[x]
    board[x][h] = 'B'
    belong[x][h] = turn

    eat_x = x - 1
    while eat_x >= 0 and board[eat_x][h] in eat_list:
        eat(eat_x, h)
        eat_x -= 1
    
    eat_x = x + 1
    while eat_x < 6 and board[eat_x][h] in eat_list:
        eat(eat_x, h)
        eat_x += 1
    
    for i in range(6):
        fall(i)
    
    pieces[turn]['B'] -= 1

def X(x):
    """
    Xin
    棋子数量：1个
    可吃：C(+) Y(+) H(+) B(+) Z(+)
    技能：炸掉周围八个棋子中男性角色，包括本方棋子
    """
    global board, turn
    eat_list = 'C C+ Y Y+ H H+ B B+ Z Z+'.split()
    if pieces[turn]['X'] == 0:
        err('棋子耗尽。')
        return
    
    h = ht[x]
    board[x][h] = 'X'
    belong[x][h] = turn

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= x + i < 6 and 0 <= h + j < 6 and board[x + i][h + j] in eat_list:
                eat(x + i, h + j)
    
    for i in range(max(0, x - 1), min(5, x + 1)):
        fall(i)
    
    pieces[turn]['X'] -= 1

def Z(x):
    global board, turn
    if pieces[turn]['H'] == 0:
        err('棋子耗尽。')
        return
        
    if ht[x] == 0:
        board[x][0] = 'Z'
        belong[x][0] = turn
        ht[x] += 1
    else:
        board[x][ht[x]] = 'Z'
        belong[x][ht[x]] = turn
        if not board[x][ht[x] - 1].endswith('+'):
            board[x][ht[x] - 1] += '+'
        if board[x][ht[x] - 1] == 'T+':
            p = input('请输入将T升级为什么（A或R）：').upper()
            while p != 'A' and p != 'R':
                p = input('输入错误。请输入将T升级为什么（A或R）：').upper()
            board[x][ht[x] - 1] = p
    pieces[turn]['Z'] -= 1


turn = YELLOW  # True=黄 False=蓝
rd = 1 # round
winner = None
while True:
    print_board()
    winner = judge()
    if winner != None:
        color_print(
            'y' if winner else 'b',
            f'''#############\n# {"黄" if winner else "蓝"}方赢了！#\n#############
            '''
        )
        break
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
