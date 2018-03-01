import pywt
from pywt._thresholding import hard, soft
from sklearn.preprocessing import StandardScaler


class SWPT(object):

  def __init__(self, wavelet='db4', max_level=3):
    self._wavelet = wavelet
    self._max_level = max_level
    self._coeff_dict = {}

  def decompose(self, signal):
    pth = ['']
    self._coeff_dict[''] = np.squeeze(signal)
    for l in range(self._max_level):
      pth_new = []
      for p in pth:
        coeff = pywt.swt(
            self._coeff_dict[p],
            wavelet=self._wavelet,
            level=self._max_level - len(p),
            start_level=len(p))
        p_run = p
        for i, C in enumerate(coeff[::-1]):
          self._coeff_dict[p_run + 'A'] = C[0]
          self._coeff_dict[p_run + 'D'] = C[1]
          if i < len(coeff) - 1 and len(p_run) < self._max_level - 1:
            pth_new.append(p_run + 'D')
            p_run = p_run + 'A'
      pth = list(pth_new)

  def get_level(self, level, order='freq', thresholding=None, threshold=None):
    assert order in ['natural', 'freq']
    r = []
    result = []
    for k in self._coeff_dict:
      if len(k) == level:
        r.append(k)
    if order == 'freq':
      graycode_order = self._get_graycode_order(level)
      for p in graycode_order:
        if p in r:
          result.append(self._coeff_dict[p])
    else:
      print('The natural order is not supported yet.')
      exit(1)
    # apply the thressholding
    if thresholding in ['hard', 'soft']:
      if isinstance(threshold, (int, float)):
        if thresholding == 'hard':
          result = hard(result, threshold)
        else:
          result = soft(result, threshold)
      else:
        print('Threshold must be an integer or float number')
        exit(1)
    return result

  def get_coefficient_vector(self, name):
    return self._coeff_dict[name]

  def _get_graycode_order(self, level, x='A', y='D'):
    graycode_order = [x, y]
    for i in range(level - 1):
      graycode_order = [x + path for path in graycode_order] + \
                       [y + path for path in graycode_order[::-1]]
    return graycode_order




if __name__ == '__main__':
  import numpy as np
  import matplotlib.pyplot as plt
  from sklearn.preprocessing import StandardScaler
  threshold = 0.1
  signal = np.load('/home/kesmarag/Github/sw06_new_modeling/signal_sw06_den.npy')
  # signal = np.squeeze(signal)
  print(signal.shape)
  wt = SWPT(max_level=4)
  wt.decompose(signal)
  coef_orig = wt.get_level(4)
  coef_soft = wt.get_level(4, thresholding='soft', threshold=threshold)
  coef_hard = wt.get_level(4, thresholding='hard', threshold=threshold)
  plt.figure()
  plt.pcolor(coef_orig)
  plt.colorbar()
  plt.figure()
  plt.pcolor(coef_soft)
  plt.colorbar()
  plt.figure()
  plt.pcolor(coef_hard)
  plt.colorbar()
  plt.figure()
  plt.pcolor(coef_orig - coef_soft)
  plt.colorbar()
  plt.figure()
  plt.pcolor(coef_orig - coef_hard)
  plt.colorbar()
  plt.figure()
  coef_soft_sc = StandardScaler().fit_transform(coef_soft.T).T
  plt.pcolor(coef_soft_sc)
  plt.colorbar()
  plt.show()
