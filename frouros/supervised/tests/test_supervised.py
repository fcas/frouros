"""Test supervised methods."""

from typing import Tuple

import pytest  # type: ignore
from sklearn.metrics import accuracy_score  # type: ignore
from sklearn.linear_model import LogisticRegression  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore
import numpy as np  # type: ignore

from frouros.supervised.base import TargetDelayEstimator
from frouros.supervised.cusum_test import PageHinkleyTest, PageHinkleyTestConfig
from frouros.supervised.ddm_based import DDM, DDMConfig, EDDM, EDDMConfig
from frouros.supervised.utils import update_detector


ESTIMATOR = LogisticRegression
ESTIMATOR_ARGS = {
    "solver": "lbfgs",
    "max_iter": 1000,
}
MIN_NUM_INSTANCES = 500


def error_scorer(y_true, y_pred):
    """Error scorer function."""
    return 1 - accuracy_score(y_true, y_pred)


@pytest.mark.parametrize(
    "detector",
    [
        PageHinkleyTest(
            estimator=ESTIMATOR(**ESTIMATOR_ARGS),
            error_scorer=error_scorer,
            config=PageHinkleyTestConfig(
                delta=0.005,
                forgetting_factor=0.9999,
                lambda_=50,
                min_num_instances=MIN_NUM_INSTANCES,
            ),
        ),
        DDM(
            estimator=ESTIMATOR(**ESTIMATOR_ARGS),
            error_scorer=error_scorer,
            config=DDMConfig(
                warning_level=2.0,
                drift_level=3.0,
                min_num_instances=MIN_NUM_INSTANCES,
            ),
        ),
        EDDM(
            estimator=ESTIMATOR(**ESTIMATOR_ARGS),
            config=EDDMConfig(
                alpha=0.95,
                beta=0.9,
                level=2.0,
                min_num_misclassified_instances=500,
            ),
        ),
    ],
)
def test_supervised_method(
    classification_dataset: Tuple[np.array, np.array, np.array, np.array],
    detector: TargetDelayEstimator,
) -> None:
    """Test supervised dataset.

    :param classification_dataset: Elec2 raw dataset
    :type classification_dataset: Tuple[numpy.array, numpy.array,
    numpy.array, numpy.array]
    """
    X_ref, y_ref, X_test, y_test = classification_dataset  # noqa: N806

    pipe = Pipeline([("scaler", StandardScaler()), ("detector", detector)])

    pipe.fit(X=X_ref, y=y_ref)

    for X_sample, y_sample in zip(X_test, y_test):  # noqa: N806
        _ = pipe.predict(X=np.array([*X_sample]).reshape(1, -1))

        # Delayed targets arriving....
        _ = update_detector(
            estimator=pipe, y=np.array([y_sample]), detector_name="detector"
        )