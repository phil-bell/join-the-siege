import pytest
from werkzeug.datastructures import FileStorage

from src.classifier import classify_file


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("drivers_license.pdf", "drivers_licence"),
        ("drivers_licence.pdf", "drivers_licence"),
        ("bank_statement.png", "bank_statement"),
        ("invoice.jpg", "invoice"),
        ("passport.jpg", "passport"),
        ("passsport.jpg", "passport"),
    ],
)
def test_classify_file(filename, expected):
    response = classify_file(filename)

    assert response == expected