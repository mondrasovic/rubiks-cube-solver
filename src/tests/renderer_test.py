import pytest

from cube import make_white_up_green_front_cube
from renderer import CubeRenderer


class TestCubeRenderer:
    @pytest.fixture
    def cube(self):
        return make_white_up_green_front_cube()

    @pytest.fixture
    def renderer(self):
        return CubeRenderer(image_width=800, image_height=600)

    def test_image_size_matches(self, cube, renderer):
        image = renderer.render(cube)
        assert image.size == (800, 600)
