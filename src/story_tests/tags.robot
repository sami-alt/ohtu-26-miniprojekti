*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***

Tag can be added by tag windod
    Go ${HOME_URL}
    ${references}=  Get Text  .references
    Should Contain  ${references}  book
    Should Contain  ${references}  Robert C. Martin
    Should Contain  ${references}  Clean Code
    Should Contain  ${references}  Prentice Hall
    Should Contain  ${references}  2008
    
