from model.HexModel_ import *
from model.player_ import *
from view.HexView_ import *

if __name__ == "__main__":
    size = 11
    model = HexModel(size)
    view = HexView(model)
    view.run()