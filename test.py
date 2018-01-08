import numpy as np
import matplotlib.pyplot as plt
from kesmarag.swpt import SWPT

if __name__ == '__main__':
  signal = np.random.randn(1024,)
  model = SWPT(max_level=3)
  model.decompose(signal)
  res = model.get_level(3)
  plt.pcolor(res)
  plt.show()