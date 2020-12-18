from config import Config, C_ImageProc
import pandas as pd
import numpy as np
import os
#Dataframe : for i in intervals : 'Column1. Column2 etc... 

class writeData:
    def __init__(self, path, bufsize):
        self.path = path
        self.columns = self._columns()
        self.bufsize = bufsize
        self.num_columns = len(self.columns)
        self.bufsize = bufsize
        self.bufpos = 0
        self.df = pd.DataFrame(columns=self.columns)
        self._remove_existing_csv(path)
        self.first_write = True
        self.time = 0
        self.time_interval = Config['FRAMERATE']/1

    def _remove_existing_csv(self, path):
        if os.path.isfile('{}'.format(path)):
            os.system('rm {}'.format(path))
        os.system('touch {}'.format(path))

    def _write_df(self):
        self.df.to_csv(self.path, mode='a', header=self.first_write)
        self.first_write = False
        self.df = pd.DataFrame(columns=self.columns)

    def _columns(self):
        indep = ['Time','Mean', 'Stddev', 'n_ContoursAbovethresh', 'n_contours']
        colour_bins = ['Bin{}'.format(i) for i in range(C_ImageProc['N_HIST'])]
        y_intervals = ['Interval{}'.format(i) for i in range(Config['YMAP'])] 
        out = indep + colour_bins + y_intervals
        #assert(len(out) == self.num_columns)
        return out
    
        #Concat lists.
    #How does value list come out?
    #ave, std_dev, n_contabovethresh, n_allcontour, contours, hist)
    def add_new(self, value_list):
        self.time = self.time + self.time_interval
        indep = list(value_list[:4])
        indep.insert(0, self.time)
        _contours = value_list[4]
        _hist = value_list[5]
        intervals = self._sort_contourstointervals(_contours)
        colour_bins = _hist
        out = dict(zip(self.columns, list(indep) + list(colour_bins)+list(intervals)))
        self.df = self.df.append(out, ignore_index=True)
        self.bufpos += 1
       # if self.bufsize > Config['W_BUF']:
        if self.bufpos == self.bufsize:
            self._write_andreset()
    
    def _write_andreset(self):
        self.bufpos = 0
        if os.path.isfile('output/values.csv'):
            os.system('rm output/values.csv')
        os.system('touch output/values.csv')
        self._write_df()



        #Contours is a dictionary! info inc = 
    #contour is in form: 
    def _sort_contourstointervals(self, l_contour):
        l_contour.sort(key=lambda x: x[-1]) # sorts the contours with respect to center y val
        #What do we do with duplicates?
        #display in form : (num @ height, [(xval, size, radius), (xval, size, radius)])
        #Example: these ones can add to 
        s_contours = np.array(l_contour)
        contourdict = dict()
        for i in range(Config['YMAP']):
            contourdict[i] = []
        ylens = [i[-1] for i in s_contours]
        number, counts = np.unique(ylens, return_counts=True) #Get values where y is the same and how
        print(number)
        for _num, _cont in zip(number, counts):
            contourdict[_num].append(_cont)
        #many times they occur
        #NO!zipped = zip(counts, s_contours[:-1])
        for i in l_contour:
            contourdict[i[-1]].append(i[:-1])
            #That should do it? yeh probably a more susinct way with mapping?
        return contourdict.values()
        
    def print_df(self):
        print(self.df)