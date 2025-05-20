import random 
from random import randint

DROP_VALUES = ['0','1','2','3','4','5','6','7','8','9']

N = 10
Num = 10
MAX_INTG = 1e4

FIELDS = [N, N]
APPEARANCE = 'light'

coordinates = []
start_end = [[0, 0], [N-1, N-1]]
for row in range(0, N-1):
    for column in range(0, N-1):
        if [row, column] not in start_end:
            coordinates.append([row, column])

TREES = random.choices(coordinates, k = random.randint(N*2, N*3))
TREES_DICT = {}
for tree in TREES:
    TREES_DICT[str(tree)] = True

coordinates_without_trees = [c for c in coordinates if c not in TREES]
NUMBERS = random.choices(coordinates_without_trees, k = Num)            # It's a list filled with coordinates for numbers.

NUMBER = {}
for cor in NUMBERS:
    NUMBER[MAX_INTG * cor[0] + cor[1]] = randint(1, 10)# (max_intg * x + y) is a unique formula for each coordinate.
                                                            # That shows us the key of each number.

COLORS = {
    'path':           ('RED', 'RED'),
    'main':           ('#a6cc9b', '#011c06'),
    'maze':           ('#faf4f0', '#051407'),
    'text':           ('#120d0c', '#ebebeb'),
    'trees':          ('#0d632d', '#0ced5e'),
    'hover':          ('#c91c3c', '#ff432e'),
    'switch':         ('#033006', '#d7fce4'),
    'numbers':        ('#000000', '#ffffff'),
    'buttons':        ('#ff432e', '#780c20'),
    'numbers fg':     ('#4ef5c3', '#0a9169'),
    'small frame':    ('#e3d56d', '#754f27'),
    'creators hover': ('#33001f', '#fbff03')
}

FONTS = {
    'maze':     ('Jokerman',25),
    'theme':    ('calibri',20,'bold'),
    'new cor':  ('arial',20),
    'SE':       ('Cambria bold',30),
    'numbers':  ('Tahoma',16),
    'creators': ('Harrington',27),
    'names':    ('Algerian',25),
    'submit':   ('Cambria',20)
}

NAMES = [
    'Mr.Alipour',
    'Mr.Kamali',
    'Mr.Petrosian'
]