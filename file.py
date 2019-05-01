import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

users = client.open("maildart users").sheet1
emails = client.open("maildart emails").sheet1
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

running = True
logged_in = False


def checkUnreads(user):

    unread = 0

    for email in email_list:
        if email["to"] == user and email["read"] == 0:
            unread += 1

    return unread


def sendMessage(recipient, sender, message):

    time = datetime.datetime.now().strftime("%a, %b %d, %Y" + " at " + "%I:%M:%S %p")
    email = [recipient, sender, message, time, 0]
    emails.append_row(email)


def createUser(user, password):

    newuser = [user, password]
    users.append_row(newuser)


def getLogin(user, password):

    success = 0

    for line in user_data:
        if str(line["username"]) == str(user) and str(line["password"]) == str(password):
            success += 1

    if success > 0:
        return True
    else:
        return False


def checkExisting(user):

    success = 0

    for username in users.col_values(1):
        if username == user:
            success += 1

    if success > 0:
        return True
    else:
        return False


while running:

    user_data = users.get_all_records()
    email_list = emails.get_all_records()

    if not logged_in:

        choice = str(input("new account or login:\n"))

        if choice[0] == "n":

            new_user = str(input("Enter your desired username:\n"))

            while checkExisting(new_user):

                new_user = str(input("Name already taken. Try another one:\n"))

            new_pass = str(input("Enter your desired password:\n"))

            createUser(new_user, new_pass)

            logged_in = True

            session = new_user

        if choice[0] == "l":

            user = input("enter username:\n")
            password = input("enter password:\n")

            logged_in = getLogin(user, password)

            session = user

    if logged_in:

        print("\nyou have ",checkUnreads(session)," unread emails.")

        choice = input("unreads, inbox, outbox, send or logout:\n")

        if choice[0] == "s":

            new_to = input("who ya sending to?:\n")

            while not checkExisting(new_to):

                new_to = input("couldn't find user. try again:\n")

            new_from = session
            new_text = input("enter your message:\n")

            send = input("send? y/n\n")

            if send == "y":

                sendMessage(new_to, new_from, new_text)

            else:

                print('message deleted.')

        if choice[0] == "l":

            print("logged out.")

            logged_in = False

        if choice[0] == "i":

            display = []

            row = 1

            for email in email_list:

                row += 1

                if email['to'] == session:

                    display.append(email)

            for email in display:

                print("\n    message from",email["from"],"on",email["time"])
                print("   ", email["message"])

        if choice[0] == "o":

            display = []

            row = 1

            for email in email_list:

                row += 1

                if email['from'] == session:

                    display.append(email)

            for email in display:

                print("\n    message to",email["to"],"on",email["time"])
                print("   ", email["message"])

        if choice[0] == "u":

            if checkUnreads(session) == 0:
                print("no new messages.")

            else:
                display = []

                row = 1

                for email in email_list:

                    row += 1

                    if email['to'] == session and email['read'] == 0:

                        display.append(email)
                        emails.update_cell(row, 5, 1)

                for email in display:

                    print("\n    message from",email["from"],"on",email["time"])
                    print("   ", email["message"])
