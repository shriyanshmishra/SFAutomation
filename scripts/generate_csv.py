import pandas as pd

# Load the Excel file (replace 'real_estate_data.xlsx' with your Excel file path)
excel_file = 'real_estate_data.xlsx'

# Read the single sheet with all data
df = pd.read_excel(excel_file)

# Filter rows where Project is 'Real Estate'
df = df[df['Project'] == 'Real Estate']

# Separate dataframes by Object type
accounts_df = df[df['Object'] == 'Account'][['Name/FirstName', 'Industry', 'Phone']].copy()
accounts_df = accounts_df.rename(columns={'Name/FirstName': 'Name'})

contacts_df = df[df['Object'] == 'Contact'][['Name/FirstName', 'LastName', 'Email', 'AccountName']].copy()
contacts_df = contacts_df.rename(columns={'Name/FirstName': 'FirstName'})

opportunities_df = df[df['Object'] == 'Opportunity'][['Name/FirstName', 'Stage', 'CloseDate', 'Amount', 'AccountName', 'ContactEmail']].copy()
opportunities_df = opportunities_df.rename(columns={'Name/FirstName': 'Name'})

# Remove duplicate accounts by Name
accounts_df = accounts_df.drop_duplicates(subset=['Name'])

# Save to CSV files
accounts_df.to_csv('Account.csv', index=False)
contacts_df.to_csv('Contact.csv', index=False)
opportunities_df.to_csv('Opportunity.csv', index=False)

print("CSV files generated: Account.csv, Contact.csv, Opportunity.csv")
