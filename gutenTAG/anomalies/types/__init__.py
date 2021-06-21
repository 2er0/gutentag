from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from typing import Optional, Dict, Type
from typing_extensions import Protocol

from ...utils.types import BaseOscillationKind


class IsDataclass(Protocol):
    __dataclass_fields__: Dict


@dataclass
class AnomalyProtocol:
    start: int
    end: int
    base_oscillation: 'BaseOscillationInterface'
    base_oscillation_kind: BaseOscillationKind
    subsequence: Optional[np.ndarray] = None


class BaseAnomaly(ABC):
    @abstractmethod
    def __init__(self, parameters: IsDataclass):
        raise NotImplementedError()

    @abstractmethod
    def generate(self, anomaly_protocol: AnomalyProtocol) -> AnomalyProtocol:
        return anomaly_protocol

    @staticmethod
    @abstractmethod
    def get_parameter_class():
        raise NotImplementedError()
