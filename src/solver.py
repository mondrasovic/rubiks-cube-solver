from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Iterator

    from cube import Cube


@dataclasses.dataclass(frozen=True)
class SetupMove:
    moves: str
    inverse_moves: str

    def __post_init__(self) -> None:
        def count_moves(moves: str) -> int:
            return len(moves.strip().split())

        n_moves = count_moves(self.moves)
        n_inverse_moves = count_moves(self.inverse_moves)
        if n_moves != n_inverse_moves:
            raise ValueError(
                f"no. of moves {n_moves} does not equal the no. of inverse moves {n_inverse_moves}"
            )


EDGE_SWAP_MOVES = "R U Ri Ui Ri F R R Ui Ri Ui R U Ri Fi"
CORNER_SWAP_MOVES = "R Ui Ri Ui R U Ri Fi R U Ri Ui Ri F R"
PARITY_MOVES = "R U Ri Fi R U U Ri U U Ri F R U R U U Ri Ui"

EDGE_SETUP_MOVES = {
    "A": SetupMove("Lw Lw Di L L", "L L D Lw Lw"),
    "C": SetupMove("Lw Lw D L L", "L L Di Lw Lw"),
    "D": SetupMove("", ""),
    "E": SetupMove("L Dwi L", "Li Dw Li"),
    "F": SetupMove("Dwi L", "Li Dw"),
    "G": SetupMove("Li Dwi L", "Li Dw L"),
    "H": SetupMove("Dw Li", "L Dwi"),
    "I": SetupMove("Lw Lw Di L L", "L L D Lw Lw"),
    "J": SetupMove("Dw Dw L", "Li Dwi Dwi"),
    "K": SetupMove("Lw D L L", "L L Di Lwi"),
    "L": SetupMove("Li", "L"),
    "N": SetupMove("Dw L", "Li Dwi"),
    "O": SetupMove("Di Di Li Dwi L", "Li Dw L D D"),
    "P": SetupMove("Dwi Li", "L Dw"),
    "R": SetupMove("Lwi D L L", "L L Di Lw"),
    "S": SetupMove("L", "Li"),
    "T": SetupMove("Lwi Di L L", "Li Li D Lw"),
    "U": SetupMove("Dwi Dwi Li", "L Dw Dw"),
    "V": SetupMove("Di L L", "L L D"),
    "W": SetupMove("D D L L", "L L D D"),
    "Y": SetupMove("D L L", "L L Di"),
    "Z": SetupMove("L L", "L L"),
}

CORNER_SETUP_MOVES = {
    "B": SetupMove("R R", "R R"),
    "C": SetupMove("F F D", "Di F F"),
    "D": SetupMove("F F", "F F"),
    "F": SetupMove("Fi D", "Di F"),
    "G": SetupMove("Fi", "F"),
    "H": SetupMove("Di R", "Ri D"),
    "I": SetupMove("F Ri", "R Fi"),
    "J": SetupMove("Ri", "R"),
    "K": SetupMove("Fi Ri", "R F"),
    "L": SetupMove("F F Ri", "R Fi Fi"),
    "M": SetupMove("F", "Fi"),
    "N": SetupMove("Ri F", "Fi R"),
    "O": SetupMove("Ri Ri F", "Fi R R"),
    "P": SetupMove("R F", "Fi Ri"),
    "R": SetupMove("R Di", "D Ri"),
    "T": SetupMove("D Fi", "F Di"),
    "U": SetupMove("R", "Ri"),
    "V": SetupMove("D", "Di"),
    "W": SetupMove("", ""),
    "Y": SetupMove("Di", "D"),
    "Z": SetupMove("D D", "Di Di"),
}


class OldPochmannSolver:
    def __init__(
        self,
        edge_swap_moves: str = EDGE_SWAP_MOVES,
        corner_swap_moves: str = CORNER_SWAP_MOVES,
        parity_moves: str = PARITY_MOVES,
        edge_setup_moves_mapping: dict[str, SetupMove] = EDGE_SETUP_MOVES,
        corner_setup_moves_mapping: dict[str, SetupMove] = CORNER_SETUP_MOVES,
    ) -> None:
        self.edge_swap_moves = edge_swap_moves
        self.corner_swap_moves = corner_swap_moves
        self.parity_moves = parity_moves
        self.edge_setup_moves_mapping = edge_setup_moves_mapping
        self.corner_setup_moves_mapping = corner_setup_moves_mapping

    def solve(
        self,
        cube: Cube,
        edge_swap_letters: str,
        corner_swap_letters: str,
        corners_first: bool = False,
        apply_parity: bool = True,
    ) -> None:
        moves = self.swaps_to_moves(
            edge_swap_letters, corner_swap_letters, corners_first, apply_parity
        )
        cube.apply_moves(moves)

    def swaps_to_moves(
        self,
        edge_swap_letters: str,
        corner_swap_letters: str,
        corners_first: bool = False,
        apply_parity: bool = True,
    ) -> str:
        edge_setup_moves = [
            self.edge_setup_moves_mapping[swap_letter] for swap_letter in edge_swap_letters
        ]
        corner_setup_moves = [
            self.corner_setup_moves_mapping[swap_letter] for swap_letter in corner_swap_letters
        ]

        setup_moves_1, commutator_moves_1 = edge_setup_moves, self.edge_swap_moves
        setup_moves_2, commutator_moves_2 = corner_setup_moves, self.corner_swap_moves
        if corners_first:
            setup_moves_1, setup_moves_2 = setup_moves_2, setup_moves_1
            commutator_moves_1, commutator_moves_2 = commutator_moves_2, commutator_moves_1

        moves_list = list(
            self._interleave_setup_moves_with_commutator(setup_moves_1, commutator_moves_1)
        )
        if apply_parity and (len(edge_swap_letters) % 2 == 1):
            moves_list.append(self.parity_moves)
        moves_list.extend(
            self._interleave_setup_moves_with_commutator(setup_moves_2, commutator_moves_2)
        )

        moves = " ".join(moves_list)

        return moves

    @staticmethod
    def _interleave_setup_moves_with_commutator(
        setup_moves: Iterable[SetupMove], commutator_moves: str
    ) -> Iterator[str]:
        for setup_move in setup_moves:
            yield setup_move.moves
            yield commutator_moves
            yield setup_move.inverse_moves
