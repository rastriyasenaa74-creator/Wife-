import os, json, smtplib
from email.message import EmailMessage
from datetime import datetime
from zoneinfo import ZoneInfo

today = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
with open("messages.json", encoding="utf-8") as f:
    messages=json.load(f)
with open("state.json", encoding="utf-8") as f:
    state=json.load(f)

if state["last_sent_date"] == today:
    print("Already sent today."); raise SystemExit(0)

i=int(state.get("next_index",0)) % len(messages)
msg=EmailMessage()
msg["Subject"]="Good Morning ❤️"
msg["From"]=os.environ["MAIL_USERNAME"]
msg["To"]=os.environ["RECIPIENT_EMAIL"]
msg.set_content(messages[i])

with smtplib.SMTP("smtp.gmail.com",587,timeout=30) as s:
    s.starttls()
    s.login(os.environ["MAIL_USERNAME"],os.environ["MAIL_PASSWORD"])
    s.send_message(msg)

state={"last_sent_date":today,"next_index":(i+1)%len(messages)}
with open("state.json","w",encoding="utf-8") as f:
    json.dump(state,f,indent=2)
print(f"Sent message {i+1}/365")
