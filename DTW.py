# ///-----------------------------------------------------------------
# ///	File Name:			DTW.py
# ///	Description:		Visualization and Interactivity of the Dynamic Time Warping Algorithm
# ///	Author:				Sayok R. Das
# ///	Date:				<DateTime>
# ///	Notes:				<Notes>
# ///	Contact:			Embedded Signal Processing Lab, Texas A&M University
# ///	Revision History:
# ///	Name:			Date:			Description:
# ///-----------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import mplcursors as mplc


# DTW  Module File

class select_map:
    """
    An path editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them


    """

    showverts = True
    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, pathpatch):

        self.ax = pathpatch.axes
        canvas = self.ax.figure.canvas
        self.pathpatch = pathpatch
        self.pathpatch.set_animated(True)

        x, y = zip(*self.pathpatch.get_path().vertices)

        self.line, = self.ax.plot(x, y, marker='o', markerfacecolor='r', animated=True)

        self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.pathpatch)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def pathpatch_changed(self, pathpatch):
        """This method is called whenever the pathpatch object is called."""
        # only copy the artist props to the line (except visibility)
        vis = self.line.get_visible()
        plt.Artist.update_from(self.line, pathpatch)
        self.line.set_visible(vis)  # don't use the pathpatch visibility state

    def get_ind_under_point(self, event):
        """
        Return the index of the point closest to the event position or *None*
        if no point is within ``self.epsilon`` to the event position.
        """
        # display coords
        xy = np.asarray(self.pathpatch.get_path().vertices)
        xyt = self.pathpatch.get_transform().transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.sqrt((xt - event.x) ** 2 + (yt - event.y) ** 2)
        ind = d.argmin()

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def button_press_callback(self, event):
        """Callback for mouse button presses."""
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        """Callback for mouse button releases."""
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None

    def key_press_callback(self, event):
        """Callback for key presses."""
        if not event.inaxes:
            return
        if event.key == 't':
            self.showverts = not self.showverts
            self.line.set_visible(self.showverts)
            if not self.showverts:
                self._ind = None

        self.canvas.draw()

    def motion_notify_callback(self, event):
        """Callback for mouse movements."""
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        vertices = self.pathpatch.get_path().vertices

        vertices[self._ind] = x, y
        self.line.set_data(zip(*vertices))

        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.pathpatch)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)


