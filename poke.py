from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from trimesh import intersections
from trimesh import load
import matplotlib.pyplot as plt
from numpy import linspace

# Load the STL files and add the vectors to the plot
your_mesh = load(r"")

midpoints = list()
z_points = list()
for i in linspace(0,1):
    midpoints.append(tuple(i*your_mesh.bounding_box.bounds.max(axis=0)))
    z_points.append(i*your_mesh.bounding_box.bounds.max(axis=0))

for j in range(len(midpoints)):
    muh_lines = intersections.mesh_plane(your_mesh, (0,0,1), midpoints[j])
    for l in muh_lines:
        plt.plot(l[:,0], l[:,1])
plt.show()