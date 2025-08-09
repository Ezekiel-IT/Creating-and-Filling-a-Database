
import pytest
from common_setup import run_test

def test_number_of_users():
    run_test("records_inserted_in_db", "Student inserted all user records into the users table as shown in the example output", "Student has not inserted all user records into the users table as shown in the example output")

if __name__ == '__main__':
    pytest.main()