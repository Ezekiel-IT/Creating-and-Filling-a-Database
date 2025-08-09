
import pytest
from common_setup import run_test

def test_users_table_exists():
    run_test("users_table_exists", "Student creates a table 'called' users in the people.db database", "Error: Table 'users' not found in 'people.db'. Ensure the table was created.")

if __name__ == '__main__':
    pytest.main()