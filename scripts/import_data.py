import subprocess
import pandas as pd
import time

# Helper to run shell commands and capture output
def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}\n{result.stderr}")
        exit(1)
    return result.stdout.strip()

print("Starting data import...")

# 1. Import Accounts
print("Importing Accounts...")
run_command('sf data bulk ingest Account -f Account.csv --json --wait 10')
time.sleep(5)  # Wait for data commit

# 2. Query Account Ids and Names
print("Querying AccountIds...")
account_query = run_command('sf data query "SELECT Id, Name FROM Account" --json')
account_data = pd.read_json(account_query)['result']['records']
account_map = {acc['Name']: acc['Id'] for acc in account_data}

# 3. Prepare Contact CSV with AccountId instead of AccountName
contacts_df = pd.read_csv('Contact.csv')
contacts_df['AccountId'] = contacts_df['AccountName'].map(account_map)
contacts_df.drop(columns=['AccountName'], inplace=True)
contacts_df.to_csv('Contact_for_import.csv', index=False)

# 4. Import Contacts
print("Importing Contacts...")
run_command('sf data bulk ingest Contact -f Contact_for_import.csv --json --wait 10')
time.sleep(5)

# 5. Query Contact Ids and Emails
print("Querying ContactIds...")
contact_query = run_command('sf data query "SELECT Id, Email FROM Contact" --json')
contact_data = pd.read_json(contact_query)['result']['records']
contact_map = {con['Email']: con['Id'] for con in contact_data}

# 6. Prepare Opportunity CSV with AccountId and ContactId instead of AccountName and ContactEmail
opp_df = pd.read_csv('Opportunity.csv')
opp_df['AccountId'] = opp_df['AccountName'].map(account_map)
opp_df['ContactId'] = opp_df['ContactEmail'].map(contact_map)
opp_df.drop(columns=['AccountName', 'ContactEmail'], inplace=True)
opp_df.to_csv('Opportunity_for_import.csv', index=False)

# 7. Import Opportunities
print("Importing Opportunities...")
run_command('sf data bulk ingest Opportunity -f Opportunity_for_import.csv --json --wait 10')

print("Data import complete!")
