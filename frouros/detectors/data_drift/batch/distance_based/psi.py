"""PSI (Population Stability Index) module."""

import sys

from typing import List, Optional, Union
import numpy as np  # type: ignore

from frouros.callbacks import Callback
from frouros.detectors.data_drift.batch.distance_based.base import (
    DistanceBinsBasedBase,
    DistanceResult,
)


class PSI(DistanceBinsBasedBase):
    """PSI (Population Stability Index) algorithm class."""

    def __init__(
        self,
        num_bins: int = 10,
        callbacks: Optional[Union[Callback, List[Callback]]] = None,
    ) -> None:
        """Init method.

        :param num_bins: number of bins in which to divide probabilities
        :type num_bins: int
        :param callbacks: callbacks
        :type callbacks: Optional[Union[Callback, List[Callback]]]
        """
        super().__init__(
            statistical_method=self._psi,
            statistical_kwargs={
                "num_bins": num_bins,
            },
            callbacks=callbacks,
        )
        self.num_bins = num_bins

    def _apply_method(
        self, X_ref: np.ndarray, X: np.ndarray, **kwargs  # noqa: N803
    ) -> DistanceResult:
        distance = self._distance_measure(X_ref=X_ref, X=X, **kwargs)
        return distance

    def _distance_measure_bins(
        self,
        X_ref: np.ndarray,  # noqa: N803
        X: np.ndarray,  # noqa: N803
    ) -> float:
        psi = self._psi(X=X_ref, Y=X, num_bins=self.num_bins)
        return psi

    @staticmethod
    def _psi(
        X: np.ndarray,  # noqa: N803
        Y: np.ndarray,  # noqa: N803
        num_bins: int,
    ) -> float:
        (  # noqa: N806
            X_percents,
            Y_percents,
        ) = DistanceBinsBasedBase._calculate_bins_values(
            X_ref=X, X=Y, num_bins=num_bins
        )
        # Replace 0.0 values with the smallest number possible
        # in order to avoid division by zero
        X_percents[X_percents == 0.0] = sys.float_info.min
        Y_percents[Y_percents == 0.0] = sys.float_info.min
        psi = np.sum((Y_percents - X_percents) * np.log(Y_percents / X_percents))
        return psi
