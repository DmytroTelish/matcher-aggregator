from queue import Queue, Empty  # Removed unnecessary import of `queue`
from threading import Lock
from typing import Dict, List, Optional


class Aggregator:
    QUEUE_TIMEOUT = 10

    def __init__(self, result_queue: Queue, total_chunks: int):
        self.result_queue = result_queue
        self.total_chunks = total_chunks
        self._completed_chunks = 0
        self._aggregated_results: Dict[str, List[Dict[str, int]]] = {}
        self._lock = Lock()  # Renamed for simplicity

    def aggregate_results(self) -> None:
        while self._completed_chunks < self.total_chunks:
            try:
                matcher_result: Optional[Dict[str, List[Dict[str, int]]]] = self.result_queue.get(
                    timeout=self.QUEUE_TIMEOUT)
            except Empty:
                break  # Breaking the loop if the queue is empty for QUEUE_TIMEOUT duration
            if matcher_result is None:
                continue
            self._update_results(matcher_result)
        self._print_results()

    def _update_results(self, matcher_result: Dict[str, List[Dict[str, int]]]) -> None:
        with self._lock:
            for name, locations in matcher_result.items():
                if name not in self._aggregated_results:
                    self._aggregated_results[name] = []
                self._aggregated_results[name].extend(locations)
            self._completed_chunks += 1

    def _print_results(self) -> None:
        formatted_results = self._format_results()
        with self._lock:
            print(formatted_results)

    def _format_results(self) -> str:
        results = []
        for name, locations in self._aggregated_results.items():
            results.append(f"{name} --> {locations}")
        return "\n".join(results)
