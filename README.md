[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20056603)
Using data provided by a file called `users.py`, create a SQLite3 database called `people` that contains a table named `users`. The `users` table should have four fields:

```
user_id  integer   primary key   autoincrement
username TEXT
password TEXT
auth_level integer
```
Using the provided `insert_recs.py` file, write code to insert all of the records provided by the data file into the users table.

After you have inserted all of the data into the users table, run the Python file in the Codespace called `show_all_records.py`. This code will attempt to open the people.db database and read all of the records in the users table, printing each record out.  