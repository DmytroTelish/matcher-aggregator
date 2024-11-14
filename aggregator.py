import queue
import threading
from queue import Queue
from typing import Dict, List, Optional


class Aggregator:
    TIMEOUT = 10

    def __init__(self, result_queue: Queue, total_chunks: int):
        self.result_queue = result_queue
        self.total_chunks = total_chunks
        self._completed_chunks = 0
        self._aggregated_results: Dict[str, List[Dict[str, int]]] = {}
        self._result_lock = threading.Lock()

    def aggregate_results(self) -> None:
        while self._completed_chunks < self.total_chunks:
            try:
                matcher_result: Optional[Dict[str, List[Dict[str, int]]]] = self.result_queue.get(
                    timeout=self.TIMEOUT)  # handle timeout
            except queue.Empty:
                break  # Breaking the loop if the queue is empty for TIMEOUT duration

            if matcher_result is None:
                continue

            self._update_results(matcher_result)
        self._print_results()

    def _update_results(self, matcher_result: Dict[str, List[Dict[str, int]]]) -> None:
        with self._result_lock:  # ensure thread safety
            for name, locations in matcher_result.items():
                if name not in self._aggregated_results:
                    self._aggregated_results[name] = []
                self._aggregated_results[name].extend(locations)
            self._completed_chunks += 1

    def _print_results(self) -> None:
        with self._result_lock:  # ensure thread safety
            for name, locations in self._aggregated_results.items():
                print(f"{name} --> {locations}")


