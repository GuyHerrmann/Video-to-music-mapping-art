import pytest
from videoHandler import Video
from config import Config
from image_processing import process
from writingdata import writeData

@pytest.fixture
def cfig():
    return Config
#Can set different configurations

@pytest.fixture
def frame():
    v = Video('Video/1min.mp4')
    return next(v)

#def test_processing(frame):
#    vals = process(frame)
#    assert len(vals) == 6

    



def test_videoHandler_works(cfig):
    v = Video('Video/1min10.mp4')
    for vid, _ in zip(v, range(2)):
        assert vid.shape == (cfig['XDIM'], cfig['YDIM'])

def test_videoHandler_fail(cfig):
    v = Video('Video/sloth')
    try : 
        next(v)
    except :
        assert True
    else:
        assert True == False

@pytest.fixture
def vid_obj():
    v = Video('Video/1min10.mp4')
    return v

def test_get_framerate(vid_obj):
    fps = vid_obj.ret_FrameRate()
    assert int(fps) == 10

def test_write(vid_obj):
    #create write obj:
    writedata = writeData('Tests/test.csv', 2)
    for i, _ in zip(vid_obj, range(5)):
        processed = process(i)
        writedata.add_new(processed)
    writedata.print_df()
    
    