from pathlib import Path
from typing import List, Tuple

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

from .config import settings
from .errors import HeightWidthMismatchError, validate_height_width


def compute_channels_mean(image: np.ndarray) -> Tuple[float, float, float]:
    """Compute the mean over each channels of an RGB images.
    Args:
        image (np.ndarray): The image, as a np.array, for which you want to compute the means.
    Returns:
        Tuple[float, float, float]: The RGB means.
    """

    red_mean_value = image[:, :, 0].mean()
    green_mean_value = image[:, :, 1].mean()
    blue_mean_value = image[:, :, 2].mean()

    return red_mean_value, green_mean_value, blue_mean_value


def compute_channels_std(image: np.ndarray) -> Tuple[float, float, float]:
    """Compute the standard deviation over each channels of an RGB images.
    Args:
        image (np.ndarray): The image, as a np.array, for which you want to compute the stds.
    Returns:
        Tuple[float, float, float]: The RGB stds.
    """

    red_std_value = image[:, :, 0].std()
    green_std_value = image[:, :, 1].std()
    blue_std_value = image[:, :, 2].std()

    return red_std_value, green_std_value, blue_std_value


def compute_histograms_channels(
        image: np.ndarray,
        filename: str,
        timestamp: str,
) -> Path:
    """Compute the channels normed histograms of an image.
    The bins of the histograms are all of width 1, meaning that the normed histogram here defines a
    Probability mass function on each channels, i.e. the sum of all values for each channels is equal to 1.
    See the following [StackOverflow post](https://stackoverflow.com/questions/21532667/numpy-histogram-cumulative-density-does-not-sum-to-1).
    Args:
        image (np.ndarray): The image, as a np.array, for which you want to compute the channels normed histograms.
        filename (str): The name of the image file.
        timestamp (str): The timestamp at which the endpoint has been called.
    Returns:
        Path: The path to the histogram.
    """
    colors = ("red", "green", "blue")
    channel_ids = (0, 1, 2)

    pixel_range_value = 255
    bins = np.arange(0, pixel_range_value)

    # create the histogram plot, with three lines, one for
    # each color
    plt.figure()
    plt.xlim([0, pixel_range_value])
    for channel_id, color in zip(channel_ids, colors):
        histogram, bin_edges = np.histogram(
            image[:, :, channel_id],
            bins=bins,
            range=(0, pixel_range_value),
            density=True,
        )
        plt.plot(bin_edges[0:-1], histogram, color=color)

    plt.title(f"Color Histogram of {filename}")
    plt.xlabel("Color value")
    plt.ylabel("Pixel density")

    saved_image_path = Path(
        f"{settings.histograms_dir}/{filename}_{timestamp}.png",
    ).resolve()

    plt.savefig(saved_image_path)

    return saved_image_path


def compute_mean_image(images_list: List[np.ndarray], timestamp: str) -> Path:
    """Compute the mean image of an image dataset.
    Args:
        images_list (List[np.ndarray]): The image dataset on which you compute the mean image.
        timestamp (str): The timestamp at which the endpoint has been called.
    Returns:
        Path: The path to the mean image.
    """
    # Assuming all images are the same size, get dimensions of first image
    height, width, _ = images_list[0].shape

    try:
        validate_height_width(images_list=images_list)
    except HeightWidthMismatchError as err:
        raise err

    num_images = len(images_list)

    # Create a numpy array of floats to store the average (assume RGB images)
    arr = np.zeros((height, width, 3), dtype=np.float32)

    # Build up average pixel intensities
    arr = sum(images_list) / num_images

    # Round values in array and cast as 8-bit integer
    arr = np.array(np.round(arr), dtype=np.uint8)

    # Generate, save final image
    out = Image.fromarray(arr, mode="RGB")

    saved_image_path = Path(
        f"{settings.mean_image_dir}/average_{timestamp}.png",
    ).resolve()

    out.save(saved_image_path)

    return saved_image_path


