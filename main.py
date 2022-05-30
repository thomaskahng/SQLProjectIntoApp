import mysql.connector
from flask import Flask, render_template, request
from database import Database
from helpers import Helpers

# Driver object and authority
app = Flask(__name__)
authorized = False

# Database class and database connection
my_db = None
database_class = None
helpers = None

@app.route("/", methods=['GET', 'POST'])
def authenticate():
    global my_db, authorized, database_class, helpers

    # If authorized, database connection, and class object declared, reset everything
    if authorized and database_class is not None and my_db is not None:
        database_class.reset()

        # Reset helper variables
        helpers.reset_insert_vals()
        helpers.reset_columns_vals()
        helpers.reset_delete_vals()

        database_class = None
        authorized = False
        my_db = None
        helpers = None

    if request.method == "POST":
        # Get fields from user for database name and authentication
        host = str(request.form.get("host"))
        user = str(request.form.get("user"))
        password = str(request.form.get("password"))
        database = str(request.form.get("database"))

        # No password if password is "none"
        if password == "none":
            password = ""

        # Run database connection and catch errors
        try:
            # Connect database with inputs, authorize database, and make class object
            my_db = mysql.connector.connect(host=host, user=user, password=password, database=database)
            authorized = True
            database_class = Database(my_db, database)
            helpers = Helpers()

            # Go to columns page
            return render_template("columns.html", table_names=database_class.table_names, chosen_table="",
                               table_chosen=False, column_names=[], chosen_column="", column_chosen=False)

        # Catch errors and stay home
        except:
            return render_template("home.html")
            
    return render_template("home.html")

@app.route("/columns", methods=['GET', 'POST'])
def columns():
    global database_class, authorized, helpers

    # If authorized and valid database object, load column page with necessary data, else go home
    if authorized and database_class is not None and helpers is not None:
        # Reset supplemental values sent to front end
        helpers.reset_columns_vals()

        return render_template("columns.html", table_names=database_class.table_names, chosen_table="",
                               row_nums=[], column_names=[], chosen_column="", table_display={})
    else:
        return render_template("home.html")

@app.route("/show_from_table", methods=['GET', 'POST'])
def show_from_table():
    global database_class, authorized, helpers

    # If authorized and valid database object, load column page with necessary data, else go home
    if authorized and database_class is not None and helpers is not None:
        if request.method == "POST":
            # Get table to select, columns from that table (nested dict) and list of column names
            helpers.table_to_select = str(request.form.get("table"))
            columns_of_table = dict(database_class.table_columns[helpers.table_to_select])
            helpers.table_cols = list(columns_of_table.keys())

            # Reload page with table names and chosen table sent to front end
            return render_template("columns.html", table_names=database_class.table_names, chosen_table=helpers.table_to_select,
                                   row_nums=[], column_names=helpers.table_cols, chosen_column="", table_display={})

        # Just reload page (change nothing)
        return render_template("columns.html", table_names=database_class.table_names, chosen_table="",
                               row_nums=[], column_names=[], chosen_column="", table_display={})
    else:
        return render_template("home.html")

@app.route("/show_column", methods=['GET', 'POST'])
def show_column():
    global database_class, authorized, helpers

    # If authorized and valid database object, load column page with necessary data, else go home
    if authorized and database_class is not None and helpers is not None:
        if request.method == "POST":
            # Get name of column and its table (nested dictionary) in dictionary
            helpers.all_or_one_col = str(request.form.get("column"))
            table_display = dict(database_class.table_columns[helpers.table_to_select])

            if helpers.all_or_one_col != "ALL (*)":
                # Get a new dictionary, find the row(s) of that column
                new_table = {}
                new_table_display = table_display[helpers.all_or_one_col]

                # Col/row is key/value pair and table is updated
                new_table[helpers.all_or_one_col] = new_table_display
                table_display = new_table

            # Get number of rows, dictionary to store each row, and list of row numbers
            len_dict = len(list(table_display.values())[0])
            table_by_row = {}
            row_nums = []

            for i in range(0, len_dict):
                new_list = []

                # If all rows, get each row element at each column
                if helpers.all_or_one_col == "ALL (*)":
                    for col_name in helpers.table_cols:
                        new_list.append(table_display[col_name][i])

                # Else get row element at selected column
                else:
                    new_list.append(table_display[helpers.all_or_one_col][i])

                # Enter into dictionary as a list of elements at row, then append row number to its list
                table_by_row[i] = new_list
                row_nums.append(i)

            # Reload page with chosen column, row numbers, and rows of table to display sent to front end
            return render_template("columns.html", table_names=database_class.table_names, chosen_table=helpers.table_to_select,
                                   row_nums=row_nums, column_names=helpers.table_cols, chosen_column=helpers.all_or_one_col, table_display=table_by_row)

        # Just reload page (change nothing)
        return render_template("columns.html", table_names=database_class.table_names, chosen_table=helpers.table_to_select,
                               row_nums=[], column_names=helpers.table_cols, chosen_column="", table_display={})
    else:
        return render_template("home.html")


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    global database_class, authorized, helpers

    # If authorized and valid database object, load delete page with necessary data, else go home
    if authorized and database_class is not None and helpers is not None:
        # If table to be deleted from and delete action are defined
        if helpers.table_to_delete != "" and helpers.delete_action != "":
            # See if we delete first row or all rows
            if helpers.delete_action == "Delete first row":
                database_class.delete_top(helpers.table_to_delete)
            elif helpers.delete_action == "Delete all rows":
                database_class.delete_table(helpers.table_to_delete)

        # Reset supplemental values sent to front end
        helpers.reset_delete_vals()

        # Reload page
        return render_template("delete.html", table_names=database_class.table_names, chosen_table="",
                               table_chosen=False, table_erase="")
    else:
        return render_template("home.html")

@app.route("/delete_table", methods=['GET', 'POST'])
def delete_table():
    global database_class, authorized, helpers

    # If valid, load delete page and necessary data, else go home
    if authorized and database_class is not None and helpers is not None:
        if request.method == "POST":
            # Get table to delete and indicate chosen table as True
            helpers.table_to_delete = str(request.form.get("table"))

            # Send chosen table to front end
            return render_template("delete.html", table_names=database_class.table_names, chosen_table=helpers.table_to_delete,
                                   table_chosen=True, table_erase="")

        # Just reload page (change nothing)
        return render_template("delete.html", table_names=database_class.table_names, chosen_table="",
                               table_chosen=False, table_erase="")

    else:
        return render_template("home.html")

@app.route("/deletion", methods=['GET', 'POST'])
def deletion():
    global database_class, authorized, helpers

    # If valid, load delete page and necessary data, else go home
    if authorized and database_class is not None and helpers is not None:
        if request.method == "POST":
            # Get delete action
            helpers.delete_action = str(request.form.get("action"))
            table_erased = False

            # Evaluate if we need to delete whole table
            if helpers.delete_action == "Delete all rows":
                table_erased = True

            # Get delete action and send indicated delete action as True
            return render_template("delete.html", table_names=database_class.table_names, chosen_table=helpers.table_to_delete,
                                   table_chosen=False, table_erase=helpers.delete_action, erase_chosen=table_erased)

        # Just reload page (change nothing)
        return render_template("delete.html", table_names=database_class.table_names, chosen_table="",
                               table_chosen=False, table_erase="", erase_chosen=False)

    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)