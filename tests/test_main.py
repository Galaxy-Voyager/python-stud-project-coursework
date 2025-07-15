from unittest.mock import patch

from src.main import main


def test_main_success():
    with patch("src.views.home_page") as mock_home:
        mock_home.return_value = {"test": "data"}
        main()


def test_main_error():
    with patch("src.views.home_page", side_effect=Exception("Test error")):
        main()


def test_main_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = main()
        assert result == 1
