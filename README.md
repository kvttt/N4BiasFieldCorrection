N4BiasFieldCorrection
=====================

This simple program is based on [SimpleITK](https://github.com/SimpleITK/SimpleITK) 
and performs N4 bias field correction on a 3D volume.

Dependencies
------------
* SimpleITK

Usage
-----
For a 3D volume saved as a NIfTI file `./input.nii`, the following script saves the bias field corrected volume as a NIfTI file `./output.nii` 
whose filename is specified by `--output` or `-o`.

    python N4.py -i ./input.nii -o ./output.nii

A mask can be specified using `--mask_file` or `-m`. If unspecified, 
a mask will be automatically generated using Otsu's method. 
Note the specified mask should be of the same shape as the input volume.

To specify the number of iterations to perform, use `--iterations` or `-n`.
More iterations yield better result but also takes longer to run.
