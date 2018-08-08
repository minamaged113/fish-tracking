import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import warp
import cv2


I = cv2.imread("/home/mghobria/Desktop/fish-tracking/frame_0_data.jpg", 0)
I = cv2.flip( I , 0)
I = cv2.flip( I , 1)
d0 = 3.3
dm = 23.3
am = 13.762
K = 2000
N, M = I.shape

xm = dm*np.tan(am/180*np.pi)
L = int(K/(dm-d0) * 2*xm)

sx = L/(2*xm)
sa = M/(2*am)
sd = N/(dm-d0)
O = sx*d0
Q = sd*d0

def invmap(inp):
    xi = inp[:,0]
    yi = inp[:,1]
    xc = (xi - L/2)/sx
    yc = (K + O - yi)/sx
    dc = np.sqrt(xc**2 + yc**2)
    ac = np.arctan(xc / yc)/np.pi*180
    ap = ac*sa
    dp = dc*sd
    a = ap + M/2
    d = N + Q - dp
    outp = np.array((a,d)).T
    return outp

out = warp(I, invmap, output_shape=(K, L))
plt.imshow(out,cmap='gray')
plt.show()

