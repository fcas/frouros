"""History callback module."""

from typing import Any, Dict, List, Optional

from frouros.callbacks.streaming.base import BaseCallbackStreaming
from frouros.utils.stats import BaseStat


class HistoryConceptDrift(BaseCallbackStreaming):
    """HistoryConceptDrift callback class.

    :param name: name value, defaults to None. If None, the name will be set to `HistoryConceptDrift`.
    :type name: Optional[str]

    :Note:
    By default the following variables are stored:

    - `value`: list of values received by the detector
    - `drift`: list of drift flags
    - `num_instances`: list of number of instances received by the detector
    Each detector may store additional variables if they are defined in an `additional_vars` dictionary in the detectors `__init__` method.
    The user can add additional variables by calling the :func:`add_additional_vars` method.

    :Example:

    >>> from frouros.callbacks import HistoryConceptDrift
    >>> from frouros.detectors.concept_drift import ADWIN
    >>> import numpy as np
    >>> np.random.seed(seed=31)
    >>> dist_a = np.random.normal(loc=0.2, scale=0.01, size=1000)
    >>> dist_b = np.random.normal(loc=0.8, scale=0.04, size=1000)
    >>> stream = np.concatenate((dist_a, dist_b))
    >>> detector = ADWIN(callbacks=[HistoryConceptDrift(name="history")])
    >>> for i, value in enumerate(stream):
    ...     callbacks_log = detector.update(value=value)
    ...     if detector.drift:
    ...         print(f"Change detected at step {i}")
    ...         break
    >>> print(callbacks_log["history"]["drift"])
    Change detected at step 1055
    [False, False, ..., True]
    """  # noqa: E501  # pylint: disable=line-too-long

    def __init__(  # noqa: D107
        self,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.additional_vars: List[str] = []
        self.history: Dict[str, List[Any]] = {
            "value": [],
            "num_instances": [],
            "drift": [],
        }

    def add_additional_vars(self, vars_: List[str]) -> None:
        """Add additional variables to track.

        :param vars_: list of variables
        :type vars_: List[str]
        """
        self.additional_vars.extend(vars_)
        self.history = {**self.history, **{var: [] for var in self.additional_vars}}

    def on_update_end(self, **kwargs) -> None:
        """On update end method."""
        self.history["value"].append(kwargs["value"])
        self.history["num_instances"].append(
            self.detector.num_instances  # type: ignore
        )
        self.history["drift"].append(self.detector.drift)  # type: ignore
        for var in self.additional_vars:
            additional_var = self.detector.additional_vars[var]  # type: ignore
            # FIXME: Extract isinstance check to be done when  # pylint: disable=fixme
            #  add_addtional_vars is called (avoid the same computation)
            self.history[var].append(
                additional_var.get()
                if isinstance(additional_var, BaseStat)
                else additional_var
            )

        self.logs.update(**self.history)

    # FIXME: set_detector method as a workaround to  # pylint: disable=fixme
    #  avoid circular import problem. Make it an abstract method and
    #  uncomment commented code when it is solved

    # def set_detector(self, detector) -> None:
    #     """Set detector method.
    #
    #     :raises TypeError: Type error exception
    #     """
    #     if not isinstance(detector, BaseConceptDrift):
    #         raise TypeError(
    #             f"callback {self.__class__.name} cannot be used with detector"
    #             f" {detector.__class__name}. Must be used with a detector of "
    #             f"type BaseConceptDrift."
    #         )
    #     self.detector = detector

    def reset(self) -> None:
        """Reset method."""
        for key in self.history.keys():
            self.history[key].clear()
