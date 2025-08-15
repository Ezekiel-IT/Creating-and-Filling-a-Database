import subprocess
import requests
import json
import socket
import os
import platform
import sys
import sqlite3
sys.path.append('..')
from central_setup.central_setup import (
    execute_logic,
    check_internet_connection,
    run_program,
    run_single_test,  # this function is called by the test files that import it from this file: common_setup.py
)

program_name = 'createDB.py'

def run_test(test_name, test_description, error_message):
    run_single_test(test_name, test_description, error_message, pre_test_setup)

def logic_database_exists():
    """Test if the database file was created."""
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
    createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'createDB.py'))
    
    # Remove existing database file to test if student's code creates it
    #if os.path.exists(db_path):
        #os.remove(db_path)
    
    # Run the student's createDB.py file
    run_program([], createDB_path)
    
    if os.path.exists(db_path):
        output = ("Database created successfully.")
    else:
        output = ("Error: Database 'people.db' not found. Ensure that it was created and that it's called 'people.db'.")
    return output

def logic_users_table_exists():
    """Test if the users table exists in the database."""
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
    createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'createDB.py'))
    
    # Remove existing database file to test if student's code creates it properly
    #if os.path.exists(db_path):
        #os.remove(db_path)
    
    # Run the student's createDB.py file
    run_program([], createDB_path)
    
    if not os.path.exists(db_path):
        output = "Error: Database 'people.db' not found. Ensure that it was created and that it's called 'people.db'."
    else:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone() is not None:
                output = "Users table successfully created."
            else:
                output = "Error: Table 'users' not found in 'people.db'. Ensure the table was created."
            conn.close()
        except sqlite3.Error as e:
            output = f"Database error: {e}"
        except Exception as e:
            output = f"Error accessing database: {e}"
    
    return output

def logic_records_inserted_in_db():
    """Test if records were properly inserted into the database."""
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
    createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'createDB.py'))
    insert_recs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'insert_recs.py'))

    # Remove existing database file to test if student's code creates it properly
    #if os.path.exists(db_path):
        #os.remove(db_path)
    
    # Run the student's createDB.py file first
    run_program([], createDB_path)
    
    # Check if database was created before running insert script
    if not os.path.exists(db_path):
        output = "Error: Database 'people.db' not found. Ensure that it was created by createDB.py."
        return output
    
    # Then run the student's insert_recs.py file
    run_program([], insert_recs_path)

    # Only try to query if database still exists
    if not os.path.exists(db_path):
        output = "Error: Database 'people.db' not found after running insert_recs.py."
        return output

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        row_count = cursor.fetchone()[0]
        conn.close()

        if(row_count >= 5):
            output = "Data inserted successfully."
        else:
            output = "Failure: Not all records were inserted into the users table within people.db as shown in the example output"
    except sqlite3.Error as e:
        output = f"Database error: {e}"
    except Exception as e:
        output = f"Error accessing database: {e}"
    
    return output

def pre_test_setup(test_name=None):
    test_outputs = {}
    test_points_awarded = {}
    test_feedback = ""
    test_response_data = None

    # Define paths
    createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'createDB.py'))
    insert_recs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'insert_recs.py'))
    autograding_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.github', 'classroom', 'autograding.json'))
    test_createDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_createDB.py'))
    peopleDB_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'people.db'))

    if test_name:
        if test_name == "database_exists":
            test_outputs["database_exists"] = logic_database_exists()
        elif test_name == "users_table_exists":
            test_outputs["users_table_exists"] = logic_users_table_exists()
        elif test_name == "records_inserted_in_db":
            test_outputs["records_inserted_in_db"] = logic_records_inserted_in_db()
    else:
        test_outputs = {
            "database_exists": logic_database_exists(),
            "users_table_exists": logic_users_table_exists(),
            "records_inserted_in_db": logic_records_inserted_in_db()
        }

    if check_internet_connection():
        try:
            # Read the contents of the files
            with open(createDB_path, 'r') as f:
                student_code_createDB = f.read()
            with open(insert_recs_path, 'r') as f:
                student_code_insert_recs = f.read()

            # Read database content if it exists
            student_DB = ""
            if os.path.exists(peopleDB_path):
                conn = sqlite3.connect(peopleDB_path)
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM users")
                    users = cursor.fetchall()
                    for user in users:
                        student_DB += str(user) + "\n"
                except sqlite3.OperationalError:
                    student_DB = "Database exists but users table not found or empty"
                conn.close()
            else:
                student_DB = "Database file not found"

            # Combine student code with database content
            student_code = "createDB.py file:\n" + student_code_createDB + "\ninsert_recs.py file:\n" + student_code_insert_recs + "\nStudent sqlite people.db file\n" + student_DB
            
            with open(test_createDB_path, 'r') as f:
                pytest_code = f.read()
            with open(autograding_path, 'r') as f:
                autograding_config = json.load(f)

            # Filter autograding config to first 3 tests
            filtered_autograding_config = {"tests": autograding_config["tests"][:3]}

            # Determine which test is being run
            if test_name:
                print(f"Running test: {test_name}")
                # Filter the autograding config to include only the relevant section
                relevant_tests = [test for test in autograding_config["tests"] if f"/{test_name}.py" in test["run"]]
                filtered_autograding_config["tests"] = relevant_tests

            # Pass the logic to the central_setup module
            test_outputs, test_points_awarded, test_feedback, test_response_data = execute_logic(
                test_name, test_outputs, student_code, pytest_code, filtered_autograding_config
            )

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"API call failed: {e}")
            print("Proceeding without API response. Run the test again with a working API to receive more user-friendly feedback.")

    return test_outputs, test_points_awarded, test_feedback, test_response_data
