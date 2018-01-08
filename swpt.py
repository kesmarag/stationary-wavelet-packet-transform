import pywt


class SWPT(object):

  def __init__(self, wavelet='db4', max_level=3):
    self._wavelet = wavelet
    self._max_level = max_level
    self._coeff_dict = {}

  def decompose(self, signal):
    pth = ['']
    self._coeff_dict[''] = signal
    for l in range(self._max_level):
      pth_new = []
      for p in pth:
        coeff = pywt.swt(self._coeff_dict[p],
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

  def get_level(self, level, order='freq'):
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
      print('natural order is not supported yet.')
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
