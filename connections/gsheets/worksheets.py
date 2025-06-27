from utils.helpers import helper_functions as helpers
from tqdm import tqdm
import pandas as pd
import config


class GsheetsWorksheets:

    def __init__(self, client):
        """Initialize a Worksheet manager.
        https://docs.gspread.org/en/latest/
        """
        self.client = client

    def get_data(self, sheet_name, include_row_numbers=False):
        """Get data from a Google Sheets worksheet as a pandas DataFrame.
        Args:
            sheet_name (str): Name of the worksheet to get data from.
            include_row_numbers (bool): Whether to include Gsheets row numbers in the DataFrame.
        Returns:
            A pandas DataFrame with data or an Error dict if an error occurs.
        """
        try:
            print(f'ℹ️  Downloading all the data from {sheet_name} Google Sheets...')
            self.client.worksheet = self.client._handle_request(
                self.client.sheet.worksheet,
                sheet_name
            )
            data = self.client._handle_request(
                self.client.worksheet.get_all_values
            )
            
            df = pd.DataFrame(data[1:], columns=data[0])  # First row as header

            if include_row_numbers:
                df.insert(0, 'Row Number', range(2, len(df) + 2)) # GSheets rows start at 2

            return df
        
        except Exception as e:
            return {'success': False, 'error': e}

    def batch_update_from_a_list(self, worksheet_name, updates, start_column='A', num_columns=5):
        """Batch update multiple rows in a worksheet.
        Args:
            worksheet_name (str): Name of the worksheet to update
            updates (list): List of tuples containing (row_number, value1, value2, ...)
            start_column (str, optional): Starting column letter. Defaults to 'A'.
            num_columns (int, optional): Number of columns to update. Defaults to 5.
        Returns:
            int: Number of rows updated or Error dict if an error occurs.
        """
        try:
            worksheet = self.get_worksheet(worksheet_name)
            batch_data = helpers.build_batch_data(updates, start_column, num_columns)

            if batch_data:
                print(f'ℹ️  Batch updating data to Worksheet {worksheet_name}...')
                self.client._handle_request(worksheet.batch_update, batch_data)
                return len(updates)
            else:
                return 0
            
        except Exception as e:
            return {'success': False, 'error': e}

    def batch_copy_rows(self, source_name, target_name, values_df, remove_from_source=False):
        """Batch transfer rows from one worksheet to another.
        Args:
            source_name (str): Name of the source worksheet
            target_name (str): Name of the target worksheet
            values_df (pd.DataFrame): DataFrame containing the values to move
            remove_from_source (bool): Whether to remove rows from the source worksheet after copying
        Returns:
            int: Number of rows moved or Error dict if an error occurs.
        """
        try:
            source_ws = self._get_worksheet(source_name)
            target_ws = self._get_worksheet(target_name)

            values_to_append = self._prepare_values(values_df)

            if not values_to_append:
                return 0
            
            self._ensure_target_size(target_ws, len(values_to_append))

            print(f'ℹ️  Copying data to {target_name} Google Sheets...')
            self._append_batch_data(target_ws, values_to_append)

            if remove_from_source:
                self._delete_rows(source_ws, values_df['Row Number'].tolist())

            return len(values_to_append)

        except Exception as e:
            return {'success': False, 'error': e}

    def batch_update_data(self, worksheet_name, df):
        """Batch remove current data and save new data to a Google Sheets worksheet.
        Args:
            worksheet_name (str): Name of the worksheet to save the data to
            df (pd.DataFrame): DataFrame containing the data to save
        Returns:
            int|dict: DataFrame length if successful, or an Error dict if an error occurs.
        """
        try:
            # Transform the data to match Google Sheets format
            worksheet = self._get_worksheet(worksheet_name)

            # Convert all values to String
            # It ensures that more complex data gets saved to GSheets (e.g. dicts, lists)
            # without any error
            df_string = df.astype(str)
            headers = df_string.columns.values.tolist()
            values = self._prepare_values(df_string)
            all_values = [headers] + values

            worksheet.clear()
            print(f'ℹ️  Saving data to {worksheet_name}...')
            worksheet.update(all_values)

            return len(values)

        except Exception as e:
            return {'success': False, 'error': e}

    def batch_remove_data(self, source_worksheet_name, updates_row_number_list):
        """Batch remove rows from a worksheet.
        Args:
            source_worksheet_name (str): Name of the worksheet to remove rows from
            updates_row_number_list (list): List of row numbers to remove
        Returns:
            int|dict: A number of removed offers, or an Error dict if an error occurs.
        """
        source_worksheet = self._get_worksheet(source_worksheet_name)

        try:
            count = self._delete_rows(source_worksheet, updates_row_number_list)
            return count
        
        except Exception as e:
            return {'success': False, 'error': e}

    # Helper functions

    def _get_worksheet(self, worksheet_name):
        print(f'ℹ️  Downloading data from Worksheet {worksheet_name}...')
        return self.client._handle_request(self.client.sheet.worksheet, worksheet_name)
    
    def _build_batch_data(self, updates, start_column, num_columns):
        """Build batch data for updating multiple rows in a worksheet."""

        # Calculate the last column letter (up to 26 columns)
        # Watch out: It works if the letters are before Z
        end_column = self.calculate_end_column(start_column, num_columns)
        batch_data = []

        for row_data in updates:
            row_number = row_data[0]
            values = row_data[1:]

            batch_data.append({
                'range': f"{start_column}{row_number}:{end_column}{row_number}",
                'values': [list(values)]
            })
        return batch_data

    def _calculate_end_column(self, start_column, num_columns):
        return chr(ord(start_column.upper()) + num_columns - 1)
    
    def _prepare_values(self, df):
        """Drops Row numbers and extracts values from DataFrame."""
        if 'Row Number' in df.columns:
            df = df.drop('Row Number', axis=1)
        return df.values.tolist()

    def _ensure_target_size(self, worksheet, rows_to_add):
        """Return next free row in the worksheet, resizing if necessary."""
        current_rows = len(self.client._handle_request(worksheet.get_all_values))
        needed_rows = current_rows + rows_to_add

        if needed_rows > current_rows:
            self.client._handle_request(worksheet.resize, rows=needed_rows)
        return current_rows + 1  # Return next free row

    def _append_batch_data(self, worksheet, values):
        start_row = len(self.client._handle_request(worksheet.get_all_values)) + 1
        batch_data = [{'range': f'A{start_row}', 'values': values}]
        self.client._handle_request(worksheet.batch_update, batch_data)
        
    def _delete_rows(self, worksheet, row_numbers):
        """Delete rows in reverse order to avoid index shifting issues.
        Returns a number of removed offers"""
        row_numbers = sorted(row_numbers, reverse=True)

        print(f'ℹ️  Removing rows from {worksheet} Google Sheets...')
        for row in tqdm(row_numbers, desc="Deleting rows", unit=" row"):
            self.client._handle_request(worksheet.delete_rows, int(row))

        return len(row_numbers)
