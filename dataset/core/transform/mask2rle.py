
import cv2

def mask2rle(mask):
    """
    img: numpy array, 1 - mask, 0 - background
    Returns run length as string formated
    """
    mask = cp.array(mask)
    pixels = mask.flatten()
    pad = cp.array([0])
    pixels = cp.concatenate([pad, pixels, pad])
    runs = cp.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]

    return " ".join(str(x) for x in runs)


def masks2rles(masks, ids, heights, widths):
    pred_strings = []
    pred_ids = []
    pred_classes = []

    for idx in range(masks.shape[0]):
        height = heights[idx].item()
        width = widths[idx].item()
        mask = cv2.resize(masks[idx], dsize=(width, height), interpolation=cv2.INTER_NEAREST)  # back to original shape

        rle = [None] * 3
        for midx in [0, 1, 2]:
            rle[midx] = mask2rle(mask[..., midx])

        pred_strings.extend(rle)
        pred_ids.extend([ids[idx]] * len(rle))
        pred_classes.extend(["large_bowel", "small_bowel", "stomach"])

    return pred_strings, pred_ids, pred_classes