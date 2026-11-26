*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Message is shown when there are no sources
    Go To  ${HOME_URL}
    Get Text  body  *=  No sources available.
    
Added book is shown in the source listing
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="citation_key"]  martin08
    Fill Text  [name="author"]        Robert C. Martin
    Fill Text  [name="title"]         Clean Code
    Fill Text  [name="publisher"]     Prentice Hall
    Fill Text  [name="year"]          2008
    Click  button >> text=Add book  
    
    Go To  ${HOME_URL}
    ${references}=  Get Text  .references
    Should Contain  ${references}  martin08
    Should Contain  ${references}  book
    Should Contain  ${references}  Robert C. Martin
    Should Contain  ${references}  Clean Code
    Should Contain  ${references}  Prentice Hall
    Should Contain  ${references}  2008
