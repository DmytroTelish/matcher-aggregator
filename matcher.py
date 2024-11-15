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
LINE_ENDING = '\n'
INITIAL_CHAR_OFFSET = 0


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
        self.chunk_start_line = start_line
        self.name_patterns = build_name_patterns()
        self.results: Dict[str, List[Dict[str, int]]] = {}

    def _process_match(self, name: str, char_pos_in_line: int) -> None:
        if name not in self.results:
            self.results[name] = []
        self.results[name].append({"lineOffset": self.chunk_start_line, "charOffset": char_pos_in_line})

    def _find_pattern_matches(self, line: str, line_offset_in_chunk: int) -> None:
        cleaned_line = line.rstrip(LINE_ENDING)
        for name, pattern in self.name_patterns.items():
            for match in pattern.finditer(cleaned_line):
                char_pos_in_line = line_offset_in_chunk + match.start()
                self._process_match(name, char_pos_in_line)

    def process_lines_and_find_matches(self) -> None:
        try:
            text_lines = self.text_chunk.split(LINE_ENDING)
            total_char_offset = INITIAL_CHAR_OFFSET
            for line in text_lines:
                self._find_pattern_matches(line, total_char_offset)
                total_char_offset += len(line)
        except Exception as e:
            print(f"{ERROR_PROCESSING_LINES} {e}")

    def find_matches(self) -> None:
        try:
            self.process_lines_and_find_matches()
            self.results_queue.put(self.results)
        except Exception as e:
            print(f"{ERROR_FINDING_MATCHES} {e}")
