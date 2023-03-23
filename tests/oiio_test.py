import sys
import os

CURRENT_DIR = os.path.dirname(__file__)

try:
    import OpenImageIO as oiio
except ImportError as err:
    print(f"[ERROR] : Can't import OpenImageIO : {str(err)}")
    sys.exit(1)

if __name__ == "__main__":
    img_input = oiio.ImageInput.open(f"{CURRENT_DIR}/test_img.png")

    if img_input is None:
        print(f"[ERROR] : Can't read image : {oiio.geterror()}")
        sys.exit(1)

    img_input.close()

    print(f"[INFO] : Test passed successfully")
