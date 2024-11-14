import re
from queue import Queue
from typing import Dict, List

NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Charles",
    "Joseph", "Thomas", "Christopher", "Daniel", "Paul", "Mark", "Donald", "George",
    "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony", "Kevin", "Jason",
    "Matthew", "Gary", "Timothy", "Jose", "Larry", "Jeffrey", "Frank", "Scott",
    "Eric", "Stephen", "Andrew", "Raymond", "Gregory", "Joshua", "Jerry", "Dennis",
    "Walter", "Patrick", "Peter", "Harold", "Douglas", "Henry", "Carl", "Arthur",
    "Ryan", "Roger"
]

ERROR_COMPILING_REGEX = "Error compiling regex patterns:"
ERROR_PROCESSING_LINES = "Error processing lines:"
ERROR_FINDING_MATCHES = "Error finding matches:"


def build_name_patterns() -> Dict[str, re.Pattern]:
    try:
        return {name: re.compile(fr"\b{name}\b") for name in NAMES}
    except re.error as e:
        print(f"{ERROR_COMPILING_REGEX} {e}")
        return {}


class Matcher:
    def __init__(self, text_chunk: str, results_queue: Queue, start_line: int):
        self.text_chunk = text_chunk
        self.results_queue = results_queue
        self.start_line = start_line
        self.name_patterns = build_name_patterns()
        self.results: Dict[str, List[Dict[str, int]]] = {}

    def _process_match(self, name: str, line_number: int, char_offset: int) -> None:
        if name not in self.results:
            self.results[name] = []
        self.results[name].append({"lineOffset": line_number, "charOffset": char_offset})

    def _process_line_for_matches(self, line: str, line_number: int, line_start_pos: int) -> None:
        for name, pattern in self.name_patterns.items():
            for match in pattern.finditer(line):
                char_offset = line_start_pos + match.start()
                self._process_match(name, line_number, char_offset)

    def process_lines_and_find_matches(self) -> None:
        try:
            text_lines = self.text_chunk.splitlines(keepends=True)
            line_number = self.start_line
            line_start_pos = 0
            for line in text_lines:
                self._process_line_for_matches(line, line_number, line_start_pos)
                line_number += 1
                line_start_pos += len(line)
        except Exception as e:
            print(f"{ERROR_PROCESSING_LINES} {e}")

    def find_matches(self) -> None:
        try:
            self.process_lines_and_find_matches()
            self.results_queue.put(self.results)
        except Exception as e:
            print(f"{ERROR_FINDING_MATCHES} {e}")
