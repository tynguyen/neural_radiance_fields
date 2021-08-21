from nerf_pl import LLFF
import nerf_pl
def test_import():
	print(f"The import is successful")

def test_version():
	assert nerf_pl.__version__ == "0.1.3"