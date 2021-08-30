# Change Logs

# [v0.1.3] Aug 20, 2021

## Added

- [x] Add a capability to normalize sampled 3D points to [-1, 1] without using NDC
      Need to give center_3dpoints and scale factor as the arguments when calling the dataset class
- [x] Add scale to test_dataloader.py.
- [x] Add docker scripts
- [] Add training script for real-world data

## Changed

- [x] --no_NDC to --ray_to_NDC
- [x] Set far distance to be at most 10 m

# [v0.1.2] Aug 13, 2021

## Changes

- [x] Upgrade pytorch-lightning to 1.4.2 to match with torch 1.9.0

# [v0.1.1] Aug 11, 2021

## Changes

- [x] Upgrade pytorch, torch vision to 1.9.0 and 0.10.0
