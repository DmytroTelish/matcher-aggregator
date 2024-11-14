import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from matcher import Matcher
from aggregator import Aggregator
from reader import FileReader


def main():
    import os
    file_path = os.getenv('FILE_PATH', 'big.txt')
    chunk_size = int(os.getenv('CHUNK_SIZE', 1000))
    max_workers = int(os.getenv('MAX_WORKERS', 5))
    start_line = int(os.getenv('START_LINE', 0))

    result_queue = Queue()
    try:
        file_reader = FileReader(file_path, chunk_size)
    except Exception as e:
        print(f"Failed to read from {file_path}: {e}")
        return

    aggregator = Aggregator(result_queue, file_reader.total_chunks())

    # Start aggregating thread
    aggregator_thread = threading.Thread(target=aggregator.aggregate_results, daemon=True)
    aggregator_thread.start()

    try:
        # Use ThreadPoolExecutor for managing a pool of worker threads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for text_chunk in file_reader.read_by_chunks():
                matcher = Matcher(text_chunk, result_queue, start_line)
                futures.append(executor.submit(matcher.find_matches))
                start_line += chunk_size

            # Ensure all futures are completed
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error occurred during matching: {e}")

        # Signal the aggregator to stop
        result_queue.put(None)
    except Exception as e:
        print(f"Error occurred while processing: {e}")
    finally:
        # Wait for the aggregator thread to complete
        aggregator_thread.join()


if __name__ == "__main__":
    main()
