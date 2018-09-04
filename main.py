from file_lib import Spreadsheet, FileFormFiller, UpdateSpreadsheetColumn
from lib import TextFormElement, ButtonFormElement, FormFiller, FormBatch, SleepElement

# We create a reference to our spreadsheet so that we can fill data from it and update it.
data = Spreadsheet('sample.csv')

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
    # Now we want to submit the form a bunch of times. Let's use our spreadsheet.
    FileFormFiller(data, [
        # We can update the spreadsheet with data from the form.
        # Here, we are updating the AUD column for each row to be the text of the #aud element.
        UpdateSpreadsheetColumn(column_name='AUD', id='aud'),
        TextFormElement(id='companyId'),
        TextFormElement(id='userId'),
        TextFormElement(id='password'),
        ButtonFormElement(id='securityMsgAck1'),
        SleepElement(3),
        ButtonFormElement(selector='.loginBtn')
    ])
])
form_batch.run()

# After updating some column, make sure to save the data back to the file.
data.save()

print('Done!')
