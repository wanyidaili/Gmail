from mailbox import mbox
import random
import pandas as pd


def generate():

    # store training label by making a dataframe of sentbox's subjects
    def store_subject(message, body=None):
        if not body:
            body = message.get_payload(decode=True)
        if len(message):
            contents = {
                "subject": message['subject'] or "",
                "from": message['from'],
                "to": message['to'],
                "date": message['date'],
            }
            return dfsent.append(contents, ignore_index=True)

    sentbox = mbox('Sent.mbox')

    # Create an empty DataFrame with the relevant columns
    dfsent = pd.DataFrame(columns=("subject", "from", "to", "date"))

    fails = []
    for message in sentbox:
        try:
            #figure out if it has been replied or not
            if message.get_content_type() == 'text/plain':
                dfsent = store_content(message)
            elif message.is_multipart():
                # Grab any plaintext from multipart messages
                for part in message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        dfsent = store_subject(message, part.get_payload(decode=True))
                        break
        except:
            fails.append(message)

    print "Finished storing subjects from sent emails."

    # This method is written to store Inbox messages into a DataFrame
    def store_content(message, body=None):
        if not body:
            body = message.get_payload(decode=True)
        if len(message):
            #first figure out if this email has been replied or not:
            label = -1 # assume it has not been replied
            for j in range(dfsent.shape[0]):
                if message['subject'] in dfsent.loc[j,'subject']:
                    if message['from'] in dfsent.loc[j,'to']:
                        label = 1 # it is replied
                        break
            contents = {
                "subject": message['subject'] or "",
                "body": body,
                "from": message['from'],
                "to": message['to'],
                "date": message['date'],
                "label": label
            }
            return contents


    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # Create an empty DataFrame with the relevant columns
    dftraining = pd.DataFrame(
        columns=("subject", "body", "from", "to", "date","label"))
    dfvalidation = pd.DataFrame(
        columns=("subject", "body", "from", "to", "date","label"))
    dftesting = pd.DataFrame(
        columns=("subject", "body", "from", "to", "date","label"))

    # Import your downloaded mbox file: inbox
    box = mbox('Inbox.mbox')

    # # Let pt of the inbox emails goe into training, pv-pt validation, 1-pv testing.
    # p = 0.2
    # pt = 0.5 * p #randomly select 10%of inbox data
    # pv = 0.75 * p

    # Instead of selecting randomly, I should select by dates

    fails = []
    for message in box:
        r = random.random() # a floating number between 0 and 1
        try:
            if 'wli2' not in message['from']: # this is only for incoming emails
                if message.get_content_type() == 'text/plain':
                    #if r <= pt:
                    #if 'Nov 2015' in message['date']: 
                    if 'Oct 2015' in message['date'] or 'Sep 2015' in message['date']:
                        contents = store_content(message)
                        dftraining = dftraining.append(contents, ignore_index=True)
                    #elif r<= pv:
                    #elif 'Oct 2015' in message['date'] or 'Sep 2015' in message['date']:
                    elif 'Nov 2015' in message['date']: 
                        contents = store_content(message)
                        dfvalidation = dfvalidation.append(contents, ignore_index=True)
                    #elif r<= p:
                    elif 'Dec 2015' in message['date']:
                        contents = store_content(message)
                        dftesting = dftesting.append(contents, ignore_index=True)
                elif message.is_multipart():
                    # Grab any plaintext from multipart messages
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            #if r <= pt:
                            #if 'Nov 2015' in message['date']:
                            if 'Oct 2015' in message['date'] or 'Sep 2015' in message['date']:
                                contents = store_content(message, part.get_payload(decode=True))
                                dftraining = dftraining.append(contents, ignore_index=True)
                                break
                            #elif r <= pv:
                            #elif 'Oct 2015' in message['date'] or 'Sep 2015' in message['date']:
                            elif 'Nov 2015' in message['date']:
                                contents = store_content(message, part.get_payload(decode=True))
                                dfvalidation = dfvalidation.append(contents, ignore_index=True)
                                break
                            #elif r <= p:
                            elif 'Dec 2015' in message['date']:
                                contents = store_content(message, part.get_payload(decode=True))
                                dftesting = dftesting.append(contents, ignore_index=True)
                                break
        except:
            fails.append(message)

    print "Finished creating inbox database with labels"


    return dfsent, dftraining, dfvalidation, dftesting
