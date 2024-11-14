from typing import Generator


class FileReader:

    def __init__(self, file_path: str, chunk_size: int):
        self.file_path = file_path
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")
        self.chunk_size = chunk_size

    def read_by_chunks(self, encoding: str = 'utf-8') -> Generator[str, None, None]:
        try:
            yield from self._read_lines_in_chunks(encoding)
        except FileNotFoundError:
            self._handle_file_not_found()
        except IOError as e:
            self._handle_io_error(e)

    def total_chunks(self, encoding: str = 'utf-8') -> int:
        try:
            with open(self.file_path, 'r', encoding=encoding) as file:
                line_count = sum(1 for line in file)
            return (line_count + self.chunk_size - 1) // self.chunk_size
        except FileNotFoundError:
            self._handle_file_not_found()
            return 0
        except IOError as e:
            self._handle_io_error(e)
            return 0

    def _read_lines_in_chunks(self, encoding: str) -> Generator[str, None, None]:
        with open(self.file_path, 'r', encoding=encoding) as file:
            buffer = []
            for line in file:
                buffer.append(line)
                if len(buffer) >= self.chunk_size:
                    yield ''.join(buffer)
                    buffer = []
            if buffer:
                yield ''.join(buffer)

    def _handle_file_not_found(self):
        print(f"Error: {self.file_path} does not exist.")

    def _handle_io_error(self, error: IOError):
        print(f"Error reading file {self.file_path}: {error}")
