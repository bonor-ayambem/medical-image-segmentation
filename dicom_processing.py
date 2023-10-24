import pydicom
import os
import numpy as np
from glob import glob

data_path = "CT-CASE15"
g = glob(data_path + '/*')

# Print out the first 5 file names to verify we're in the right folder.
print("Total of %d DICOM images.\nFirst 5 filenames:" % len(g))
print('\n'.join(g[:5]))

# Load medical image slices from 'path' directory, and return them in 'slices'
def load_scan(path):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices

# Loop over the image files and store everything into a list.
def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans], axis=-1)
    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -3000] = 0

    # Convert to Hounsfield units (HU)
    # The rescale slope and rescale intercept allow to transform the pixel values to HU or other units
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope

    # Pixel -> HU: slope * x + intercept
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)

    return np.array(image, dtype=np.int16)

patient = load_scan(data_path)
img = get_pixels_hu(patient)

