from unittest.mock import patch
from src.main import main

def test_main_success():
    with patch("src.main.home_page") as mock_home:
        mock_home.return_value = {"test": "data"}
        with patch("src.main.json.dumps") as mock_dumps:
            mock_dumps.return_value = "{}"
            main()
            mock_home.assert_called_once()
            mock_dumps.assert_called_once()

def test_main_error():
    with patch("src.main.home_page", side_effect=Exception("test")) as mock_home:
        with patch("src.main.print") as mock_print:
            main()
            mock_print.assert_called_with("Ошибка при выполнении: test")
