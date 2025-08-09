# *****************************************************************************
# *                                                                           *
# *   IMPORTANT: DO NOT MODIFY THIS FILE                                      *
# *                                                                           *
# *   This testing file is provided to help you check the functionality of    *
# *   your code and understand the requirements for this assignment.          *
# *                                                                           *
# *   Please review the tests carefully to understand what is expected, but   *
# *   DO NOT make any changes to this file. Modifying this file will          *
# *   interfere with the grading system, lead to incorrect results, and       *
# *   will be flagged as cheating.                                            *
# *                                                                           *
# *   Focus on writing your own code to meet the requirements outlined in the *
# *   tests.                                                                  *
# *                                                                           *
# *****************************************************************************

import subprocess
import sqlite3
import os
from common_setup import pre_test_setup, check_internet_connection

def test_all():
    test_outputs, test_points_awarded, test_feedback, test_response_data = pre_test_setup()  # passing no tests means test everything
    if check_internet_connection():
        assert test_response_data['totalPointsAwarded'] == test_response_data['totalPointsPossible'], test_feedback
    else:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
        ## TEST 1
        # Check if the database file 'people.db' exists

        assert os.path.exists(
            db_path), "Error: Database 'people.db' not found. Ensure that it was created and that it's called 'people.db'."

        ## TEST 2
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if the 'users' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")

        # Assert that the table exists
        assert cursor.fetchone() is not None, "Error: Table 'users' not found in 'people.db'. Ensure the table was created."

        # Close the connection
        conn.close()

        ## Test 3 Records Inserted
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor();
        cursor.execute("select COUNT(*) from users")
        row_count = cursor.fetchone()[0]

        # Assert that the output matches the expected output
        assert row_count >= 5, "Records were not inserted into the users table within the people.db as shown in the example output"
