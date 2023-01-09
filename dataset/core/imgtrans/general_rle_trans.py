'''
RLE: Run-Length Encode
'''
#!--*-- coding: utf- --*--
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# M1:
class general_rle(object):
    '''
    ref.: https://www.kaggle.com/stainsby/fast-tested-rle
    '''
    def __init__(self):
        pass


    def rle_encode(self, binary_mask):
        pixels = binary_mask.flatten()
        # We avoid issues with '1' at the start or end (at the corners of
        # the original image) by setting those pixels to '0' explicitly.
        # We do not expect these to be non-zero for an accurate mask,
        # so this should not harm the score.
        pixels[0] = 0
        pixels[-1] = 0
        runs = np.where(pixels[1:] != pixels[:-1])[0] + 2
        runs[1::2] = runs[1::2] - runs[:-1:2]
        return runs


    def rle_to_string(self, runs):
        return ' '.join(str(x) for x in runs)


    def check(self):
        test_mask = np.asarray([[0, 0, 0, 0],
                                [0, 0, 1, 1],
                                [0, 0, 1, 1],
                                [0, 0, 0, 0]])
        assert rle_to_string(rle_encode(test_mask)) == '7 2 11 2'


# M2:
class binary_mask_rle(object):
    '''
    ref.: https://www.kaggle.com/paulorzp/run-length-encode-and-decode
    '''
    def __init__(self):
        pass

    def rle_encode(self, binary_mask):
        '''
        binary_mask: numpy array, 1 - mask, 0 - background
        Returns run length as string formated
        '''
        pixels = binary_mask.flatten()
        pixels = np.concatenate([[0], pixels, [0]])
        runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
        runs[1::2] -= runs[::2]
        return ' '.join(str(x) for x in runs)


    def rle_decode(self, mask_rle, shape):
        '''
        mask_rle: run-length as string formated (start length)
        shape: (height,width) of array to return
        Returns numpy array, 1 - mask, 0 - background
        '''
        s = mask_rle.split()
        starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
        starts -= 1
        ends = starts + lengths
        binary_mask = np.zeros(shape[0] * shape[1], dtype=np.uint8)
        for lo, hi in zip(starts, ends):
            binary_mask[lo:hi] = 1
        return binary_mask.reshape(shape)

    def check(self):
        maskfile = '/path/to/test.png'
        mask = np.array(Image.open(maskfile))
        binary_mask = mask.copy()
        binary_mask[binary_mask <= 127] = 0
        binary_mask[binary_mask > 127] = 1

        # encode
        rle_mask = self.rle_encode(binary_mask)

        # decode
        binary_mask2 = self.rle_decode(rle_mask, binary_mask.shape[:2])

