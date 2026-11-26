*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Citation key is shown in source
    Go To  ${HOME_URL}/new_source?type=book
    Fill Text  [name="citation_key"]  martin08
    Fill Text  [name="author"]        Robert C. Martin
    Fill Text  [name="title"]         Clean Code
    Fill Text  [name="publisher"]     Prentice Hall
    Fill Text  [name="year"]          2008
    Click  button >> text=Add book
    ${references}=  Get Text  .references
    Should Contain  ${references}  martin08

Empty citation key is rejected
    Go To  ${HOME_URL}/new_source?type=book
    Fill Text  [name="author"]        Robert C. Martin
    Fill Text  [name="title"]         Clean Code
    Fill Text  [name="publisher"]     Prentice Hall
    Fill Text  [name="year"]          2008
    Click  button >> text=Add book
    Get Title  ==  Add book

Invalid citation key is rejected
    Go To  ${HOME_URL}/new_source?type=book
    Fill Text  [name="citation_key"]  €£$
    Fill Text  [name="author"]        Robert C. Martin
    Fill Text  [name="title"]         Clean Code
    Fill Text  [name="publisher"]     Prentice Hall
    Fill Text  [name="year"]          2008
    Click  button >> text=Add book
    Get Title  ==  Add book

Dual citation keys are rejected
    Go To  ${HOME_URL}/new_source?type=book
    Fill Text  [name="citation_key"]  martin08
    Fill Text  [name="author"]        Robert C. Martin
    Fill Text  [name="title"]         Clean Code
    Fill Text  [name="publisher"]     Prentice Hall
    Fill Text  [name="year"]          2008
    Click  button >> text=Add book
    Go To  ${HOME_URL}/new_source?type=book
    Fill Text  [name="citation_key"]  martin08
    Fill Text  [name="author"]        Robert C. Martin
    Fill Text  [name="title"]         Clean Code
    Fill Text  [name="publisher"]     Prentice Hall
    Fill Text  [name="year"]          2008
    Click  button >> text=Add book
    Get Title  ==  Add source
    Get Text  .flashes  *=  An entry with this citation key already exists!