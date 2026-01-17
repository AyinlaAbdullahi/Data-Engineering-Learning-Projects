"""
Simple Data Cleaning Pipeline
A beginner-friendly script to clean CSV data
"""
import pandas as pd
import logging

# basic logging setup
logging.basicConfig(
    filename='cleaning.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def clean_data(input_file, output_file):
    """
    Clean the CSV data and save results
    
    input_file: path 
    
    to raw CSV
    output_file: path to save cleaned CSV
    """
    logging.info("=" * 50)
    logging.info("Starting data cleaning pipeline")
    
    # Step 1: Load the data
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    original_rows = len(df)
    print(f"Loaded {original_rows} rows")
    logging.info(f"Loaded {original_rows} rows from {input_file}")
    
    # Step 2: Remove duplicate rows
    print("Removing duplicates...")
    before_dup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dup - len(df)
    print(f"Removed {duplicates_removed} duplicate rows")
    logging.info(f"Removed {duplicates_removed} duplicate rows")
    
    # Step 3: Handle missing values
    print("Handling missing values...")
    missing_count = df.isnull().sum().sum()
    
    if missing_count > 0:
        print(f"Found {missing_count} missing values")
        logging.info(f"Found {missing_count} missing values")
        
        # Fill numeric columns with median
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                logging.info(f"Filled missing values in {col} with median")
        
        # Fill text columns with 'unknown'
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            if df[col].isnull().any():
                df[col].fillna('unknown', inplace=True)
                logging.info(f"Filled missing values in {col} with 'unknown'")
    else:
        print("No missing values found")
        logging.info("No missing values found")
    
    # Step 4: Clean text data
    print("Cleaning text columns...")
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].astype(str).str.strip().str.lower() #Remove space and make lowercase
    logging.info(f"Cleaned {len(text_columns)} text columns")
    
    # Step 5: Remove rows with negative values in key columns
    print("Validating numeric data...")
    columns_to_check = ['requests_per_second', 'cpu_utilization_percent', 'mmemory_utilization_percent']
    for col in columns_to_check:
        if col in df.columns:
            before = len(df)
            df = df[df[col] >= 0]
            removed = before - len(df)
            if removed > 0:
                print(f"Removed {removed} rows with negative {col}")
                logging.info(f"Removed {removed} rows with negative {col}")
    
    # Step 6: Save cleaned data
    final_rows = len(df)
    df.to_csv(output_file, index=False)
    print(f"\nCleaning complete!")
    print(f"Original rows: {original_rows}")
    print(f"Final rows: {final_rows}")
    print(f"Rows removed: {original_rows - final_rows}")
    print(f"Cleaned data saved to: {output_file}")
    print(f"Check cleaning.log for details")
    
    logging.info(f"Final dataset: {final_rows} rows")
    logging.info(f"Saved cleaned data to {output_file}")
    logging.info("Pipeline completed successfully")
    logging.info("=" * 50)


if __name__ == "__main__":
    #file paths here
    INPUT_FILE = "distributed_system_architecture_stress_dataset.csv"
    OUTPUT_FILE = "cleaned_data.csv"
    
    # Run the cleaning
    clean_data(INPUT_FILE, OUTPUT_FILE)

    
 