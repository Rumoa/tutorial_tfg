import logging
from pathlib import Path

import pandas as pd
from experiments import Experiment


logger = logging.getLogger("results")


class ResultLogger:
    def __init__(self, path, flush_interval=100):
        self.path = Path(path)
        self.flush_interval = flush_interval
        self.buffer = []

        # load existing exp_ids
        if self.path.exists():
            df = pd.read_parquet(self.path, columns=["exp_id"])
            self.done_ids = set(df["exp_id"].astype(str))
            logger.info(f"Found {len(self.done_ids)} existing experiments to skip.")
        else:
            self.done_ids = set()
            logger.info(
                "ResultLogger initialized."
                "No existing results file found; starting fresh."
            )

    def log(self, exp: Experiment, result) -> None:
        eid = exp.exp_id()
        if eid in self.done_ids:
            return
        rec = exp.to_record(result)
        self.buffer.append(rec)
        self.done_ids.add(eid)
        logger.debug(
            f"Buffered exp_id={eid}. Buffer size: {len(self.buffer)}/{self.flush_interval}."
        )
        if len(self.buffer) >= self.flush_interval:
            logger.info(
                f"Flush interval reached ({self.flush_interval} records). "
                "Flushing to disk..."
            )
            self.flush()

    def flush(self) -> None:
        if not self.buffer:
            return
        df_new = pd.DataFrame(self.buffer)
        logger.info(f"Flushing {len(df_new)} new records to {self.path}.")
        if self.path.exists():
            df_existing = pd.read_parquet(self.path)
            df_all = pd.concat([df_existing, df_new], ignore_index=True)
            total = len(df_all)
            logger.info(
                f"Read {len(df_existing)} existing records; total will be {total}."
            )
        else:
            df_all = df_new
        self.path.parent.mkdir(parents=True, exist_ok=True)
        df_all.to_parquet(self.path, compression="zstd", index=False)
        logger.info(f"Successfully wrote {len(df_all)} total records to {self.path}.")
        self.buffer.clear()
        logger.debug("Buffer cleared after flush.")
