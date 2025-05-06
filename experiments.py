import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict


class Experiment(ABC):
    @abstractmethod
    def exp_id(self) -> str:
        """Return a deterministic, unique ID for this experiment."""
        ...

    @abstractmethod
    def to_record(
        self,
        result,
    ) -> Dict[str, Any]:
        """Serialize this experiment (plus result) into a dict."""
        ...


@dataclass(
    frozen=True
)  # <- with this we make the dataclass immutable so we don't overwrite their values by accident
class myExperiment(Experiment):
    initial_state: str
    delay_time: float
    qubit_id: int
    n_shots: int

    def exp_id(self) -> str:
        dict_of_fields = asdict(self)
        hash = hashlib.sha256(
            json.dumps(dict_of_fields, sort_keys=True).encode()
        ).hexdigest()
        return hash

    def to_record(self, result: int) -> dict:
        dict_of_fields = asdict(self)
        # we now add the results to the dictionary
        dict_of_fields.update(
            {
                "result": result,
                "datetime": datetime.now().isoformat(),
                "exp_id": self.exp_id(),
            }
        )
        return dict_of_fields
