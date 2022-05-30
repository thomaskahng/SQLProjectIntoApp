class Database:
    def __init__(self, db, database_name):
        # Cursor to navigate database and database name
        self.cursor = db.cursor()
        self.database_name = database_name.upper()

        # List of table names, dictionary of table sizes
        # Also dictionary of table columns nested with a dictionary of column name and values
        self.table_names = []
        self.table_sizes = {}
        self.table_columns = {}
        #
        self.query = ""

        # Get the tables, table sizes, table's column names, and table's columns' contents
        self.get_tables()
        self.get_table_sizes()
        self.get_column_names()
        self.get_column_contents()

    def get_tables(self):
        # Execute result of showing tables
        self.cursor.execute("SHOW TABLES;")
        my_result = self.cursor.fetchall()

        # Split by ' (used to find table name) and append the capitalized table name
        for x in my_result:
            line = str(x).split("'")
            table_name = line[1].upper()
            self.table_names.append(table_name)

    def get_table_sizes(self):
        for table_name in self.table_names:
            # Fetch query of table name
            self.cursor.execute(f'SELECT * FROM {table_name};')
            my_result = self.cursor.fetchall()

            # Get size of table and append to dictionary of table sizes
            table_len = len(my_result)
            self.table_sizes[table_name] = table_len

    def get_column_names(self):
        for table_name in self.table_names:
            # Fetch query of table name and make a empty dictionary of column names
            self.cursor.execute(f'SELECT * FROM {table_name};')
            my_result = self.cursor.fetchall()
            col_dict = {}

            for row in self.cursor.description:
                # Get name of column and put into column name dictionary with empty list value
                col_name = row[0]
                col_dict[col_name] = []

            # Sub dictionary is value of table name
            self.table_columns[table_name] = col_dict

    def get_column_contents(self):
        for table_name in self.table_names:
            # Fetch query of table name and nested dict value of table of such name
            self.cursor.execute(f'SELECT * FROM {table_name};')
            my_result = self.cursor.fetchall()
            cols = self.table_columns[table_name]

            # Iterator to traverse column names and store it in array by index ordering
            col_int = 0
            col_arr = []

            for col in cols:
                # Store in array of column names with 0th indexing
                col_arr.append(col)
                col_int += 1

            for res in my_result:
                # For each tuple value from query, find necessary index corresponding column
                # Get that corresponding column name and add tuple value to that corresponding column
                for j in range(0, len(col_arr)):
                    into_col = col_arr[j]
                    cols[into_col].append(res[j])

    def delete_top(self, table_name):
        # Table name to delete rows in
        table_name = table_name.upper()

        if table_name in self.table_names:
            # Table size and columns if table name is valid
            table_size = self.table_sizes[table_name]
            table_value = self.table_columns[table_name]

            # Table has to have elements
            if table_size > 0:
                # New table size, then delete first row
                self.table_sizes[table_name] = table_size - 1
                self.cursor.execute(f"DELETE FROM {table_name} LIMIT {1};")

                # Substring each column of table by leaving off first 'n' values
                for column in table_value:
                    values = table_value[column]
                    values = values[1:table_size]

    def delete_table(self, table_name):
        # Table name to delete rows in
        table_name = table_name.upper()

        if table_name in self.table_names:
            # Table size and columns if table name is valid
            table_size = self.table_sizes[table_name]
            table_value = self.table_columns[table_name]

            # Table should have elements to be cleared
            if table_size > 0:
                # Table size is 0 and all elements deleted
                self.table_sizes[table_name] = 0
                self.cursor.execute(f"DELETE FROM {table_name};")

            # Clear each column of its values
            for column in table_value:
                values = table_value[column]
                values.clear()

    def reset(self):
        # Reset all data structures
        self.table_names = []
        self.table_columns = {}
        self.table_lengths = {}