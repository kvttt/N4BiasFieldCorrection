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
The default number of iterations is 50.

Use `--get_bias_field` or `-b` 
to save the estimated bias field as a NIfTI file under the same directory as the output file.

Use `--get_mask` or `-k`
to save the generated/specified mask as a NIfTI file under the same directory as the output file.

To enable progress reporting, use `--verbose` or `-v` (only works with SimpleITK 2.3.0 or later).
To install the latest pre-release version of SimpleITK, run the following command in a terminal:

    pip install --upgrade --pre SimpleITK --find-links https://github.com/SimpleITK/SimpleITK/releases/tag/latest
