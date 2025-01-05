from trimesh import intersections
from trimesh import load
import matplotlib.pyplot as plt
from numpy import linspace, ceil
from sys import argv
import shapely

UNI_TOL = 1e-7

class LineSegment:
    point1 = None
    point2 = None
    adjacent_segs = []
    def __init__(self, point1_in, point2_in):
        self.point1 = point1_in
        self.point2 = point2_in

    def connected(self, lineSeg2):
        return (self.point1.equals_exact(lineSeg2.point1, UNI_TOL) or self.point1.equals_exact(lineSeg2.point2, UNI_TOL) or self.point2.equals_exact(lineSeg2.point1, UNI_TOL) or self.point2.equals_exact(lineSeg2.point2, UNI_TOL))

    def __repr__(self):
        return self.point1.__repr__() + "--" + self.point2.__repr__()
        
def is_in(point, list):
    for p in list:
        if p.equals_exact(point, UNI_TOL):
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
    for z_val in midpoints:
        muh_lines = intersections.mesh_plane(your_mesh, (0,0,1), z_val)
        seg_list = list(map(lambda line : LineSegment(shapely.Point(line[0,0:2]), shapely.Point(line[1,0:2])), muh_lines))
        if len(seg_list) <= 0:
            continue
        poly_segs = [seg_list.pop(0)]
        END_OF_LOOP = False
        while True:
            current_seg = poly_segs[-1]
            for k, seg in enumerate(seg_list):
                if seg.connected(current_seg):
                    poly_segs.append(seg_list.pop(k))
                    break
            else:
                break

        poly_points = []

        poly_segs_len = len(poly_segs)
        for k in range(poly_segs_len):
            prev_seg = poly_segs[(k-1) % poly_segs_len]
            next_seg = poly_segs[(k+1) % poly_segs_len]
            
            if not is_in(poly_segs[k].point1, [prev_seg.point1, prev_seg.point2]) and not is_in(poly_segs[k].point2, [next_seg.point1, next_seg.point2]):
                poly_segs[k] = LineSegment(poly_segs[k].point2, poly_segs[k].point2)


        for s in poly_segs:
            if not is_in(s.point1, poly_points):
                poly_points.append(s.point1)
            if not is_in(s.point2, poly_points):
                poly_points.append(s.point2)

        my_gon = shapely.Polygon(poly_points)
        x,y = my_gon.exterior.xy
        plt.plot(x,y)
        
    plt.show()