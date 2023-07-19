import argparse

import SimpleITK as sitk

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', '-i', type=str, required=True, help='path to the input file')
parser.add_argument('--mask_file', '-m', type=str, default=None, help='path to the mask file')
parser.add_argument('--output_file', '-o', type=str, required=True, help='path to the output file')
parser.add_argument('--shrink_factor', '-s', type=int, default=1, help='shrink factor (default = 1)')
parser.add_argument('--iterations', '-n', type=int, default=1, help='number of iterations (default = 1)')
parser.add_argument('--levels', '-l', type=int, default=4, help='number of fitting levels (default = 4)')
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

# Setup corrector
corrector = sitk.N4BiasFieldCorrectionImageFilter()
levels = int(args.levels)
assert levels > 0, 'Number of fitting levels must be positive.'

iterations = int(args.iterations)
assert iterations > 0, 'Number of iterations must be positive.'

corrector.SetMaximumNumberOfIterations([iterations] * levels)

# Correct image
output = corrector.Execute(image, mask)
log_bias_field = corrector.GetLogBiasFieldAsImage(image)
output_full_res = image / sitk.Exp(log_bias_field)

# Save output
if shrink_factor > 1:
    sitk.WriteImage(output, args.output_file)
elif shrink_factor == 1:
    sitk.WriteImage(output_full_res, args.output_file)

print(f'Saved corrected image to {args.output_file}.')
