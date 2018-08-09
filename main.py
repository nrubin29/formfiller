from lib import TextFormElement, ButtonFormElement, FormFiller, FormBatch, SleepElement, FileFormFiller

form_batch = FormBatch('https://www.e-oscar-web.net/EntryController?trigger=Login', [
    # First we need to log in. We don't need to use a file for this.
    FormFiller([
        TextFormElement(id='companyId', val='RegID'),
        TextFormElement(id='userId', val='UserID'),
        TextFormElement(id='password', val='password'),
        ButtonFormElement(id='securityMsgAck1'),
        SleepElement(3),  # For demonstration purposes only. Fills in info and then waits 3 seconds.
        ButtonFormElement(selector='.loginBtn')
    ]),
    # Now we want to submit the form a bunch of times. Let's read from a file.
    FileFormFiller('sample.csv', [
        TextFormElement(id='companyId'),
        TextFormElement(id='userId'),
        TextFormElement(id='password'),
        ButtonFormElement(id='securityMsgAck1'),
        SleepElement(3),
        ButtonFormElement(selector='.loginBtn')
    ])
])
form_batch.run()

print('Done!')