class DTW_Vis:
    def __init__(self, series1, series2):  # Class Initialization
        self.series1 = series1
        self.series2 = series2
        self.path = mpath.Path
        self.fig, self.ax = plt.subplots()

    def not_static(self):  # Defining a member function as not static
        pass

    def dtw_matrix(self):  # Defining DTW Algorithm
        n = len(self.series1)
        m = len(self.series2)
        dist_matrix = np.empty([n, m], dtype=float)  # Distance matrix as a 2d array

        for i in range(n):
            for j in range(m):
                dist_matrix[i][j] = ((self.series1[i] - self.series2[j]) ** 2)  # distance between points

        for i in range(n):
            for j in range(m):
                dist_matrix[i][j] = dist_matrix[i][j] + min(dist_matrix[i - 1][j], dist_matrix[i - 1][j - 1],
                                                            dist_matrix[i][j - 1])  # adding the value into 2D array
        return dist_matrix

    def warping_path(self, matrix):  # Defining the "Shortest Path" among the distance matrix
        self.not_static()
        i = matrix.shape[0] - 1
        j = matrix.shape[1] - 1
        path_dict = dict()
        while i > 0 or j > 0:
            ind_of_min = np.argmin([matrix[i - 1][j], matrix[i - 1][j - 1], matrix[i][j - 1]])
            path_dict.update({(i, j): matrix[i][j]})
            if ind_of_min == 0:
                i = i - 1
                j = j
                path_dict.update({(i, j): matrix[i][j]})
            elif ind_of_min == 1:
                i = i - 1
                j = j - 1
                path_dict.update({(i, j): matrix[i][j]})
            elif ind_of_min == 2:
                i = i
                j = j - 1
                path_dict.update({(i, j): matrix[i][j]})
        return path_dict

    def display_matrix(self, matrix, warping_path):
        plt.figure()
        # plt.matshow(matrix, cmap="Reds")
        # ax = plt.gca()
        # ax.set_xticklabels([''] + self.series2)
        # ax.set_yticklabels([''] + self.series1)
        # plt.title('Distance Matrix')
        # for i in range(len(self.series1)):
        #     for j in range(len(self.series2)):
        #         plt.text(j, i, matrix[i, j], horizontalalignment='center', verticalalignment='center')
        warping_path_mat = np.zeros((matrix.shape[0],matrix.shape[1]))
        for index in warping_path:
            warping_path_mat[index[0],index[1]] = warping_path[index]
        plt.matshow(warping_path_mat)


    def dtw_hover_plot(self, path):  # Plotting of the series
        plt.figure(2)
        plt.title('Display on hover')

        spaced_series = []
        x_axis1 = np.arange(len(self.series1))
        x_axis2 = np.arange(len(self.series2))

        for i in range(len(self.series1)):
            spaced_series.append(self.series1[i] + 10)

        warping_path = []
        plt.plot(x_axis1, spaced_series, '-r', label='Series 1')
        plt.plot(x_axis2, self.series2, '-g', label='Series 2')
        for index in path:
            warping_path_line, = plt.plot([x_axis1[index[0]], x_axis2[index[1]]],
                                          [spaced_series[index[0]], self.series2[index[1]]],
                                          color='black', label=f'Distance={path[index]}')
            warping_path.append(warping_path_line)

        series1_point = []
        series2_point = []
        for index in path:
            point1, = plt.plot(x_axis1[index[0]], spaced_series[index[0]], 'go', label='Series 1 point')
            series1_point.append(point1)
            point2, = plt.plot(x_axis2[index[1]], self.series2[index[1]], 'ro', label='Series 2 point')
            series2_point.append(point2)

        cursor1 = mplc.cursor(series1_point + series2_point, hover=True, highlight=True)
        pairs1 = dict(zip(series1_point, series2_point))
        pairs1.update(zip(series2_point, series1_point))

        @cursor1.connect("add")
        def on_add(sel):
            sel.extras.append(cursor1.add_highlight(pairs1[sel.artist]))

        cursor2 = mplc.cursor(series1_point + warping_path, hover=True, highlight=True)
        pairs2 = dict(zip(series1_point, warping_path))
        pairs2.update(zip(warping_path, series1_point))

        @cursor2.connect("add")
        def on_add(sel):
            sel.extras.append(cursor1.add_highlight(pairs2[sel.artist]))

        cursor3 = mplc.cursor(series2_point + warping_path, hover=True, highlight=True)
        pairs3 = dict(zip(series2_point, warping_path))
        pairs3.update(zip(warping_path, series2_point))

        @cursor3.connect("add")
        def on_add(sel):
            sel.extras.append(cursor1.add_highlight(pairs3[sel.artist]))

    def dtw_drag_plot(self, short_path):
        self.fig.suptitle('Selective Mapping (Drag on Click)')
        self.ax.set_title('Press t to toggle the vertex markers')

        spaced_series = []
        for i in range(len(self.series1)):
            spaced_series.append(self.series1[i] + 10)
        x_axis1 = np.arange(len(self.series1))
        x_axis2 = np.arange(len(self.series2))

        pathdata1 = []
        pathdata1.append((self.path.MOVETO, (x_axis1[0], spaced_series[0])))
        for i in range(len(self.series1)):
            pathdata1.append((self.path.LINETO, (x_axis1[i], spaced_series[i])))
        codes1, verts1 = zip(*pathdata1)
        path1 = mpath.Path(verts1, codes1)
        patch1 = mpatches.PathPatch(path1, facecolor='white', edgecolor='red', linewidth=1.5)
        self.ax.add_patch(patch1)
        selective_mapping1 = select_map(patch1)

        pathdata2 = []
        pathdata2.append((self.path.MOVETO, (x_axis2[0], self.series2[0])))
        for i in range(len(self.series2)):
            pathdata2.append((self.path.LINETO, (x_axis2[i], self.series2[i])))
        codes2, verts2 = zip(*pathdata2)
        path2 = mpath.Path(verts2, codes2)
        patch2 = mpatches.PathPatch(path2, facecolor='white', edgecolor='green', linewidth=1.5)
        self.ax.add_patch(patch2)
        selective_mapping2 = select_map(patch2)

        pathdata3 = []
        for index in short_path:
            pathdata3.append((self.path.MOVETO, (x_axis1[index[0]], spaced_series[index[0]])))
            pathdata3.append((self.path.LINETO, (x_axis2[index[1]], self.series2[index[1]])))
        codes3, verts3 = zip(*pathdata3)
        path3 = mpath.Path(verts3, codes3)
        patch3 = mpatches.PathPatch(path3, facecolor='white', linewidth=1.5)
        self.ax.add_patch(patch3)
        selective_mapping3 = select_map(patch3)

        self.ax.set_ylim(-15, 25)

        plt.show()
