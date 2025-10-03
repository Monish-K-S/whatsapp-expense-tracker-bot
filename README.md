WhatsApp Expense Tracker Bot
A WhatsApp bot to help you track expenses and manage budgets directly from your phone.

Features 🚀
add <amount> <category> <description> - Log a new expense.

list - See your last 5 expenses.

total - Get your total spending for the month.

setbudget <amount> - Set a monthly budget.

budgetstatus - Check your budget status.

resetbudget - Clear this month's budget.

How to Set Up 🛠️
1. Prepare Google Sheets
Create a Google Sheet named My Expenses.

Make two tabs: Expenses and Budgets.

Set up columns in the Expenses tab: UserID, Timestamp, Amount, Category, Description.

Set up columns in the Budgets tab: UserID, MonthYear, BudgetAmount.

Go to the Google Cloud Console, enable the Drive and Sheets APIs, and create a Service Account.

Download the JSON key, rename it to credentials.json, and place it in your project folder.

Share your Google Sheet with the client_email from the JSON file, giving it "Editor" access.

2. Set Up Your Project
Create a folder for your project and place the app.py and credentials.json files inside.

Open a terminal in the folder and run these commands:

Bash

# Create a virtual environment
python -m venv venv

# Activate it (on Windows)
venv\Scripts\activate

# Install required packages
pip install Flask gspread oauth2client pandas twilio


3. Run the Bot
Run the app from your terminal:

Bash

python app.py
Run ngrok in a new terminal to get a public URL:

Bash

ngrok http 5000
Update your webhook. Copy the https:// URL from ngrok, add /webhook to the end, and paste it into your WhatsApp provider's (e.g., Twilio) settings.
