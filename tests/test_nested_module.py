from public_package_template.nested.module import mock_function_three


def test_mock_function_three():
    """Test the mock_function_three."""
    assert mock_function_three(3, 4) == 12
    assert mock_function_three(-2, 5) == -10
