# Experiencing NERF

# Structure
* notebooks: ipython notebooks that introduces NERF
* nerf_pl: a Pytorch implementation that supports custom datasets

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


# Getting started
## Simple Ipython Notebooks
-[x] notebooks

##
