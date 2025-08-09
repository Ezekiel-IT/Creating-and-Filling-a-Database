
import pytest
from common_setup import run_test

def test_database_exists():
    run_test("database_exists", "Student creates a database called 'people.db", "Student didn't create a database called 'people.db")

if __name__ == '__main__':
    pytest.main()