from trimesh import intersections
from trimesh import load
import matplotlib.pyplot as plt
from numpy import linspace, ceil
from sys import argv
import shapely

UNI_TOL = 1e-4

class LineSegment:
    point1 = (None, None)
    point2 = (None, None)
    adjacent_segs = []
    def __init__(self, point1_in, point2_in):
        self.point1 = point1_in
        self.point2 = point2_in

    def connected(self, lineSeg2):
        return (self.point1.equals_exact(lineSeg2.point1, UNI_TOL) or self.point1.equals_exact(lineSeg2.point2, UNI_TOL) or self.point2.equals_exact(lineSeg2.point1, UNI_TOL) or self.point2.equals_exact(lineSeg2.point2, UNI_TOL))
        
def is_in(point, list):
    for p in list:
        if p.equals_exact(point, 1e-6):
            return True
    return False

# Load the STL files and add the vectors to the plot
if __name__ == "__main__":
    your_mesh = load(argv[-1])

    midpoints = list()
    z_points = list()
    for i in linspace(0,1):
        midpoints.append(tuple(i*your_mesh.bounding_box.bounds.max(axis=0)))
        z_points.append(i*your_mesh.bounding_box.bounds.max(axis=0))

    for j in range(len(midpoints)):
        # j = int(ceil((len(midpoints)-1)/2))
        muh_lines = intersections.mesh_plane(your_mesh, (0,0,1), midpoints[j])
        seg_list = list(map(lambda line : LineSegment(shapely.Point(line[0,0:2]), shapely.Point(line[1,0:2])), muh_lines))
        if len(seg_list) <= 0:
            continue
        poly_segs = [seg_list.pop(0)]
        while True:
            current_seg = poly_segs[-1]
            for k in range(len(seg_list)):
                if seg_list[k].connected(current_seg):
                    poly_segs.append(seg_list.pop(k))
                    break
            break
        poly_points = []
        for s in poly_segs:
            if not is_in(s.point1, poly_points):
                poly_points.append(shapely.Point(s.point1))
            if not is_in(s.point2, poly_points):
                poly_points.append(shapely.Point(s.point2))

        print(poly_points)
        my_gon = shapely.Polygon(poly_points)
        x,y = my_gon.exterior.xy
        plt.plot(x,y)


    plt.show()