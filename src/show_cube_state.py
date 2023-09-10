from __future__ import annotations

import click

from cube import make_white_up_green_front_cube
from renderer import CubeRenderer
from solver import OldPochmannSolver


@click.command()
@click.argument("edge_swap_letters", type=str)
@click.argument("corner_swap_letters", type=str)
@click.option(
    "--corners-first",
    is_flag=True,
    help="indicates whether to apply corner swaps before edge swaps",
)
@click.option(
    "--reverse-swap-letters",
    is_flag=True,
    help="indicates whether to reverse swap letter sequences (useful for verifying solves)",
)
@click.option(
    "--apply-parity",
    is_flag=True,
    help="indicates whether to apply parity if there is an odd number of swaps",
)
@click.option(
    "-w",
    "--image-width",
    type=int,
    default=1024,
    show_default=True,
    help="width of the rendered image",
)
@click.option(
    "-h",
    "--image-height",
    type=int,
    default=768,
    show_default=True,
    help="height of the rendered image",
)
def main(
    edge_swap_letters: str,
    corner_swap_letters: str,
    corners_first: bool,
    reverse_swap_letters: bool,
    apply_parity: bool,
    image_width: int,
    image_height: int,
) -> None:
    cube = make_white_up_green_front_cube()
    solver = OldPochmannSolver()
    renderer = CubeRenderer(image_width, image_height)

    if reverse_swap_letters:
        edge_swap_letters = reverse_str(edge_swap_letters)
        corner_swap_letters = reverse_str(corner_swap_letters)

    solver.solve(cube, edge_swap_letters, corner_swap_letters, corners_first, apply_parity)
    cube_image = renderer.render(cube)

    cube_image.show(title="Rubik's Cube Preview")


def reverse_str(s: str) -> str:
    return "".join(reversed(s))


if __name__ == "__main__":
    main()
