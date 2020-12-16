import os
import cv2
from config import C_ImageProc, Config

def process(frame):
    hist = cv2.calcHist([frame], [0], None, [IMAGE_PROC['N_HIST']], [0, 256])
    assert len(hist) == C_ImageProc['N_HIST']
    ave = np.mean(frame)
    std_dev = np.std_dev(frame)


def _threshold(frame):
    thresh = cv2.threshold(frame, C_ImageProc['THRESHOLD'], 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresh, 150, 200, -1) #Here there is a possibility to change these nums
    #Maybe use config options
    contours, hierachy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours = np.array(sorted(contours, key=len, reverse=True))
    n_allcontour = len(sorted_contours)
    size_list = [len(i) for i in sorted_contours]
    n_contours_abovethresh = np.count_nonzero(size_list>C_ImageProc['CONTOUR_SIZE_THRESH'])
    final_contours = sorted_contours[:n_contours_abovethresh]
    d_points = _contours_to_points(final_contours)

    return (n_contoursabovethresh, n_allcontour, d_points)

def _map_coords(coord, xdim, ydim, xint, yint):
    x = int(((coord[0]/Config['XDIM'])*Config['XMAP'])+0.5)
    y = int(((coord[1]/Config['YDIM'])*Config['YMAP'])+0.5)
    return (x,y)

def _contours_to_points(contours):
    d_points = dict()
    for i, point in enumerate(final_contours):
        _area = len(point)
        _tmp, _rad = cv2.minEnclosingCircle(point)
        _coord = _map_coords(_tmp, x_dim, y_dim, x_inter, y_inter)
        d_points[i] = (_area, _rad, _coord)
    return d_points