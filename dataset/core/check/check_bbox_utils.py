from __future__ import print_function
from __future__ import unicode_literals

"""All bbox in this file assumed (x, y, w, h), x rightward, y downward"""


class BBox(object):
    def __init__(self, bbox):
        self.x = bbox[0]
        self.y = bbox[1]
        self.w = bbox[2]
        self.h = bbox[3]

    def get_bbox(self):
        return [self.x, self.y, self.w, self.h]

    def __getitem__(self, key):
        return self.get_bbox()[key]


def check_intersect_range(x1, l1, x2, l2):
    if x1 > x2:
        x1, x2 = x2, x1
        l1, l2 = l2, l1
    return (x1+l1) > x2


def check_intersect_vertical_proj(bbox1, bbox2):
    '''Projection vertically intersected?'''
    return check_intersect_range(bbox1[0], bbox1[2], bbox2[0], bbox2[2])


def check_intersect_horizontal_proj(bbox1, bbox2):
    '''Projection horizontally intersected?'''
    return check_intersect_range(bbox1[1], bbox1[3], bbox2[1], bbox2[3])


def check_intersect_bbox(bbox1, bbox2):
    return check_intersect_horizontal_proj(bbox1, bbox2) and\
        check_intersect_vertical_proj(bbox1, bbox2)


def get_intersect_range(x1, l1, x2, l2):
    '''Get the length of the intersection range'''
    if x1 > x2:
        x1, x2 = x2, x1
        l1, l2 = l2, l1
    if not check_intersect_range(x1, l1, x2, l2):
        return 0
    if (x1 + l1) > (x2+l2):
        return l2
    else:
        return x1 + l1 - x2


def check_bbox_contains_each_other(bbox1, bbox2):
    """Get the bigger box be the first box"""
    if bbox1[2]* bbox1[3] < bbox2[2]*bbox2[3]:
        bbox2, bbox1 = bbox1, bbox2
    if bbox2[1] < bbox1[1] - bbox1[3]*0.1:
        return False
    if (bbox1[0] + bbox1[2] > bbox2[0] + bbox2[2]) and (bbox1[1] + bbox1[3] > bbox2[1] + bbox2[3]):
        return True
    return False


def check_bbox_almost_contains_each_other(bbox1, bbox2):
    if bbox1[2] * bbox1[3] < bbox2[2] * bbox2[3]:
        bbox2, bbox1 = bbox1, bbox2
    if bbox2[1] < bbox1[1] - bbox1[3]*0.2:
        return False
    if get_intersect_range_vertical_proj(
        bbox1, bbox2
    ) * get_intersect_range_horizontal_proj(bbox1, bbox2) > 0.8*bbox2[2] * bbox2[3]:
        return True
    return False


def get_intersect_range_horizontal_proj(bbox1, bbox2):
    return get_intersect_range(bbox1[1], bbox1[3], bbox2[1], bbox2[3])


def get_intersect_range_vertical_proj(bbox1, bbox2):
    return get_intersect_range(bbox1[0], bbox1[2], bbox2[0], bbox2[2])


def get_min_bbox_contains_all(bbox_list):
    if bbox_list is None or len(bbox_list) == 0:
        return None
    bbox_x = min(bbox[0] for bbox in bbox_list)
    bbox_y = min(bbox[1] for bbox in bbox_list)
    bbox_x_end = max(bbox[0]+bbox[2] for bbox in bbox_list)
    bbox_y_end = max(bbox[1]+bbox[3] for bbox in bbox_list)
    return (bbox_x, bbox_y, bbox_x_end-bbox_x, bbox_y_end-bbox_y)


def convert_to_param_format(bbox_list):
    new_bbox_list = list([BBox(bbox) for bbox in bbox_list])
    return new_bbox_list