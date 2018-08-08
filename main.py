from lib import TextFormElement, ButtonFormElement, FormFiller, FormBatch, SleepElement

form_batch = FormBatch('https://www.e-oscar-web.net/EntryController?trigger=Login', [
    FormFiller([
        TextFormElement(id='companyId', val='RegID'),
        TextFormElement(id='userId', val='UserID'),
        TextFormElement(id='password', val='password'),
        ButtonFormElement(id='securityMsgAck1'),
        SleepElement(3),  # For demonstration purposes only. Fills in info and then waits 3 seconds.
        ButtonFormElement(selector='.loginBtn')
    ]),
    FormFiller([
        TextFormElement(id='companyId', val='RegID2'),
        TextFormElement(id='userId', val='UserID2'),
        TextFormElement(id='password', val='password2'),
        ButtonFormElement(id='securityMsgAck1'),
        SleepElement(3),
        ButtonFormElement(selector='.loginBtn')
    ])
])
form_batch.run()

print('Done!')
