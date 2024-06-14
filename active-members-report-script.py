import pandas as pd
import os

def load_data(file_path): # Load data from csv file
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
def analyze_active_members(df): # Group actively working employees by employer & calculate active member percentages
    grouped = df.groupby('employer')['actively_working'].value_counts().unstack()
    grouped['active_%'] = grouped[True] / (grouped[True] + grouped[False]) * 100

    # Rename columns for clarity
    grouped.columns = ['actively_working', 'not_working', 'active_%']
    return grouped

def save_to_excel(df, output_path): # Save dataframe to Excel file
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=True)
        print(f"Report saved to {output_path}")
    except Exception as e:
        print(f"Error saving report: {e}")
        
def main(input_path, output_path): # Main function to load data, analyze, and save report
    df = load_data(input_path)
    analysis_result = analyze_active_members(df)
    save_to_excel(analysis_result, output_path)
    
if __name__ == "__main__":
    # Replace 'path_to_your_input_file.csv' and 'path_to_your_output_file.xlsx' with actual paths
    input_path = 'cleaned_census.csv'
    output_path = 'reports/active-members-report.xlsx'
    main(input_path, output_path)