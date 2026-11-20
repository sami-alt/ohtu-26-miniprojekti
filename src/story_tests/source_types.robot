*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Add source opens the source type selection page
    [Tags]  story18
    Go To  ${HOME_URL}
    Click  text=Add source
    Get Url  ==  ${HOME_URL}/new_source
    Get Text  h2  ==  Select source type
    Get Text  body  *=  Book
    Get Text  body  *=  Journal article
    Get Text  body  *=  Conference paper

Each source type opens its matching form
    [Tags]  story18
    Go To  ${HOME_URL}/new_source
    Click  text=Book
    Get Title  ==  Add book
    Get Text  h2  ==  Add a book

    Go To  ${HOME_URL}/new_source
    Click  text=Journal article
    Get Title  ==  Add a journal article
    Get Text  h2  ==  Add a journal article

    Go To  ${HOME_URL}/new_source
    Click  text=Conference paper
    Get Title  ==  Add a conference paper
    Get Text  h2  ==  Add a conference paper

Each source form can return to source type selection
    [Tags]  story18
    Go To  ${HOME_URL}/new_book
    Click  text=Back to source types
    Get Url  ==  ${HOME_URL}/new_source

    Go To  ${HOME_URL}/new_article
    Click  text=Back to source types
    Get Url  ==  ${HOME_URL}/new_source

    Go To  ${HOME_URL}/new_inproceedings
    Click  text=Back to source types
    Get Url  ==  ${HOME_URL}/new_source

Selecting source types does not add a source
    [Tags]  story18
    Go To  ${HOME_URL}/new_source
    Click  text=Book
    Go To  ${HOME_URL}/new_source
    Click  text=Journal article
    Go To  ${HOME_URL}/new_source
    Click  text=Conference paper
    Go To  ${HOME_URL}
    Get Text  body  *=  No sources available.
