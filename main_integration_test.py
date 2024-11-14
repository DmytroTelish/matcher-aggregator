import os
import unittest
from unittest.mock import patch, mock_open
from main import main
import io
import sys
from contextlib import redirect_stdout


class TestMainIntegration(unittest.TestCase):

    def set_env_vars(self, chunk_size, file_path='mocked_file.txt', max_workers='1', start_line='0'):
        return patch.dict(os.environ, {
            'FILE_PATH': file_path,
            'CHUNK_SIZE': chunk_size,
            'MAX_WORKERS': max_workers,
            'START_LINE': start_line,
        })

    def run_main_test(self, mock_file_data, chunk_size, expected_output_contains=None,
                      expected_output_not_contains=None):
        with patch('builtins.open', new_callable=mock_open, read_data=mock_file_data):
            with self.set_env_vars(chunk_size=chunk_size):
                captured_output = io.StringIO()
                with redirect_stdout(captured_output):
                    main()
                self.assert_output(captured_output, contains=expected_output_contains,
                                   not_contains=expected_output_not_contains)

    def assert_output(self, captured_output, contains=None, not_contains=None):
        output = captured_output.getvalue()
        if contains:
            for item in contains:
                self.assertIn(item, output)
        if not_contains:
            for item in not_contains:
                self.assertNotIn(item, output)

    @patch('builtins.open', new_callable=mock_open, read_data="John\nMichael\n")
    def test_main_with_multiple_names(self, mock_file):
        self.run_main_test(mock_file_data="John\nMichael\n", chunk_size='1',
                           expected_output_contains=["John", "Michael"])

    @patch('builtins.open', new_callable=mock_open, read_data="Alice\nBob\n")
    def test_main_with_no_names(self, mock_file):
        self.run_main_test(mock_file_data="Alice\nBob\n", chunk_size='1',
                           expected_output_not_contains=["John", "Michael"])

    @patch('builtins.open', new_callable=mock_open, read_data="John\nMichael\n")
    def test_main_with_large_chunk(self, mock_file):
        self.run_main_test(mock_file_data="John\nMichael\n", chunk_size='10',
                           expected_output_contains=["John", "Michael"])

    @patch('builtins.open', new_callable=mock_open, read_data="John Michael\nJohn Michael\n")
    def test_main_with_multiple_lines_in_chunk(self, mock_file):
        self.run_main_test(mock_file_data="John Michael\nJohn Michael\n", chunk_size='2',
                           expected_output_contains=["John", "Michael"])

    @patch('builtins.open', new_callable=mock_open, read_data="John,! Michael.\n")
    def test_main_with_special_characters(self, mock_file):
        self.run_main_test(
            mock_file_data="John,! Michael.\n",
            chunk_size='1',
            expected_output_contains=["John", "Michael"]
        )

if __name__ == '__main__':
    unittest.main()
