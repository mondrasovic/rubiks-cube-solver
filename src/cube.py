from __future__ import annotations

import dataclasses
import enum
from typing import TYPE_CHECKING

import more_itertools
from rubik.cube import Cube as RubikCube

if TYPE_CHECKING:
    from typing import Iterator


class InvalidMove(Exception):
    """Raise when an invalid move is encountered in the string specification."""


class Color(enum.Enum):
    WHITE = "W"
    ORANGE = "O"
    GREEN = "G"
    RED = "R"
    BLUE = "B"
    YELLOW = "Y"

    @classmethod
    def from_string(cls, color_str: str) -> Color:
        for member in cls:
            if member.value == color_str:
                return member
        raise ValueError(f"unrecognized color: {color_str}")

    def __str__(self) -> str:
        return self.value


@dataclasses.dataclass(frozen=True)
class Face:
    piece_colors: list[list[Color]]

    def __post_init__(self) -> None:
        if not ((len(self.piece_colors) == 3) and all(len(row) == 3 for row in self.piece_colors)):
            raise ValueError("`piece_colors` is not a 3x3 list of colors")

    def __iter__(self) -> Color:
        yield from more_itertools.flatten(self.piece_colors)

    def __getitem__(self, index: tuple[int, int]) -> Color:
        row, col = index
        return self.piece_colors[row][col]

    def __str__(self) -> str:
        return "\n".join(" ".join(row.value for row in self.piece_colors))

    @classmethod
    def from_single_color(cls, color: Color) -> Face:
        return cls(piece_colors=[[color] * 3 for _ in range(3)])

    def as_flat_str(self) -> str:
        return "".join(
            str(piece_colors) for piece_colors in more_itertools.flatten(self.piece_colors)
        )


class Cube:
    def __init__(
        self, up: Face, left: Face, front: Face, right: Face, back: Face, down: Face
    ) -> None:
        cube_str = self._as_cube_str(up, left, front, right, back, down)
        self._cube = RubikCube(cube_str)

    def __str__(self) -> str:
        return str(self._cube)

    def __iter__(self) -> Iterator[Face]:
        row_face_indices = (0, 0, 0, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 5, 5, 5)
        faces_piece_colors = [[] for _ in range(6)]

        for face_index, row_colors_str in zip(
            row_face_indices, more_itertools.chunked(self.as_flat_str(), 3)
        ):
            faces_piece_colors[face_index].append(
                [Color.from_string(color_str) for color_str in row_colors_str]
            )

        for piece_colors in faces_piece_colors:
            yield Face(piece_colors)

    @staticmethod
    def _as_cube_str(up: Face, left: Face, front: Face, right: Face, back: Face, down: Face) -> str:
        cube_str = up.as_flat_str()
        cube_str += "".join(
            str(face[(row, col)])
            for row in range(3)
            for face in (left, front, right, back)
            for col in range(3)
        )
        cube_str += down.as_flat_str()
        return cube_str

    def as_flat_str(self) -> str:
        return self._cube.flat_str()

    def apply_moves(self, moves: str) -> None:
        for i, move in enumerate(moves.strip().split()):
            try:
                getattr(self, move)()
            except AttributeError:
                raise InvalidMove(f"invalid move '{move}' at position {i}")

    def is_solved(self) -> bool:
        return self._cube.is_solved()

    def L(self) -> None:
        self._cube.L()

    def Li(self) -> None:
        self._cube.Li()

    def Lw(self) -> None:
        self.L()
        self.M()

    def Lwi(self) -> None:
        self.Li()
        self.Mi()

    def R(self) -> None:
        self._cube.R()

    def Ri(self) -> None:
        self._cube.Ri()

    def Rw(self) -> None:
        self.R()
        self.Mi()

    def Rwi(self) -> None:
        self.Ri()
        self.M()

    def U(self) -> None:
        self._cube.U()

    def Ui(self) -> None:
        self._cube.Ui()

    def D(self) -> None:
        self._cube.D()

    def Di(self) -> None:
        self._cube.Di()

    def Dw(self) -> None:
        self.D()
        self.E()

    def Dwi(self) -> None:
        self.Di()
        self.Ei()

    def F(self) -> None:
        self._cube.F()

    def Fi(self) -> None:
        self._cube.Fi()

    def B(self) -> None:
        self._cube.B()

    def Bi(self) -> None:
        self._cube.Bi()

    def M(self) -> None:
        self._cube.M()

    def Mi(self) -> None:
        self._cube.Mi()

    def E(self) -> None:
        self._cube.E()

    def Ei(self) -> None:
        self._cube.Ei()


def make_white_up_green_front_cube() -> Cube:
    return Cube(
        up=Face.from_single_color(Color.WHITE),
        left=Face.from_single_color(Color.ORANGE),
        front=Face.from_single_color(Color.GREEN),
        right=Face.from_single_color(Color.RED),
        back=Face.from_single_color(Color.BLUE),
        down=Face.from_single_color(Color.YELLOW),
    )
