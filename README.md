# Text Matcher-Aggregator

## Overview

Text Matcher-Aggregator is a Python-based multithreaded application designed for processing large text files by breaking them into manageable chunks. It searches for specific names within each chunk and aggregates the results. The project aims to demonstrate efficient file reading, multi-threading, and result aggregation.

## Features

- **File Reading in Chunks:** Reads a large text file in specified chunk sizes to manage memory usage effectively.
- **Name Matching:** Searches for predefined names within each text chunk using regular expressions.
- **Multi-threading:** Utilizes Python's threading capabilities and `ThreadPoolExecutor` for concurrent processing.
- **Result Aggregation:** Aggregates the results safely using thread locks and prints the matches found.

## Project Structure

- **Aggregator:** Responsible for aggregating the results from workers and printing the final results.
- **FileReader:** Reads the file in chunks and handles file-related errors.
- **Matcher:** Searches for names within each text chunk and enqueues the results.
- **Main Script:** Orchestrates the file reading, processing, and result aggregation.

## Usage

### Prerequisites

- Python 3.8+
- Required Python packages:
  - `queue`
  - `threading`
  - `concurrent.futures`
  - `re`
  - `os`

### Environment Variables

The following environment variables can be set to customize the behavior of the application:

- `FILE_PATH`: Path to the text file to be processed (default is `big.txt`).
- `CHUNK_SIZE`: Number of lines per chunk (default is `1000`).
- `MAX_WORKERS`: Maximum number of worker threads (default is `5`).
- `START_LINE`: Starting line for processing (default is `0`).

### Running the Application

1. **Clone the repository:**
   
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install the required packages:**
   
    ```bash
    pip install -r requirements.txt
    ```

3. **Set the environment variables (optional):**

    ```bash
    export FILE_PATH=/path/to/your/big.txt
    export CHUNK_SIZE=1000
    export MAX_WORKERS=5
    export START_LINE=0
    ```

4. **Run the `main.py` script:**

    ```bash
    python main.py
    ```

## Classes and Methods

### Aggregator

```python
class Aggregator:
    def __init__(self, result_queue: Queue, total_chunks: int):
        # Initialization code

    def aggregate_results(self) -> None:
        # Aggregates results from the queue

    def _update_results(self, matcher_result: Dict[str, List[Dict[str, int]]]) -> None:
        # Updates the aggregate results

    def _print_results(self) -> None:
        # Prints the aggregated results

    def _format_results(self) -> str:
        # Formats and returns the results as a string
```

### FileReader

```python
class FileReader:
    def __init__(self, file_path: str, chunk_size: int):
        # Initialization code

    def read_by_chunks(self, encoding: str = 'utf-8') -> Generator[str, None, None]:
        # Reads the file in chunks

    def total_chunks(self, encoding: str = 'utf-8') -> int:
        # Calculates total chunks

    def _handle_file_not_found(self):
        # Handles file not found error

    def _handle_io_error(self, error: IOError):
        # Handles IO error
```

### Matcher

```python
class Matcher:
    def __init__(self, text_chunk: str, results_queue: Queue, start_line: int):
        # Initialization code

    def process_lines_and_find_matches(self) -> None:
        # Processes each line in the chunk to find matches

    def find_matches(self) -> None:
        # Finds and enqueues the matches
```

### Main Script

```python
def main():
    # Orchestrates the file reading, processing, and result aggregation
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.