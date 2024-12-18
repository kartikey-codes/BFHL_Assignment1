# Assignment 1: FastAPI-based Python Application

## Features
- **CRUD Operations**: Perform Create, Read, Update, and Delete operations on customer, policy, and claims data.
- **Data Cleaning and EDA**: Handle uncleaned data, perform exploratory data analysis, and clean the data before usage.
- **Pydantic Validation**: Ensure strict data validation for API request bodies.
- **Exception Handling**: Provide meaningful error messages with appropriate HTTP status codes.
- **Change Tracking**: Maintain a separate dataframe tracking history of changes, including Primary Key and timestamps.
- **Logging**: Implement effective logging for debugging and monitoring using loguru.
- **Deployment**: Dockerized for easy deployment.

## Application Endpoints
### Base URL:
```
https://bfhl-assignment1.onrender.com
```

### API Documentation:
- Swagger UI: [https://bfhl-assignment1.onrender.com](https://bfhl-assignment1.onrender.com)
- Additional API Testing: [https://egjbhccggb.apidog.io/health-check-12590959e0](https://egjbhccggb.apidog.io/health-check-12590959e0)

### Key Endpoints
1. **Fetch Customer Information**: Retrieve customer details, their policies, and claims data using `AccountId`.
2. **Add/Delete Records**: Add or delete claims, policies, or customers while maintaining data relationships.
3. **Update Records**: Update any record and track changes in a history dataframe.
4. **Export Data**: Export all dataframes (original and updated) into a single Excel file with multiple sheets.

## Development Process
### Key Highlights
1. **Proper Validation**:
   - Validates relationships between datasets.
   - For example, when updating the `account_id` in the claims sheet, the system checks if the `account_id` exists in the customer sheet.

2. **Logging with Loguru**:
   - All critical operations are logged for debugging and monitoring.
   - Logs include timestamps, error details, and operational messages.

3. **Dockerized Deployment**:
   - The project is fully Dockerized, ensuring consistent deployment environments.

4. **Exception Handling**:
   - Proper error messages with HTTP response codes.
   - Handles cases like missing records, invalid data formats, or failed operations.