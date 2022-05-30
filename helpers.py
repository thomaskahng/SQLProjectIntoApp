class Helpers:
    def __init__(self):
        # Table, array, and column to select things from and selection action
        self.table_to_select = ""
        self.table_cols = []
        self.all_or_one_col = ""

        # Table to delete things from and deletion action
        self.table_to_delete = ""
        self.delete_action = ""

        # Table to insert things into
        self.table_to_insert = ""
        self.ins_table_cols = []

    def reset_columns_vals(self):
        # Reset columns helper values
        self.table_to_select = ""
        self.table_cols = []
        self.all_or_one_col = ""

    def reset_delete_vals(self):
        # Reset delete helper values
        self.table_to_delete = ""
        self.delete_action = ""

    def reset_insert_vals(self):
        # Reset insert helper values
        self.table_to_insert = ""
        self.ins_table_cols = []