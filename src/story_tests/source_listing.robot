*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Source listing can be opened from the home page
    Go To  ${HOME_URL}
    Click  text=Source listing
    Get Url  ==  ${HOME_URL}/source_listing
    Get Title  ==  Source Listing
    Get Text  h2  ==  Source Listing

Message is shown when there are no sources
    Go To  ${HOME_URL}/source_listing
    Get Text  body  *=  No sources available.
    
Added book is shown in the source listing
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     Robert C. Martin
    Fill Text  [name="title"]      Clean Code
    Fill Text  [name="publisher"]  Prentice Hall
    Fill Text  [name="year"]       2008
    Click  button >> text=Add book
    
    Go To  ${HOME_URL}/source_listing
    Get Text  .references dd:nth-of-type(1)  ==  book
    Get Text  .references dd:nth-of-type(2)  ==  Robert C. Martin
    Get Text  .references dd:nth-of-type(3)  ==  Clean Code
    Get Text  .references dd:nth-of-type(4)  ==  Prentice Hall
    Get Text  .references dd:nth-of-type(5)  ==  2008
