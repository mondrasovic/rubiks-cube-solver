from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from cube import Color

if TYPE_CHECKING:
    from typing import TypeAlias

    from cube import Cube, Face

    PilImage: TypeAlias = Image.Image
    Draw: TypeAlias = ImageDraw.ImageDraw
    ColorSpec: TypeAlias = tuple[int, int, int]

COLOR_MAP = {
    Color.WHITE: (250, 250, 250),
    Color.ORANGE: (235, 136, 49),
    Color.GREEN: (49, 235, 117),
    Color.RED: (236, 49, 86),
    Color.BLUE: (49, 114, 235),
    Color.YELLOW: (235, 225, 49),
}


class CubeRenderer:
    def __init__(
        self,
        image_width: 1024,
        image_height: 768,
        color_map: dict[Color, ColorSpec] = COLOR_MAP,
        background_color: ColorSpec = (64, 64, 64),
        piece_border_color: ColorSpec = (32, 32, 32),
        border_size_percent: float = 0.02,
    ) -> None:
        self.image_width = image_width
        self.image_height = image_height
        self.color_map = color_map
        self.background_color = background_color
        self.piece_border_color = piece_border_color
        self.border_size_percent = border_size_percent

    def render(self, cube: Cube) -> PilImage:
        # The rendered cube is 3 faces tall and 4 faces wide
        face_side_size = min(self.image_height // 3, self.image_width // 4)

        x_left_start = (self.image_width - face_side_size * 4) // 2
        y_top_start = (self.image_height - face_side_size * 3) // 2

        image = Image.new(
            "RGB", size=(self.image_width, self.image_height), color=self.background_color
        )
        draw = ImageDraw.Draw(image)

        for (row, col), face in zip(((0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1)), cube):
            self._render_face(
                draw,
                face,
                x_left=x_left_start + col * face_side_size,
                y_top=y_top_start + row * face_side_size,
                face_side_size=face_side_size,
            )

        return image

    def _render_face(
        self, draw: Draw, face: Face, x_left: int, y_top: int, face_side_size: int
    ) -> None:
        piece_side_size = face_side_size // 3
        x_left_start = y_top_start = (face_side_size - piece_side_size * 3) // 2

        border_size = int(round(piece_side_size * self.border_size_percent))

        for (row, col), color in zip(itertools.product(range(3), repeat=2), face):
            x_1 = x_left + x_left_start + col * piece_side_size
            y_1 = y_top + y_top_start + row * piece_side_size
            x_2 = x_1 + piece_side_size
            y_2 = y_1 + piece_side_size
            color_rgb = self.color_map[color]

            draw.rectangle((x_1, y_1, x_2, y_2), fill=self.piece_border_color)
            draw.rectangle(
                (x_1 + border_size, y_1 + border_size, x_2 - border_size, y_2 - border_size),
                fill=color_rgb,
            )
