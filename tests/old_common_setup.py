import subprocess
import requests
import json
import socket
import os
import platform
import sqlite3

def check_internet_connection():
    """Check if there is an active internet connection."""
    try:
        # Try to connect to a known server (Google's public DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def run_program(file_to_run):
    """Run the student's program using subprocess and return the output."""

    # Determine the command based on the operating system
    if platform.system() == "Windows":
        command = ['python', file_to_run]
    else:
        command = ['python3', file_to_run]

    # Run the student's program and capture output
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        #check=True
    )

    return result.stdout  # Capture standard output
## TEST 1
def logic_database_exits():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
    """Logic to test if the database is created successfully."""
    test_createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_createDB.py'))
    run_program(test_createDB_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the 'users' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if os.path.exists(db_path):
        output = ("Database created successfully.")
    else:
        output = ("Error: Database 'people.db' not found. Ensure that it was created and that it's called 'people.db'.")
    return output

## TEST 2
def logic_users_table_exists():
    """Logic to see if the users_table is created successfully."""
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
    test_createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_createDB.py'))
    run_program(test_createDB_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone() is not None:
        output = "Users table successfully created."
    else:
        output = "Error: Table 'users' not found in 'people.db'. Ensure the table was created."
    return output

## Test 3
def logic_records_inserted_into_db():
    """Logic to see if the records were inserted into the database successfully."""
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    row_count = cursor.fetchone()[0]

    if(row_count >= 5):
        output = "Data inserted successfully."
    else:
        output = "Failure: Not all records were inserted into the users table within people.db as shown in the example output"
    return output


def pre_test_setup(test_name=None):
    test_outputs = {}
    test_points_awarded = {}
    test_feedback = {}
    test_response_data = None

    createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'createDB.py'))
    insert_recs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'insert_recs.py'))
    autograding_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.github', 'classroom', 'autograding.json'))
    test_createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_createDB.py'))
    peopleDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))


    if test_name:
        if test_name == "database_exists":
            test_outputs["database_exists"] = logic_database_exits()
        elif test_name == "users_table_exists":
            test_outputs["users_table_exists"] = logic_users_table_exists()
        elif test_name == "records_inserted_into_db":
            test_outputs["records_inserted_into_db"] = logic_records_inserted_into_db()
    else:
        test_outputs = {
            "database_exists": logic_database_exits(),
            "users_table_exists": logic_users_table_exists(),
            "records_inserted_into_db": logic_records_inserted_into_db(),
        }

    if check_internet_connection():
        try:
            with open(createDB_path, 'r') as f:
                student_code_createDB = f.read()
            with open(insert_recs_path, 'r') as f:
                student_code_insert_recs = f.read()

            conn = sqlite3.connect(peopleDB_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            conn.close()
            student_DB = ""
            for user in users:
                student_DB += str(user) + "\n"
            student_code = "test_createDB.py file:\n" + student_code_createDB + "\ninsert_recs.py file:\n" + student_code_insert_recs + "\nStudent sqlite people.db file\n" + student_DB
            with open(test_createDB_path, 'r') as f:
                pytest_code = f.read()
            with open(autograding_path, 'r') as f:
                autograding_config = json.load(f)
                filtered_autograding_config = {"tests": autograding_config["tests"][:3]}

            # Determine which test is being run
            if test_name:
                print(f"Running test: {test_name}")
                # Filter the autograding config to include only the relevant section - this avoids grading on unnecessary criteria
                relevant_tests = [test for test in autograding_config["tests"] if f"/{test_name}.py" in test["run"]]
                autograding_config["tests"] = relevant_tests

            # Prepare the data for the POST request
            data = {
                "studentCode": student_code,
                "pytestCode": pytest_code,
                "autogradingConfig": json.dumps(filtered_autograding_config),
                "terminalOutputs": "When grading, if all terminal outputs say that they are all successful please give full points (20 points) on the assignment. Here are the terminal outputs:\n" + str(list(test_outputs.values()))
            }

            # Send the POST request
            response = requests.post('https://autograding-api-next.vercel.app/api/autograde', json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the response
            test_response_data = response.json()

            # Store the points awarded for each test
            test_points_awarded.update({test['name']: test['pointsAwarded'] for test in test_response_data["tests"]})

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"API call failed: {e}")
            print("Proceeding without API response. Run the test again with a working API to receive more user-friendly feedback.")

    if check_internet_connection() and test_response_data:
        # Print the results in a well-formatted manner
        test_feedback = (
            "\nTest Results:\n"
            + "\n".join(
                [
                    f"Test Name: {test['name']}\nPoints Awarded: {test['pointsAwarded']}\nFeedback: {test['feedback']}\n"
                    for test in test_response_data["tests"]
                ]
            )
            + f"\nTotal Points Awarded: {test_response_data['totalPointsAwarded']}\n"
            + f"Total Points Possible: {test_response_data['totalPointsPossible']}\n"
            + "\nSpecific Code Feedback:\n"
            + "\n".join(
                [
                    f"{feedback['feedback']}\nRecommendation: {feedback['recommendation']}\n"
                    for feedback in test_response_data["specificCodeFeedback"]["code"]
                ]
            )
            + "\nGeneral Feedback:\n"
            + test_response_data["specificCodeFeedback"]["general"]
        )
    else:
        print("No active internet connection or API response. Run the test again with an active internet connection and a working API to receive more user-friendly feedback.")

    return test_outputs, test_points_awarded, test_feedback, test_response_data

def run_test(test_name, test_point_key, offline_feedback):
    test_outputs, test_points_awarded, test_feedback, test_response_data = pre_test_setup(test_name=test_name)
    print("Test Outputs -------------------", test_outputs)
    output = test_outputs[test_name]

    autograding_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '.github', 'classroom', 'autograding.json'))
    # Load points from autograding.json
    with open(autograding_path, 'r') as f:
        autograding_config = json.load(f)

    # Find the points for the specific test
    test_config = next((test for test in autograding_config["tests"] if test["name"] == test_point_key), None)
    expected_points = test_config["points"] if test_config else 0

    if check_internet_connection():
        assert test_points_awarded.get(test_point_key, 0) == expected_points, test_feedback
    else:
        assert offline_feedback in output.strip(), offline_feedback
