from typing import List

import numpy as np


class DimensionError(ValueError):
    """_summary_
    Args:
        ValueError (_type_): _description_
    """


class HeightWidthMismatchError(DimensionError):
    """_summary_
    Args:
        DimensionError (_type_): _description_
    """


class ChannelNotFoundError(DimensionError):
    """_summary_
    Args:
        DimensionError (_type_): _description_
    """


def validate_height_width(
    images_list: List[np.ndarray],
) -> None:
    height, width, _ = images_list[0].shape

    for idx in range(1, len(images_list)):
        img_height, img_width, _ = images_list[idx].shape
        if img_height - height != 0:
            raise HeightWidthMismatchError(img_height, height)
        elif img_width - width != 0:
            raise HeightWidthMismatchError(img_width, width)