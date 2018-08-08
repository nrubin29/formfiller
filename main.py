from selenium import webdriver

from lib import TextFormElement, SelectFormElement, ButtonFormElement

elements = [
    TextFormElement(name='firstNameTextBox', val='Noah'),
    TextFormElement(name='lastNameTextBox', val='Rubin'),
    TextFormElement(name='emailTextBox', val='noah@my.site'),
    TextFormElement(name='phoneTextBox', val='800-555-1234'),
    SelectFormElement(name='booksDropDownList', val='Selenium RC'),
    ButtonFormElement(id='osRadioButtonList_2'),
    ButtonFormElement(id='registerButton')
]

options = webdriver.ChromeOptions()
# options.headless = True  # If true, it'll run in the background and not show the Chrome window.

driver = webdriver.Chrome(options=options)
driver.get('http://seleniummaster.com/seleniumformtest/registrationform.aspx')

for element in elements:
    element.run(driver)

print('Done!')
