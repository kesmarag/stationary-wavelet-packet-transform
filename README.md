## instalation using pip:

pip install git+https://github.com/kesmarag/stationary-wavelet-packet-transform.git


## usage
```python
import numpy as np
import matplotlib.pyplot as plt
from kesmarag.swpt import SWPT

signal = np.load('/home/kesmarag/sw06_den.npy')
model = SWPT(max_level=3)
model.decompose(signal.T)
res = model.get_level(3)
'''
  level 1 => (0.A, 1.D)
  level 2 => (0.AA, 1.AD), (3.DA, 2.DD)
  level 3 => (0.AAA, 1.AAD), (3.ADA, 2.ADD), (7.DAA, 6.DAD), (4.DDA, 5.DDD)
'''
res_np = np.array(res)
plt.pcolor(np.squeeze(res_np))
plt.show()
```