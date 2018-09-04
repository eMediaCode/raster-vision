import unittest
import numpy as np

from rastervision.core.raster_source import RasterSource
from rastervision.core.box import Box
from rastervision.label_stores.segmentation_raster_file import (
    SegmentationInputRasterFile)


class TestingRasterSource(RasterSource):
    def __init__(self, zeros=False, data=None):
        if data is not None:
            self.data = data
            (self.height, self.width, self.channels) = data.shape
        elif zeros and data is None:
            self.width = 4
            self.height = 4
            self.channels = 3
            self.data = np.zeros(
                (self.height, self.width, self.channels), dtype=np.uint8)
        elif not zeros and data is None:
            self.width = 4
            self.height = 4
            self.channels = 3
            self.data = np.random.randint(
                0,
                2,
                size=(self.width, self.height, self.channels),
                dtype=np.uint8)
            self.data[:, :, 0:(self.channels - 1)] = np.zeros(
                (self.height, self.width, self.channels - 1), dtype=np.uint8)

    def get_extent(self):
        return Box(0, 0, self.height, self.width)

    def _get_chip(self, window):
        ymin = window.ymin
        xmin = window.xmin
        ymax = window.ymax
        xmax = window.xmax
        return self.data[ymin:ymax, xmin:xmax, :]

    def get_chip(self, window):
        return self.get_chip(window)

    def get_crs_transformer(self, window):
        return None


class TestSegmentationRasterFile(unittest.TestCase):
    def test_interesting_subwindow(self):
        zeros = np.zeros((11, 11, 3), dtype=np.uint8)
        ones = np.ones((10, 10, 3), dtype=np.uint8)
        zeros[1:, 1:, :] = ones
        raster_source = TestingRasterSource(data=zeros)
        label_store = SegmentationInputRasterFile(
            source=raster_source,
            raster_class_map={'#010101': 1})
        extent = Box(0, 0, 10, 10)
        window = label_store.interesting_subwindow(extent, 2, 0)
        self.assertEqual(window.xmin, 1)
        self.assertEqual(window.ymin, 1)
        self.assertEqual(window.xmax, 3)
        self.assertEqual(window.ymax, 3)


if __name__ == '__main__':
    unittest.main()
