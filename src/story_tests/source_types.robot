*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Add source opens the source type selector
    [Tags]  story18
    Go To  ${HOME_URL}
    Click  text=Add source
    Get Url  ==  ${HOME_URL}/new_source
    Get Text  h2  ==  Select source type
    ${selector_states}=  Get Element States  id=source_type
    Should Contain  ${selector_states}  visible
    Get Element Count  id=source_type >> option  ==  4

Each source type opens its matching form
    [Tags]  story18
    Go To  ${HOME_URL}/new_source
    Select Options By  id=source_type  label  Book
    Click  text=Continue
    Get Title  ==  Add book
    Get Text  h2  ==  Add a book
    ${action}=  Get Attribute  form[method="post"]  action
    Should Be Equal  ${action}  /create_source/book

    Go To  ${HOME_URL}/new_source
    Select Options By  id=source_type  label  Journal article
    Click  text=Continue
    Get Title  ==  Add a journal article
    Get Text  h2  ==  Add a journal article
    ${action}=  Get Attribute  form[method="post"]  action
    Should Be Equal  ${action}  /create_source/article

    Go To  ${HOME_URL}/new_source
    Select Options By  id=source_type  label  Conference paper
    Click  text=Continue
    Get Title  ==  Add a conference paper
    Get Text  h2  ==  Add a conference paper
    ${action}=  Get Attribute  form[method="post"]  action
    Should Be Equal  ${action}  /create_source/inproceedings

Each source form can return to source type selection
    [Tags]  story18
    Go To  ${HOME_URL}/new_source?type=book
    Click  text=Back to source types
    Get Url  ==  ${HOME_URL}/new_source
    Get Text  h2  ==  Select source type

    Go To  ${HOME_URL}/new_source?type=article
    Click  text=Back to source types
    Get Url  ==  ${HOME_URL}/new_source
    Get Text  h2  ==  Select source type

    Go To  ${HOME_URL}/new_source?type=inproceedings
    Click  text=Back to source types
    Get Url  ==  ${HOME_URL}/new_source
    Get Text  h2  ==  Select source type

Selecting source types does not add a source
    [Tags]  story18
    Go To  ${HOME_URL}
    Click  text=Add source
    Select Options By  id=source_type  label  Book
    Click  text=Continue
    Select Options By  id=source_type  label  Journal article
    Click  text=Continue
    Select Options By  id=source_type  label  Conference paper
    Click  text=Continue
    Go To  ${HOME_URL}
    Get Text  body  *=  No sources available.
