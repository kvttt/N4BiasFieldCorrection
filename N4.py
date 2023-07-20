import argparse
from packaging import version

import SimpleITK as sitk


def command_iteration(filter: sitk.N4BiasFieldCorrectionImageFilter):
    print('------------------------------------')
    print(f'Level = {filter.GetCurrentLevel()} | Iteration = {filter.GetElapsedIterations()} | '
          f'Lambda = {filter.GetCurrentConvergenceMeasurement()} ')


parser = argparse.ArgumentParser()
parser.add_argument('--input_file', '-i', type=str, required=True, help='path to the input file')
parser.add_argument('--mask_file', '-m', type=str, default=None, help='path to the mask file')
parser.add_argument('--output_file', '-o', type=str, required=True, help='path to the output file')
parser.add_argument('--shrink_factor', '-s', type=int, default=1, help='shrink factor (default = 1)')
parser.add_argument('--iterations', '-n', type=int, default=50, help='number of iterations (default = 50)')
parser.add_argument('--levels', '-l', type=int, default=4, help='number of fitting levels (default = 4)')
parser.add_argument('--get_bias_field', '-b', action='store_true', help='save bias field')
parser.add_argument('--get_mask', '-k', action='store_true', help='save mask')
parser.add_argument('--verbose', '-v', action='store_true', help='display progress')
args = parser.parse_args()

# Load input file
image = sitk.ReadImage(args.input_file, sitk.sitkFloat32)

# Load mask file
if args.mask_file is not None:
    mask = sitk.ReadImage(args.mask_file, sitk.sitkUInt8)
else:
    mask = sitk.OtsuThreshold(image, 0, 1, 200)

# Resample image
shrink_factor = int(args.shrink_factor)
assert shrink_factor > 0, 'Shrink factor must be positive.'
if shrink_factor > 1:
    image = sitk.Shrink(
        image,
        [shrink_factor] * image.GetDimension()
    )
    mask = sitk.Shrink(
        mask,
        [shrink_factor] * mask.GetDimension()
    )

# Save mask
if args.get_mask:
    sitk.WriteImage(mask, args.output_file.replace('.nii.gz', '_mask.nii.gz'))
    print(f'Saved mask to {args.output_file.replace(".nii.gz", "_mask.nii.gz")}.')

# Setup corrector
corrector = sitk.N4BiasFieldCorrectionImageFilter()

# Setup iterations
levels = int(args.levels)
assert levels > 0, 'Number of fitting levels must be positive.'

iterations = int(args.iterations)
assert iterations > 0, 'Number of iterations must be positive.'

corrector.SetMaximumNumberOfIterations([iterations] * levels)

# Setup reporting
if args.verbose:
    if version.parse(sitk.__version__) >= version.parse('2.3.0rc1.post24'):
        corrector.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(corrector))

    else:
        print('Warning: Progress reporting requires SimpleITK version 2.3.0 or later. '
              f'Current version: {sitk.__version__}. '
              'Progress will not be reported.')

# Correct image
output = corrector.Execute(image, mask)
log_bias_field = corrector.GetLogBiasFieldAsImage(image)
output_full_res = image / sitk.Exp(log_bias_field)

# Save bias field
if args.get_bias_field:
    sitk.WriteImage(log_bias_field, args.output_file.replace('.nii.gz', '_bias_field.nii.gz'))

print(f'Saved bias field to {args.output_file.replace(".nii.gz", "_bias_field.nii.gz")}.')

# Save output
if shrink_factor > 1:
    sitk.WriteImage(output, args.output_file)
elif shrink_factor == 1:
    sitk.WriteImage(output_full_res, args.output_file)

print(f'Saved corrected image to {args.output_file}.')
