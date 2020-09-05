import numpy as np
import matplotlib.pyplot as plt
import DTW as dtw
# Credit for Displaying Distance Matrix: https://stackoverflow.com/questions/32503308/plot-distance-matrix-for-a-1d-array
# Credit for Matrix Labels: https://stackoverflow.com/questions/3529666/matplotlib-matshow-labels

a = [1, 2, 3, 4, 4, 5, 6, 6]
b = [1, 1, 2, 3, 4, 5, 5, 6, 7]
#
# template = np.load('template_derivative.npy')
# stream = np.load('stream_derivative.npy')
# stream = stream[520:850]
# plt.plot(stream[:,1])
# plt.plot(template[:])
# plt.show()
#
# dtw = dtw.DTW_Vis(template[:],stream[:,1])
dtw = dtw.DTW_Vis(a,b)
matrix = dtw.dtw_matrix()
path = dtw.warping_path(matrix)
# print(matrix)
# print(path)
dtw.display_matrix(matrix,path)
# dtw.dtw_hover_plot(path)
# dtw.dtw_drag_plot(path)
plt.show()