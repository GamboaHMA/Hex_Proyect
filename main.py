from model.HexModel_ import *
from view.HexView_ import *

if __name__ == "__main__":
    size = 3
    model = HexBoard(size)
    view = HexView(model)
    view.run()