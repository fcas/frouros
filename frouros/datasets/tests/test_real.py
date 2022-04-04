"""Test real datasets module."""

import pytest  # type: ignore
import numpy as np  # type: ignore

from frouros.datasets.exceptions import ReadFileError
from frouros.datasets.real import Elec2


# Elec2 tests
def test_elec2_file_not_found_error(elec2_raw: Elec2, elec2_delimiter: str) -> None:
    """Test Elec2 file not found error.

    :param elec2_raw: Elec2 raw dataset
    :type elec2_raw: Elec2
    :param elec2_delimiter: Elec2 load delimiter
    :type elec2_delimiter: str
    """
    _ = elec2_raw.load(delimiter=elec2_delimiter)
    with pytest.raises(FileNotFoundError):
        _ = elec2_raw.load(delimiter=elec2_delimiter)


def test_elec2_no_verbose(elec2_delimiter: str) -> None:
    """Test Elec2 no verbose.

    :param elec2_delimiter: Elec2 load delimiter
    :type elec2_delimiter: str
    """
    elec2 = Elec2(verbose=False)
    elec2.download()
    _ = elec2.load(delimiter=elec2_delimiter)


def test_elec2_permission_error() -> None:
    """Test Elec2 permission error."""
    with pytest.raises(PermissionError):
        Elec2(file_path="//elec2").download()


def test_elec2_read_file_error(elec2_raw: Elec2) -> None:
    """Test Elec2 read file error.

    :param elec2_raw: Elec2 raw dataset
    :type elec2_raw: Elec2
    """
    with pytest.raises(ReadFileError):
        _ = elec2_raw.load()


def test_elec2_shape(elec2: np.ndarray) -> None:
    """Test Elec2 shape.

    :param elec2: Elec2 dataset
    :type elec2: np.ndarray
    """
    assert elec2.shape == (45313, 9)


def test_elec2_type(elec2: np.ndarray) -> None:
    """Test Elec2 type.

    :param elec2: Elec2 dataset
    :type elec2: np.ndarray
    """
    assert isinstance(elec2, np.ndarray)