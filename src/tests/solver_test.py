import pytest

from cube import make_white_up_green_front_cube
from solver import (
    CORNER_SETUP_MOVES,
    CORNER_SWAP_MOVES,
    EDGE_SETUP_MOVES,
    EDGE_SWAP_MOVES,
    PARITY_MOVES,
    OldPochmannSolver,
    SetupMove,
)


class TestDummyOldPochmannSolver:
    TEST_EDGE_SWAP_MOVES = "<edge-swap>"
    TEST_CORNER_SWAP_MOVES = "<corner-swap>"
    TEST_PARITY_MOVES = "<parity-resolve>"
    TEST_EDGE_SETUP_MOVES_MAPPING = {
        "A": SetupMove("edge-setup-1", "edge-setup-1-inv"),
        "B": SetupMove("edge-setup-2", "edge-setup-2-inv"),
    }
    TEST_CORNER_SETUP_MOVES_MAPPING = {
        "C": SetupMove("corner-setup-1", "corner-setup-1-inv"),
        "D": SetupMove("corner-setup-2", "corner-setup-2-inv"),
    }

    @pytest.fixture
    def old_pochmann_solver(self):
        return OldPochmannSolver(
            self.TEST_EDGE_SWAP_MOVES,
            self.TEST_CORNER_SWAP_MOVES,
            self.TEST_PARITY_MOVES,
            self.TEST_EDGE_SETUP_MOVES_MAPPING,
            self.TEST_CORNER_SETUP_MOVES_MAPPING,
        )

    @pytest.mark.parametrize(
        "edge_swap_letters, corner_swap_letters, corners_first, expected_moves",
        [
            pytest.param(
                "A",
                "C",
                False,
                "edge-setup-1 <edge-swap> edge-setup-1-inv "
                "<parity-resolve> "
                "corner-setup-1 <corner-swap> corner-setup-1-inv",
                id="single_edge_single_corner",
            ),
            pytest.param(
                "A",
                "C",
                True,
                "corner-setup-1 <corner-swap> corner-setup-1-inv "
                "<parity-resolve> "
                "edge-setup-1 <edge-swap> edge-setup-1-inv",
                id="single_edge_single_corner_reversed",
            ),
            pytest.param(
                "AB",
                "CD",
                False,
                "edge-setup-1 <edge-swap> edge-setup-1-inv "
                "edge-setup-2 <edge-swap> edge-setup-2-inv "
                "corner-setup-1 <corner-swap> corner-setup-1-inv "
                "corner-setup-2 <corner-swap> corner-setup-2-inv",
                id="two_edges_two_corners",
            ),
            pytest.param(
                "AB",
                "CD",
                True,
                "corner-setup-1 <corner-swap> corner-setup-1-inv "
                "corner-setup-2 <corner-swap> corner-setup-2-inv "
                "edge-setup-1 <edge-swap> edge-setup-1-inv "
                "edge-setup-2 <edge-swap> edge-setup-2-inv",
                id="two_edges_two_corners_reversed",
            ),
        ],
    )
    def test_swaps_to_moves(
        self,
        old_pochmann_solver,
        edge_swap_letters,
        corner_swap_letters,
        corners_first,
        expected_moves,
    ):
        moves = old_pochmann_solver.swaps_to_moves(
            edge_swap_letters, corner_swap_letters, corners_first=corners_first
        )
        assert moves == expected_moves


class TestRealOldPochmannSolver:
    @pytest.fixture
    def old_pochmann_solver(self):
        return OldPochmannSolver(
            EDGE_SWAP_MOVES, CORNER_SWAP_MOVES, PARITY_MOVES, EDGE_SETUP_MOVES, CORNER_SETUP_MOVES
        )

    @pytest.fixture
    def cube(self):
        return make_white_up_green_front_cube()

    @pytest.mark.parametrize(
        "edge_swap_letters, corner_swap_letters, corners_first, apply_parity, expected_cube_flat_str",
        [
            pytest.param(
                "D",
                "",
                False,
                False,
                "WWWWWWWWW" + "OROGGRBOGRBB" + "OOOGGGRRRBBB" + "OOOGGGRRRBBB" + "YYYYYYYYY",
                id="T_perm",
            ),
            pytest.param(
                "",
                "W",
                False,
                False,
                "RWWWWWWWW" + "YBOGGGRRRBOG" + "OOOGGGRRRBBB" + "OOOGGBWRRBBB" + "YYOYYYYYY",
                id="Y_perm",
            ),
            pytest.param(
                "L",
                "",
                False,
                False,
                "WWWWWGWWW" + "OOOGGRBOGRBB" + "OORWGGRRRBBB" + "OOOGGGRRRBBB" + "YYYYYYYYY",
                id="single_corner_swap_L",
            ),
            pytest.param(
                "AC",
                "",
                False,
                False,
                "WWWWWWWWW" + "OOOGBGRGRBRB" + "OOOGGGRRRBBB" + "OOOGGGRRRBBB" + "YYYYYYYYY",
                id="three_corner_cycle_up_layer",
            ),
            pytest.param(
                "D",
                "W",
                False,
                False,
                "RWWWWWWWW" + "YBOGGRBOGRRG" + "OOOGGGRRRBBB" + "OOOGGBWRRBBB" + "YYOYYYYYY",
                id="D_edge_W_corner_no_setup",
            ),
        ],
    )
    def test_solve(
        self,
        old_pochmann_solver,
        cube,
        edge_swap_letters,
        corner_swap_letters,
        corners_first,
        apply_parity,
        expected_cube_flat_str,
    ):
        old_pochmann_solver.solve(
            cube, edge_swap_letters, corner_swap_letters, corners_first, apply_parity
        )
        assert cube.as_flat_str() == expected_cube_flat_str
