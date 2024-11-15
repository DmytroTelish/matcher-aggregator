import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from matcher import Matcher
from aggregator import Aggregator
from reader import FileReader
import os

# Extracted Constants
FILE_PATH_ENV = 'FILE_PATH'
DEFAULT_FILE_PATH = 'big.txt'
CHUNK_SIZE_ENV = 'CHUNK_SIZE'
DEFAULT_CHUNK_SIZE = 1000
MAX_WORKERS_ENV = 'MAX_WORKERS'
DEFAULT_MAX_WORKERS = 5
START_LINE_ENV = 'START_LINE'
DEFAULT_START_LINE = 0


def get_env_variable(name, default):
    try:
        return int(os.getenv(name, default))
    except ValueError as e:
        print(f"Invalid value for environment variable {name}: {e}")
        return default

def initialize_file_reader(file_path, chunk_size):
    try:
        return FileReader(file_path, chunk_size)
    except Exception as e:
        print(f"Failed to read from {file_path}: {e}")
        return None


def process_chunks_with_threads(file_reader, chunk_size, max_workers, result_queue, start_line):
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for text_chunk in file_reader.read_by_chunks():
                matcher = Matcher(text_chunk, result_queue, start_line)
                futures.append(executor.submit(matcher.find_matches))
                start_line += chunk_size

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error occurred during matching: {e}")

        result_queue.put(None)

    except Exception as e:
        print(f"Error occurred while processing: {e}")



def main():
    file_path = os.getenv(FILE_PATH_ENV, DEFAULT_FILE_PATH)
    chunk_size = get_env_variable(CHUNK_SIZE_ENV, DEFAULT_CHUNK_SIZE)
    max_workers = get_env_variable(MAX_WORKERS_ENV, DEFAULT_MAX_WORKERS)
    start_line = get_env_variable(START_LINE_ENV, DEFAULT_START_LINE)

    result_queue = Queue()
    file_reader = initialize_file_reader(file_path, chunk_size)
    if not file_reader:
        return

    total_chunks = file_reader.total_chunks()
    aggregator = Aggregator(result_queue, total_chunks)
    aggregator_thread = threading.Thread(target=aggregator.aggregate_results, daemon=True)
    aggregator_thread.start()

    process_chunks_with_threads(file_reader, chunk_size, max_workers, result_queue, start_line)

    aggregator_thread.join()


if __name__ == "__main__":
    main()
