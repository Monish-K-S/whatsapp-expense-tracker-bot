from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Google Sheets Authentication ---
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("My Expenses").sheet1



@app.route('/webhook', methods=['POST'])
def webhook():
    
    incoming_msg = request.values.get('Body', '').strip()

    
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    
    parts = incoming_msg.split()
    command = parts[0].lower() 
    try:
        if command == 'add':
            
            amount = float(parts[1])
            category = parts[2]
            description = ' '.join(parts[3:])

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_row = [timestamp, amount, category, description]
            sheet.append_row(new_row)

            msg.body(f"✅ Expense logged: ₹{amount:.2f} for {category} ({description}).")
            responded = True

        elif command == 'list':
            records = sheet.get_all_records()
            if not records:
                msg.body("No expenses logged yet. Use 'add <amount> <category> ...' to start.")
            else:
                last_5 = records[-5:]
                response_text = "Your last 5 expenses:\n"
                for record in reversed(last_5): 
                    response_text += f"- ₹{record['Amount']:.2f} on {record['Category']} ({record['Timestamp'].split()[0]})\n"
                msg.body(response_text.strip())
            responded = True

        elif command == 'total':
            records = sheet.get_all_records()
            if not records:
                msg.body("No expenses to total yet!")
            else:
                df = pd.DataFrame(records)
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                current_month = datetime.now().month
                current_year = datetime.now().year

                month_df = df[(df['Timestamp'].dt.month == current_month) & (df['Timestamp'].dt.year == current_year)]
                total = month_df['Amount'].sum()

                msg.body(f"Total expenses for September 2025: ₹{total:.2f}")
            responded = True

        elif command == 'help':
            help_text = "Available commands:\n" \
                        "1. *add <amount> <category> <description>*\n" \
                        "   (e.g., add 250 groceries milk)\n" \
                        "2. *list* - Shows last 5 expenses.\n" \
                        "3. *total* - Shows total for the current month."
            msg.body(help_text)
            responded = True

    except Exception as e:
        msg.body(f"Oops! Something went wrong. Make sure your command is correct. For help, type 'help'.")
        responded = True


    if not responded:
        msg.body("Sorry, I don't understand that command. Type 'help' to see what I can do.")

    return str(resp)



if __name__ == '__main__':
    app.run(port=5000)