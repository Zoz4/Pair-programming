import numpy as np
import cv2
from matplotlib import pyplot as plt

t = np.array([[1,2,3]],np.int32)
s = np.empty((0,3),np.int32)
t = np.append(t,s,axis=0)
print(s.shape)
print(t.shape)
tr = np.full((len(s),1),1.0)
print(tr.shape)