import os

os.environ["ZMQ_SERVER"] = "tcp://127.0.0.1:5556"
import numpy as np

# from qmiotools.integrations.qiskitqmio.qmiobackend import QmioBackend # <- if you use the real hardware
import logging

import hashlib
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pandas as pd
from experiments import myExperiment
from logger import ResultLogger

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import HGate, XGate
from qmiotools.integrations.qiskitqmio.fakeqmio import FakeQmio
import argparse


def make_circuit(initial_state, delay_time):
    qc = QuantumCircuit(1)
    if initial_state == "+":
        qc.append(HGate(), [0])
    qc.delay(duration=delay_time, unit="s")
    qc.measure_all()
    return qc


def main(config_dict: dict):
    log_file = "logs.log"

    path_to_save_data = config_dict.get("parquet_results_file", "aux/temp.parquet")
    qubit_id = config_dict.get("qubit_id")

    backend = FakeQmio(
        logging_filename=None, logging_level=logging.ERROR
    )  # when using the real hardware, we will use QmioBackend

    logger = logging.getLogger("results")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    file_handler = logging.FileHandler(log_file, mode="a")
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    logging.getLogger("qiskit").setLevel(logging.WARNING)

    results_logger = ResultLogger(path_to_save_data, flush_interval=1)

    exp_a = myExperiment(
        initial_state="0", delay_time=0.00001, qubit_id=qubit_id, n_shots=1000
    )
    exp_b = myExperiment(
        initial_state="+", delay_time=0.000003, qubit_id=qubit_id, n_shots=1000
    )

    list_of_experiments = [exp_a, exp_b]

    list_circuits = []
    for info_circ in list_of_experiments:
        init_state_i = info_circ.initial_state
        delay_time_i = info_circ.delay_time
        ideal_circ_i = make_circuit(init_state_i, delay_time_i)
        list_circuits.append(ideal_circ_i)

    list_transpiled_circuits = []
    for info_circ_i, ideal_circ_i in zip(list_of_experiments, list_circuits):
        qubit_id_i = info_circ_i.qubit_id

        transpiled_circ_i = transpile(
            circuits=ideal_circ_i, backend=backend, initial_layout=[qubit_id_i]
        )
        list_transpiled_circuits.append(transpiled_circ_i)

    for exp_info_i, transpiled_circ_i in zip(
        list_of_experiments, list_transpiled_circuits
    ):
        if exp_info_i.exp_id() in results_logger.done_ids:
            logger.info(f"Skipping already done exp_id={exp_info_i.exp_id()}")
            continue
        print(exp_info_i)
        n_shots = exp_info_i.n_shots
        results = backend.run(
            transpiled_circ_i, shots=int(n_shots), output_qasm3=True
        ).result()
        counts = results.get_counts()
        counts_0 = counts.get("0", 0)

        results_logger.log(exp_info_i, counts_0)

        print(counts)

    results_logger.flush()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Two-qubit delay experiments.")
    p.add_argument("-c", "--config", type=Path, required=True)

    args = p.parse_args()

    with open(args.config, "r") as f:
        config_dict = json.load(f)

    main(
        config_dict,
    )
