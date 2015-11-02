import sys
import imaplib
import getpass
import email
import email.header
import datetime
import csv

EMAIL_ACCOUNT = "wli2@wellesley.edu"
EMAIL_FOLDER = "[Gmail]/Sent Mail"
after_date = "01-Jan-2015"

def process_mailbox(M):
    """
    Scrap your "sent mail" folder and keep track of who you talk to.
    """

    rv, data = M.search(None,'SINCE', after_date,'SEEN')
    if rv != 'OK':
        print "No messages found!"
        return

    existed=[] #keep track of existed senders

    #write header for a csv file
    outputfile = open('data.csv','wt')
    writer = csv.writer(outputfile)
    writer.writerow(('receiver_id','average_time','last_time','replied?','remind?')) #headers

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        try:
            subject = unicode(decode[0],'utf-8')
        except UnicodeDecodeError:
            print "UnicodeDecodeError"

        raw_date = msg['Date']
        sender_id = msg['From']
        receiver_id = msg['To']

        print "title",subject
        print "sender",sender_id
        print "date",raw_date
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))

            LocalDate = local_date.strftime("%a, %d %b %Y %H:%M:%S")

        #write a new row into a csv
        writer.writerow((receiver_id,0,raw_date,'N','N')) #default

M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)

print rv, data

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print "Processing %s ...\n" %EMAIL_FOLDER
    process_mailbox(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv

M.logout()