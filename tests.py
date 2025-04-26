from model.HexModel_ import *

board = HexBoard(5)
board_1 = HexBoard(6)

board.board = [
    [1, 0, 0, 0, 0],
     [0, 1, 0, 2, 0],
      [0, 2, 0, 0, 1],
       [1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
]

bridges = get_bridges(board)
assert(bridges == [(0, 0), (1, 1), (1, 3), (2, 1), (2, 4), (4, 3)]), f'bridges debe ser igual a {[(0, 0), (1, 1), (1, 3), (2, 1), (2, 4), (4, 3)]}'

# template2
# player 2
assert(template_a2((1,2), board, 2)), f'deber devolver True'
assert(not template_a2((1,0), board, 2)), f'deber devolver False'
assert(template_a2((3,1), board, 2)), f'deber devolver True'
assert(not template_a2((3,3), board, 2)), f'deber devolver False'

# player 1
assert(template_a2((1,1), board, 1)), f'debe devolver True'
assert(not template_a2((0,1), board, 1)), f'debe devolver True'
assert(template_a2((4,3), board, 1)), f'debe devolver True'
assert(not template_a2((2,3), board, 1)), f'debe devolver True'

# template3
# player2
board.board = [
    [0, 0, 0, 0, 1, 0],
     [0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
         [1, 0, 0, 1, 0, 0],
]

board_1.board = [
    [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 1],

]
# dowm
assert(not template_a3((3,2), board, 2)), f'debe devolver False'
assert(not template_a3((3,4), board, 2)), f'debe devolver False'
assert(not template_a3((3,2), board, 2)), f'debe devolver False'
assert(not template_a3((3,4), board_1, 2)), f'debe devolver False'
assert(template_a3((3,3), board_1, 2)), f'debe devolver True'

# up
assert(not template_a3((2,1), board, 2)), f'debe devolver False'
#assert(not template_a3((3,4), board, 2)), f'debe devolver False'
#assert(not template_a3((3,2), board, 2)), f'debe devolver False'
#assert(not template_a3((3,4), board_1, 2)), f'debe devolver False'
#assert(template_a3((3,3), board_1, 2)), f'debe devolver True'

