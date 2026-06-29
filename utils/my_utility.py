
import numpy as np
from skimage import measure, filters

def detect_hotspots(image, threshold=150):
    """
    Detect regions with intensity above a threshold.

    Parameters:
        image (ndarray): Grayscale image.
        threshold (int): Intensity threshold.

    Returns:
        list: Region properties (area, mean intensity, total count)
    """
    binary = image > threshold
    labeled = measure.label(binary)
    regions = measure.regionprops(labeled, intensity_image=image)

    results = []
    for region in regions:
        results.append({
            'area': region.area,
            'mean_intensity': region.mean_intensity,
            'total_count': region.intensity_image[region.image].sum()
        })
    return results

def compute_texture_features(image):
    """
    Compute texture features using standard deviation in local windows.

    Parameters:
        image (ndarray): Grayscale image.

    Returns:
        dict: Global texture metrics.
    """
    std_image = filters.rank.standard_deviation(image.astype(np.uint8), np.ones((9, 9)))
    return {
        'texture_std_mean': np.mean(std_image),
        'texture_std_max': np.max(std_image),
        'texture_std_min': np.min(std_image)
    }

def analyze_intensity_profile(image, axis=0):
    """
    Analyze intensity profile along a given axis (0=rows, 1=columns).

    Parameters:
        image (ndarray): Grayscale image.
        axis (int): Axis along which to compute mean intensity.

    Returns:
        ndarray: 1D intensity profile.
    """
    return np.mean(image, axis=axis)
