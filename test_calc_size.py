import importlib
import pytest

import image_size_calculator as img_calculator

def test_get_image_size():
    image_path = '/test-images/image-1.png'
    assert img_calculator.get_image_size(image_path) = 
