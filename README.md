# Segmentation of Lungs and Airways from CT Scan

## Purpose

The purpose of this project is to compare different segmentation techniques
for CT Scan of Lungs and Airways.

Image segmentation involves dividing an image into continuous regions or sets 
of pixels/voxels.

## Project Description

The segmentation methods implemented are hybrid segmentation and region growing.

Region-based segmentation is a process in image processing and computer vision that
involves dividing an image into meaningful and coherent regions or objects.
These regions are typically composed of pixels or voxels that share similar properties,
such as intensity, color, or texture.

Hybrid segmentation is an approach to image segmentation that combines multiple 
segmentation methods or techniques to improve the accuracy and robustness of the 
segmentation results.

Both of these methods are carried out on dicom files for a
high-resolution CT image.
The CT image given is single subject but saved slice by slice in DICOM format 
(where each slice is 2D). 

## Usage

### For Hybrid Segmentation
* Begin by running the following python commands in a terminal:
  ```
  pip install -q pydicom  # -q means quiet
  pip install -q scikit-image
  ```
  These install the necessary packages to our project:
    * pydicom -> for reading dcm image formats
    * skimage -> for image processing functions
* Run `python main_hybrid.py`

### For Region Growing
* Begin by running the following python commands in a terminal:
  ```
  pip install -q SimpleITK  # -q means quiet
  pip install -q tabulate
  ```
  These install the necessary packages to our project:
    * SimpleITK > for medical image segmentation and registration
    * 
* Run `python main_region.py`

## Test Run

* Dowload data of a CT scan as .dicom files and import them to the project directory
* Run `python main_hybrid.py` and `python main_region.py` to run hybrid segmentation and 
region-growing respectievly on the image data
* Results are generated in .png files located in the project directory
* For this example, the CT scan use is CT-CASE15

## Author

### Bonor Ayambem

Github - @bonor-ayambem
