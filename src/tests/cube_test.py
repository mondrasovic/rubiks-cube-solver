import pytest

from cube import InvalidMove, make_white_up_green_front_cube


class TestCube:
    @pytest.fixture
    def cube(self):
        return make_white_up_green_front_cube()

    def test_as_flat_str(self, cube):
        assert cube.as_flat_str() == (
            "WWWWWWWWW" + "OOOGGGRRRBBB" + "OOOGGGRRRBBB" + "OOOGGGRRRBBB" + "YYYYYYYYY"
        )

    def test_is_solved(self, cube):
        assert cube.is_solved()

    @pytest.mark.parametrize(
        "move_method_name, expected_flat_str",
        [
            pytest.param(
                "L",
                "BWWBWWBWW" + "OOOWGGRRRBBY" + "OOOWGGRRRBBY" + "OOOWGGRRRBBY" + "GYYGYYGYY",
                id="L",
            ),
            pytest.param(
                "Lw",
                "BBWBBWBBW" + "OOOWWGRRRBYY" + "OOOWWGRRRBYY" + "OOOWWGRRRBYY" + "GGYGGYGGY",
                id="Lw",
            ),
            pytest.param(
                "Rw",
                "WGGWGGWGG" + "OOOGYYRRRWWB" + "OOOGYYRRRWWB" + "OOOGYYRRRWWB" + "YBBYBBYBB",
                id="Rw",
            ),
            pytest.param(
                "Dw",
                "WWWWWWWWW" + "OOOGGGRRRBBB" + "BBBOOOGGGRRR" + "BBBOOOGGGRRR" + "YYYYYYYYY",
                id="Dw",
            ),
        ],
    )
    def test_single_move(self, cube, move_method_name, expected_flat_str):
        getattr(cube, move_method_name)()
        assert cube.as_flat_str() == expected_flat_str

    @pytest.mark.parametrize(
        "moves, expected_flat_str",
        [
            pytest.param(
                "L",
                "BWWBWWBWW" + "OOOWGGRRRBBY" + "OOOWGGRRRBBY" + "OOOWGGRRRBBY" + "GYYGYYGYY",
                id="L",
            ),
            pytest.param(
                "L D",
                "BWWBWWBWW" + "OOOWGGRRRBBY" + "OOOWGGRRRBBY" + "BBYOOOWGGRRR" + "GGGYYYYYY",
                id="LD",
            ),
        ],
    )
    def test_apply_moves(self, cube, moves, expected_flat_str):
        cube.apply_moves(moves)
        assert cube.as_flat_str() == expected_flat_str

    @pytest.mark.parametrize("moves", ["?!", ".,/", "QW"])
    def test_apply_moves_raises_invalid_move(self, cube, moves):
        with pytest.raises(InvalidMove):
            cube.apply_moves(moves)
