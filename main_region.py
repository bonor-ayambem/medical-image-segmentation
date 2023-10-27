### **Region Growing-based Segmentation with SimpleITK on MRI Head**

# Import general functions
import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt
# import gui

#### **Helper-Functions**
def sitk_show(img, output_file, title=None, margin=0.05, dpi=40):
    nda = SimpleITK.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    extent = (0, nda.shape[1]*spacing[1], nda.shape[0]*spacing[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])

    plt.set_cmap("gray")
    ax.imshow(nda,extent=extent,interpolation=None)

    if title:
        plt.title(title)

    plt.savefig(output_file)

####  **Loading DICOM files**
# Directory where the DICOM files are being stored (in this case the 'HeadMRI' folder).
pathDicom = "CT-CASE15"

# segmentation will be limited to a single 2D image (slice) but all processes are entirely applicable to the 3D image
idxSlice = 50

# int labels to assign to the segmented white and gray matter.
# These need to be different integers but their values themselves don't matter
labelWhiteMatter = 1
labelGrayMatter = 2

reader = SimpleITK.ImageSeriesReader()
filenamesDICOM = reader.GetGDCMSeriesFileNames(pathDicom)
reader.SetFileNames(filenamesDICOM)
imgOriginal = reader.Execute()

# get image size
img_array = SimpleITK.GetArrayFromImage(imgOriginal)
print(img_array.shape)

# **Note: numpy array will reverse image dimension!**

# Extract one slice
idxSlice = 50
imgSlice = imgOriginal[:,:, idxSlice]
sitk_show(imgSlice, "region1", title="one slice")

imgSmooth = SimpleITK.CurvatureFlow(image1=imgOriginal, timeStep=0.125, numberOfIterations=5)

#### **Smoothing/Denoising**

imgSmooth = SimpleITK.CurvatureFlow(image1=imgSlice, timeStep=0.125, numberOfIterations=5)

# blurFilter = SimpleITK.CurvatureFlowImageFilter()
# blurFilter.SetNumberOfIterations(5)
# blurFilter.SetTimeStep(0.125)
# imgSmooth = blurFilter.Execute(imgSlice)

sitk_show(imgSmooth, "region2", title="smoothing")


lstSeeds = [(100,75)]

# point_acquisition_interface = gui.PointDataAquisition(img_Smooth, window_level=(1050,500))
# #preselected seed point in the left ventricle  
# point_acquisition_interface.set_point_indexes([(132,142,96)])
# initial_seed_point_indexes = point_acquisition_interface.get_point_indexes()

imgWhiteMatter = SimpleITK.ConnectedThreshold(image1=imgSmooth, seedList=lstSeeds, lower=130, upper=190, replaceValue=labelWhiteMatter)

# Rescale 'imgSmooth' and cast it to an integer type to match that of 'imgWhiteMatter'
imgSmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgSmooth), imgWhiteMatter.GetPixelID())

# Use 'LabelOverlay' to overlay 'imgSmooth' and 'imgWhiteMatter'
sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgWhiteMatter), "region3")

# imgWhiteMatterNoHoles = SimpleITK.VotingBinaryHoleFilling(image1=imgWhiteMatter, radius=[2]*3, majorityThreshold=1, backgroundValue=0, foregroundValue=labelWhiteMatter)

# sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgWhiteMatterNoHoles), "region4")

# lstSeeds = [(119, 83), (198, 80), (185, 102), (164, 43)]

# imgGrayMatter = SimpleITK.ConnectedThreshold(image1=imgSmooth, seedList=lstSeeds, lower=150, upper=270, replaceValue=labelGrayMatter)

# imgGrayMatterNoHoles = SimpleITK.VotingBinaryHoleFilling(image1=imgGrayMatter, radius=[2]*3, majorityThreshold=1, backgroundValue=0, foregroundValue=labelGrayMatter)

# sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgGrayMatterNoHoles), "region5")

# #### **Merge Two Label-Fields**
# imgLabels = imgWhiteMatterNoHoles | imgGrayMatterNoHoles

# sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgLabels), "Region6")


# #### **Refine Segmentation**

# # Create image mask (boolean) containing only the common regions of the two labels
# imgMask = (imgWhiteMatterNoHoles/labelWhiteMatter) * (imgGrayMatterNoHoles/labelGrayMatter)
# print(imgMask.GetPixelIDTypeAsString())

# # transform image to UInt8 type to match
# imgMask = SimpleITK.Cast(imgMask, SimpleITK.sitkUInt8)

# # Remove common regions from WhiteMatter segment
# imgWhiteMatterNoHoles -= imgMask * labelWhiteMatter

# # Bitwise OR combination of the white matter and gray matter labels after refinement
# imgLabels = imgWhiteMatterNoHoles + imgGrayMatterNoHoles

# # Use 'LabelOverlay' to overlay 'imgSmooth' and 'imgLabels'
# sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, imgLabels), "region7")

# #### **Display Edge-Only Contours**

# sitk_show(SimpleITK.LabelOverlay(imgSmoothInt, SimpleITK.LabelContour(imgLabels)), "region8")

# # Compute statistics for imgSmooth
# LabelStatistics = SimpleITK.LabelStatisticsImageFilter()
# LabelStatistics.Execute(imgSmoothInt, SimpleITK.Cast(imgLabels, SimpleITK.sitkInt8))
# count_pixel = LabelStatistics.GetCount(1)
# img_mean = LabelStatistics.GetMean(1)
# img_var = LabelStatistics.GetVariance(1)
# img_max = LabelStatistics.GetMaximum(1)
# img_min = LabelStatistics.GetMinimum(1)

# import tabulate
# from tabulate import tabulate
# print(tabulate([['Count', count_pixel], ['Mean', img_mean], 
#                 ['Variance', img_var], ['Max', img_max], ['Min', img_min]],
#                 headers=['Name', 'Value'], tablefmt='orgtbl', numalign='left'))

# #### **Save Results**
# # save segmentation result to file
# SimpleITK.WriteImage(imgLabels, "MRIsegLabels.mhd")
