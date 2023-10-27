from scipy import ndimage
import nibabel as nib
import numpy as np
from nilearn import plotting
from nilearn.image import threshold_img
from nilearn.image import load_img, math_img
import matplotlib.pyplot as plt


from glob import glob

import dicom_processing
import hybrid_seg

data_path = "CT-CASE15"
g = glob(data_path + '/*')

# Print out the first 5 file names to verify we're in the right folder.
print("Total of %d DICOM images.\nFirst 5 filenames:" % len(g))
print('\n'.join(g[:5]))

patient = dicom_processing.load_scan(data_path)
img = dicom_processing.get_pixels_hu(patient)

# Check data shape
# img_new = img.transpose(2, 0, 1).  # transform data dimensions from xyz to zxy
img_new = ndimage.rotate(img, -90, reshape=False)
img_new.shape

# Displaying an Image Stack
# transform data into nii format
img_nii = nib.Nifti1Image(img_new, affine=np.eye(4))
# save nii file
# nib.save(img_nii, "nifty_img.nii")
# nii_filename = "nifty_img.nii"
# Visualize slices
plotting.plot_anat(img_nii, display_mode= 'z', cut_coords=range(0, 139, 10), title='Slices', output_file='image_stack.png')

# Create a histogram of all the voxel data.

img_to_process = img_new.astype(np.float64)

plt.hist(img_to_process.flatten(), bins=50, color='c')
plt.xlabel("Hounsfield Units (HU)")
plt.ylabel("Frequency")
plt.savefig("vox_histogram")




# print("Shape before resampling\t", img_to_process.shape)
img_after_resamp, spacing = hybrid_seg.resample(img_to_process, patient, [1,1,1])
# print("Shape after resampling\t", img_after_resamp.shape)


# single slice example at each step
img_target = ndimage.rotate(img_after_resamp, 180, reshape=False)

img_target = img_target.transpose(2,1,0)

fiber = img_target[260]
hybrid_seg.make_lungmask(fiber, display=True)

# does global and percentile count as two?
# does mine look right?
# what do you mean by "conduct a comprehensive analysis of
# the results," 