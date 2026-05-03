import imaplib
import email
import os
import asyncio
import base64

from python.agents.extraction.process import extration_agent_process
from python.knowledgebase.db import vector_search
from python.agents.approval.process import approval_agent_process

from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

try:
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)
    # mail.select("inbox")
    print("Gmail connection created")
except Exception as ex:
    print("Gmail connection failed:", ex)
    
    
async def realtime_reading_emails():
    try:
        while True:
            try:
                mail.select("inbox")
                status, messages = mail.search(None, '(UNSEEN SUBJECT "purchase order")')
                print("new email search: ", status)
            except Exception as ex:
                print("new email searching failed:", ex)
            
            
            if messages[0]:
                print(len(messages[0]), "found")
                
                for num in messages[0].split():
                    status, msg_data = mail.fetch(num, '(RFC822)')
                    
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    print("checking attachemnets for email:", msg["Subject"])

                    for part in msg.walk():
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            
                            if filename.endswith(".pdf"):
                                file_bytes = part.get_payload(decode=True)
                                
                                #agent process 
                                if file_bytes:
                                    response = await extration_agent_process(file_bytes)
                                    if response:
                                        result = await vector_search(response)
                                        approve_res = await approval_agent_process(response, result)
                                            
                            else:
                                print(filename, "is not a pdf")
                                continue
                            
            else:
                print("No new emails found. try again after 10sec")
                await asyncio.sleep(10)
                continue
            
    except Exception as e:
        print("realtime reading proccess failed:", e)
        
