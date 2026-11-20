*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Book form can be opened from the home page
    Go To  ${HOME_URL}
    Click  text=Add source
    Click  text=Book
    Get Title  ==  Add book
    Get Text  h2  ==  Add a book

Return home after adding a book
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     Robert C. Martin
    Fill Text  [name="title"]      Clean Code
    Fill Text  [name="publisher"]  Prentice Hall
    Fill Text  [name="year"]       2008
    Click  button >> text=Add book
    Get Url  ==  ${HOME_URL}/

Book is not added when required field is empty
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]  Robert C. Martin
    Click  button >> text=Add book
    Get Url  ==  ${HOME_URL}/new_book

Book is not added when year is not a number
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     Robert C. Martin
    Fill Text  [name="title"]      Clean Code
    Fill Text  [name="publisher"]  Prentice Hall
    Type Text  [name="year"]       abcd
    Click  button >> text=Add book
    Get Url  ==  ${HOME_URL}/new_book
