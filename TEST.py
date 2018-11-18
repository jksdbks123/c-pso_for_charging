from scipy.spatial import Voronoi,voronoi_plot_2d
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import numpy as np
if __name__ == '__main__':
    points = np.array([[1,2],[2,5],[2,4],[3,4],[7,2]])
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor)
    plt.show()