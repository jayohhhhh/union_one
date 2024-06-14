import pandas as pd
import numpy as np
import re
from word2number import w2n
from datetime import datetime

def load_data(file_path):
    return pd.read_csv(file_path)

def handle_duplicates(df): # Drops duplicate member_id rows, keeps first
    df = df.drop_duplicates(subset='member_id', keep='first')
    return df
# NOTE: we can preserve these duplicates but the statistics may appear skewed. Another option is to create new unique member_id's but we run the risk of id conflicts if these members are already stored in database.


def handle_nulls(df): # Fills null values in 'first_name' column to "first_name" as a placeholder
    df['first_name'] = df['first_name'].fillna('first_name')
    return df

def fix_date_format(df):
    # Converts 'start_date' column to datetime format, handling errors
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    if df['start_date'].isnull().any():
        print("Warning: Some dates could not be converted and are set to NaT")
    print(f"start_date dtype after conversion: {df['start_date'].dtype}")  # Debugging line
    return df

def convert_written_to_number(text):
    try:
        # Check if text is numeric
        if pd.notna(text) and re.match(r'^-?\d+(?:,\d+)?(?:\.\d+)?$', text.strip()):
            return float(text.replace(',', ''))  # Convert numeric text to float

        # Convert written numbers to actual numbers using word2number library
        return w2n.word_to_num(text) if text != 'NaN' else None
    
    except ValueError:
        return text  # Return original text if conversion fails

def convert_salaries(df):
    # Convert mixed numbers and written numbers to actual numbers in 'salary' column
    df['salary'] = df['salary'].apply(convert_written_to_number)
    return df

def calculate_length_worked(df, current_date=None): # Create a column showing length of years worked
    if current_date is None:
        current_date = pd.to_datetime(datetime.now())
    # Calculate length worked in years
    df['length_worked_yrs'] = (current_date - pd.to_datetime(df['start_date'])).dt.days / 365.25
    
    # Handle cases where 'start_date' might be NaT (Not a Time)
    df['length_worked_yrs'] = df['length_worked_yrs'].fillna(0)
    return df

def remove_salary_placeholders(df):
    # Remove placeholder salaries to avoid skewed statistics in salary analysis.
    df = df[df['salary'] != 50000]
    return df

def set_index(df): # Set 'member_id' column as index
    df.set_index('member_id', inplace=True)
    return df

def save_cleaned_data(df, output_path):
    df.to_csv(output_path, index=True)
    return df

def main(input_path, output_path):
    # main function to clean the data
    print("Loading data...")
    df = load_data(input_path)
    print("Handling duplicates...")
    df = handle_duplicates(df)
    print("Handling null values...")
    df = handle_nulls(df)
    print("Fixing date format...")
    df = fix_date_format(df)
    print("Converting written numbers to numeric...")
    df = convert_salaries(df)
    print("Creating length worked column")
    df = calculate_length_worked(df)
    print("Removing salary placeholders")
    df = remove_salary_placeholders(df)
    print("Setting member_id as index...")
    df = set_index(df)
    print("Saving cleaned data...")
    save_cleaned_data(df, output_path)
    print("Data cleaning complete.")

if __name__ == "__main__":
    # Replace 'path_to_your_input_file.csv' and 'path_to_your_output_file.csv' with the actual paths to your input and output files
    input_path = 'census.csv'
    output_path = 'cleaned_census.csv'
    main(input_path, output_path)
    
# Run "python cleaning_script.py" in your powershell after changing the input_path & output_path above.