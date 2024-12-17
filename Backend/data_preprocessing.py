import pandas as pd

file_path = './Assignment1.xlsx'

accounts = pd.read_excel(file_path, sheet_name='Accounts')
policies = pd.read_excel(file_path, sheet_name='Policies')
claims = pd.read_excel(file_path, sheet_name='Claims')


accounts['Pincode'] = accounts['Pincode'].fillna(0).astype(int)  # Convert Pincode to integer
accounts['Name'] = accounts['Name'].str.title()  
accounts['City'] = accounts['City'].fillna("NA")  
accounts['State'] = accounts['State'].fillna("NA")  

# Clean Policies
policies['Policy Name'] = policies['Policy Name'].str.title()  


# Clean Claims
claims['BillAmount'] = claims['BillAmount'].fillna(0)  
claims['Status'] = claims['Status'].str.capitalize() 
claims['HAN'] = claims['HAN'].fillna("NA")  


def check_missing(data, name):
    print(f"Missing values in {name}:")
    print(data.isnull().sum())
    print("\n")

check_missing(accounts, "Accounts")
check_missing(policies, "Policies")
check_missing(claims, "Claims")


def check_duplicates(data, name):
    duplicates = data.duplicated().sum()
    print(f"Number of duplicates in {name}: {duplicates}\n")

check_duplicates(accounts, "Accounts")
check_duplicates(policies, "Policies")
check_duplicates(claims, "Claims")


def summarize_data(data, name):
    print(f"Summary statistics for {name}:")
    print(data.describe())
    print("\n")

summarize_data(accounts, "Accounts")
summarize_data(claims, "Claims")

output_path = './Processed_Assignment1.xlsx'
with pd.ExcelWriter(output_path) as writer:
    accounts.to_excel(writer, sheet_name='Accounts', index=False)
    policies.to_excel(writer, sheet_name='Policies', index=False)
    claims.to_excel(writer, sheet_name='Claims', index=False)

print(f"Cleaned dataset with multiple sheets saved to {output_path}")
