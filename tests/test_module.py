from public_package_template.module import mock_function_one, mock_function_two


def test_mock_function_one():
    assert mock_function_one() == "Hello from mock_function_one"


def test_mock_function_two():
    assert mock_function_two(2, 3) == 5
    assert mock_function_two(-1, 1) == 0
