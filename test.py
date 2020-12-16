import pytest
from videoHandler import Video
from config import Config

@pytest.fixture
def cfig():
    return Config
#Can set different configurations

@pytest.fixture
def frame():
    v = Video('Video/1min.mp4')
    return next(v)
    



def test_videoHandler_works(cfig):
    v = Video('Video/1min.mp4')
    for vid, _ in zip(v, range(2)):
        assert vid.shape == (cfig['XDIM'], cfig['YDIM'])

def test_videoHandler_fail(cfig):
    fail = False
    try:
         v = Video('Video/sloth')
    except:
        fail = True
    assert fail == True

def ret_frame():
    v = Video('Video/1min.mp4')
    return next(v)
    