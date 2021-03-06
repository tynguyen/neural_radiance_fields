[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
<img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white" />

# NeRF Simplification

This repo contains simple implementations of NeRF models packaged to ready-to-use modules which can be installed using `pip install`.

---

# Structure

- notebooks: ipython notebooks that introduces NERF
- nerf_pl: a Pytorch implementation that supports custom datasets

# Build and Install Using Poetry

## Build a Wheel Locally

```
cd neural_radiance_fields
poetry init
```

Convert requirements packages given in requirements.txt format to poetry format

```
cat nerf_pl/requirements.txt | perl -pe 's/([<=>]+)/:$1/' | xargs -t -n 1 -I {} poetry add '{}'
```

Add torchsearchsorted to the dependence list by inserting the following line to pyproject.toml

```
torchsearchsorted = {git = "https://github.com/aliutkus/torchsearchsorted.git", rev = "1e0ffc3e0663ffda318b4e28348efd90313d08f3"}
```

Then refresh the dependence list

```
poetry lock
```

Then build the package

```
cd neural_radiance_fields
poetry build
```

## Install Using the built Wheel

```
pip install dist/nerf_pl-0.1.0-py3-none-any.whl
```

## Test

```
cd neural_radiance_fields
poetry run pytest tests
```

## (Optional) Publish to TestPyPi

This is not working due to the dependence on torchsearchsorted package.

```
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi
```

---

# Getting started

## Simple Ipython Notebooks

-[x] notebooks

## Prepare Data

In here, we use dataset `replica/room_0_array` that can be found from [this link](https://drive.google.com/drive/folders/1N1F80da4fqulprZgfi-i5WLAkQwET6SG?usp=sharing).
After obtaining RGBDS from the soundspace simulation, we need to use colmap to reconstruct the environment. Note that the data given by the above link already include the reconstructed environment so you can skip the following steps.

To do this, for example with new data, first move the data to
`~/github_ws/neural_radiance_fields/nerf_pl/data/replica/room_0_array` such that this folder contains

```
|_audios
|_depths
|_images
|_map
|_rirs
```

And then run the following commands to create a docker container.

```
cd docker
source my_docker_env.sh
bash create_container.sh -v ~/github_ws
```

Inside the docker,

```
cd ~/github_ws/neural_radiance_fields/nerf_pl/LLFF
python imgs2poses.py ../data/replica/room_0_array/ --map_file_ext .bin
```

After these steps, we will get the following datas structure

```
|_audios
|_depths
|_images
|_map
|_rirs
|_colmap_output.txt: not important
|_database.db: not important file. Can ignore
|_poses_bounds.npy: important file, will be used for visual NeRF
```

Note that the outcome of colmap has NO SCALE information.

## Verify DataLoader

To test the dataloader, you can run

```
cd ~/github_ws/neural_radiance_fields/nerf_pl
python test_dataloader.py --test_name step_2
python test_dataloader.py --test_name step_3
```

You should expect two figures shown in `assets` of this repo.
![step2](assets/expected_result_test_step_2.png)
![step3](assets/expected_result_test_step_3.png)

Note that this test is specific to the data given above (replica/room_0_array) with 9 poses because we hardcoded the scale factor as well as the link to the dataset.

## Train the model

A script example to train the model can be found at `nerf_pl/scripts`.

```
ROOT_DIR="data/replica/room_0_array"
# directory containing the data
IMG_W=640  # image width (do not set too large)
IMG_H=360  # image height (do not set too large)
NUM_EPOCHS=30  # number of epochs to train (depending on how many images there are,
# 20~30 might be enough)
EXP="replica_room_0_array"  # name of the experience (arbitrary)

# Normalize the sampled 3D points to the unit sphere without using NDC
NORMALIZE_SAMPLED_POINTS="True"
RAY_TO_NDC="False"
python3 train.py \
   --dataset_name llff \
   --root_dir "$ROOT_DIR" \
   --N_importance 64 --img_wh $IMG_W $IMG_H \
   --num_epochs $NUM_EPOCHS --batch_size 1024 \
   --optimizer adam --lr 5e-4 \
   --normalize_sampled_points $NORMALIZE_SAMPLED_POINTS\
   --ray_to_NDC $RAY_TO_NDC\
   --lr_scheduler cosine \
   --exp_name $EXP
```

There are two ways to convert coordinates of sampled 3D points to [-1, 1].

- Use NDC

```
NORMALIZE_SAMPLED_POINTS="False"
RAY_TO_NDC="True"
```

Only Z would be in [-1, 1].

- Use scaling and shifting

```
NORMALIZE_SAMPLED_POINTS="True"
CENTER_3DPOINTS=-0.0028,0.0005,-0.3630 # center of 3D points after scaling
RAYS_SCALE_FACTOR=0.065 # Scaling factor to ensure 3D points' coordinates are within [-1, 1]
RAY_TO_NDC="False"
```

All XYZ are converted to be in [-1, 1].

# TODO

- [ ] Remove local dependence in torchsearchsorted
- [ ] Publish to Pypi
