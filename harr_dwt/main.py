import cv2
import numpy as np
import matplotlib.pyplot as plt
from pywt import dwt2, idwt2


# calling cover image
A = cv2.imread('host_tiger.jpeg') # same dim
host = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
LL, (LH, HL, HH) = dwt2(host, 'haar')

# calling watermark image
B = cv2.imread('barbara512.jpg') # same dim
watermark = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
LL_w, (LH_w, HL_w, HH_w) = dwt2(watermark, 'haar')

# adding watermark
manipulated = LL_w * 0.9
new_host_LL = LL + manipulated
result_LL = idwt2((new_host_LL,( LH, HL, HH)), 'haar')
cv2.imwrite('watermarked.jpeg', result_LL)


# extracting
wm_LL,( m_LH, wm_HL, m_HH) = dwt2(result_LL, 'haar')
new_LL = (wm_LL - LL) / 0.1
new_image = idwt2((new_LL, (LH_w, HL_w, HH_w)), 'haar')
cv2.imwrite('extracted.jpeg', new_image)