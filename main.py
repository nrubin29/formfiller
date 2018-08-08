from lib import TextFormElement, SelectFormElement, ButtonFormElement, FormFiller

elements = [
    TextFormElement(name='firstNameTextBox', val='Noah'),
    TextFormElement(name='lastNameTextBox', val='Rubin'),
    TextFormElement(name='emailTextBox', val='noah@my.site'),
    TextFormElement(name='phoneTextBox', val='800-555-1234'),
    SelectFormElement(name='booksDropDownList', val='Selenium RC'),
    ButtonFormElement(id='osRadioButtonList_2'),
    ButtonFormElement(id='registerButton')
]

form_filler = FormFiller('http://seleniummaster.com/seleniumformtest/registrationform.aspx', elements)
form_filler.run()

print('Done!')
