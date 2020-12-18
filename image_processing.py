import os
import cv2
from config import C_ImageProc, Config
import numpy as np
import logging


def process(frame):
    hist = cv2.calcHist([frame], [0], None, [C_ImageProc['N_HIST']], [0, 256])
    assert len(hist) == C_ImageProc['N_HIST']
    ave = np.mean(frame)
    std_dev = np.std(frame)
    n_contabovethresh, n_allcontour, contours = _contours(frame)
    output = (ave, std_dev, n_contabovethresh, n_allcontour, contours, hist)
    return output

def _contours(frame):
    _, thresh = cv2.threshold(frame, C_ImageProc['THRESHOLD'], 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(thresh, 150, 200, -1) #Here there is a possibility to change these nums
    #Maybe use config options
    contours, hierachy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours = np.array(sorted(contours, key=len, reverse=True))
    n_allcontour = len(sorted_contours)
    size_list = [len(i) for i in sorted_contours]
    n_contours_abovethresh = np.count_nonzero(np.array(size_list) >C_ImageProc['CONTOUR_SIZE_THRESH'])
    final_contours = sorted_contours[:n_contours_abovethresh]
    d_points = _contours_to_points(final_contours)

    return (n_contours_abovethresh, n_allcontour, d_points)

def _map_coords(coord, xdim, ydim, xint, yint):
    x = int(((coord[0]/Config['XDIM'])*Config['XMAP'])+0.5)
    y = int(((coord[1]/Config['YDIM'])*Config['YMAP'])+0.5)
    return (x,y)

def _contours_to_points(contours):
    d_points = list()
    for point in contours:
        _area = len(point)
        _tmp, _rad = cv2.minEnclosingCircle(point)
        x, y = _map_coords(_tmp, Config['XDIM'], Config['YDIM'], Config['XMAP'], Config['YMAP'])
        d_points.append((_area, _rad, x, y))
    return d_points