def compute_scatterplot(images_paths: List[Path], timestamp: str) -> Path:
    """Compute the mean vs std scatterplot of an image dataset.
    Args:
        images_list (List[np.ndarray]): The image dataset on which you compute the mean vs std scatterplot.
        timestamp (str): The timestamp at which the endpoint has been called.
    Returns:
        Path: The path to the scatterplot.
    """

    # colors = ("red", "green", "blue")
    # channel_ids = (0, 1, 2)

    images_labels = [Path(image_path).parent.stem for image_path in images_paths]
    labels_dict = {label: idx for idx, label in enumerate(sorted(set(images_labels)))}
    tags = [labels_dict[image_label] for image_label in images_labels]

    images_list = [
        np.array(Image.open(image), dtype=np.float32) / 255 for image in images_paths
    ]

    # defines placeholders for subplots
    fig, (ax1, ax2, ax3) = plt.subplots(
        nrows=1,
        ncols=3,
        sharex='True',
        sharey='True',
        figsize=(20, 15),
    )
    fig.suptitle("Mean-std scatterplot. Pixel values in [0,1]")
    # fig = plt.figure(figsize=(20, 15))
    # ax1 = fig.add_subplot(131)
    # ax2 = fig.add_subplot(132)
    # ax3 = fig.add_subplot(133)

    # compute means-stds for each subplots
    r_means = [compute_channels_mean(image)[0] for image in images_list]
    r_stds = [compute_channels_std(image)[0] for image in images_list]

    g_means = [compute_channels_mean(image)[1] for image in images_list]
    g_stds = [compute_channels_std(image)[1] for image in images_list]

    b_means = [compute_channels_mean(image)[2] for image in images_list]
    b_stds = [compute_channels_std(image)[2] for image in images_list]

    N = len(set(images_labels))

    # define the colormap
    cmap = plt.cm.jet
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # create the new map
    cmap = cmap.from_list("Custom cmap", cmaplist, cmap.N)

    # populate subplots
    ax1.scatter(r_means, r_stds, c=tags, alpha=0.5, cmap=cmap)
    ax2.scatter(g_means, g_stds, c=tags, alpha=0.5, cmap=cmap)
    ax3.scatter(b_means, b_stds, c=tags, alpha=0.5, cmap=cmap)

    ax1.set_title("red channel")
    ax1.set_xlabel("means")
    ax1.set_ylabel("stds")

    ax2.set_title("green channel")
    ax2.set_xlabel("means")
    ax2.set_ylabel("stds")

    ax3.set_title("blue channel")
    ax3.set_xlabel("means")
    ax3.set_ylabel("stds")

    handles, labels = ax3.get_legend_handles_labels()
    fig.legend(
        handles=handles,
        labels=labels,
        loc="upper left",
    )

    # for channel, color in zip(channel_ids, colors):
    #     means = [compute_channels_mean(image)[channel] for image in images_list]
    #     stds = [compute_channels_std(image)[channel] for image in images_list]

    # plt.scatter(means, stds, c=color, alpha=0.5)

    # plt.title("Mean-std scatterplot. Pixel values in [0,1]")
    # plt.xlabel("means")
    # plt.ylabel("stds")

    saved_image_path = Path(
        f"{settings.scatterplots_dir}/scatter_{timestamp}.png",
    ).resolve()

    plt.savefig(saved_image_path)

    return saved_image_path

from sklearn.decomposition import PCA
from math import ceil

def eigenimages(full_mat, title, n_comp = 0.7, size = (64, 64)):
    # fit PCA to describe n_comp * variability in the class
    pca = PCA(n_components = n_comp, whiten = True)
    pca.fit(full_mat)
    print('Number of PC: ', pca.n_components_)
    return pca

def plot_pca(pca, size = (64, 64)):
    # plot eigenimages in a grid
    n = pca.n_components_
    fig = plt.figure(figsize=(8, 8))
    r = int(n**.5)
    c = ceil(n/ r)
    for i in range(n):
        ax = fig.add_subplot(r, c, i + 1, xticks = [], yticks = [])
        ax.imshow(pca.components_[i].reshape(size),
                  cmap='Greys_r')
    plt.axis('off')
    plt.show()

# plot_pca(eigenimages(normal_images, 'NORMAL'))
# plot_pca(eigenimages(pnemonia_images, 'PNEUMONIA'))

# contrast_mean = norm_mean - pneu_mean
# plt.imshow(contrast_mean, cmap='bwr')
# plt.title(f'Difference Between Normal & Pneumonia Average')
# plt.axis('off')
# plt.show()
