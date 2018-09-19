from file_lib import Spreadsheet
from lib import TextFormElement, ButtonFormElement, SleepElement, Form

# We create a reference to our spreadsheet so that we can fill data from it and update it.
spreadsheet = Spreadsheet('sample.csv')

# To begin, we load the form on the supplied URL.
# This is just the starting point, so the URL will change as we navigate around.
form = Form('https://www.e-oscar-web.net/EntryController?trigger=Login')

# First we need to log in.
form.fill([
    TextFormElement(id='companyId', val='RegID'),
    TextFormElement(id='userId', val='UserID'),
    TextFormElement(id='password', val='password'),
    ButtonFormElement(id='securityMsgAck1'),
    SleepElement(3),  # For demonstration purposes only. Fills in info and then waits 3 seconds.
    ButtonFormElement(selector='.loginBtn')
])

with form.frame('topFrame'):
    form.fill([
        ButtonFormElement(id='AUDButton')
    ])

# Clicking the .loginBtn will cause the form to submit and we'll be navigated to a new page.
# Now we want to submit the form a bunch of times. Let's use our spreadsheet.
for row in spreadsheet.rows:
    #  We can update the spreadsheet with data from the form.
    #  Here, we are updating the AUD column of each row to be the text of the #aud element.
    row.set('AUD', form.get_text(id='aud'))

    # Because we are using fill_from_row, the elements will automatically get their values from the spreadsheet
    # for the current row and at the column specified by the `col` field.
    form.fill_from_row(row, [
        TextFormElement(id='companyId', col='Company ID'),
        TextFormElement(id='userId', col='User ID'),
        TextFormElement(id='password', col='Password'),
        ButtonFormElement(id='securityMsgAck1'),
        SleepElement(3),
        ButtonFormElement(selector='.loginBtn')
    ])

# After updating the spreadsheet, make sure to save it back to the file.
spreadsheet.save()

print('Done!')
