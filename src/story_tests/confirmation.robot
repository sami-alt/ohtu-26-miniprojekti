*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Successful book addition shows a confirmation message
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     Ada Lovelace
    Fill Text  [name="title"]      A book
    Fill Text  [name="publisher"]  Publisher
    Fill Text  [name="year"]       2024
    Click  button >> text=Add book
    Get Text  .flash-success  ==  Book added successfully.

Successful article addition shows a confirmation message
    Go To  ${HOME_URL}/new_article
    Fill Text  [name="author"]   Grace Hopper
    Fill Text  [name="title"]    An article
    Fill Text  [name="journal"]  Journal
    Fill Text  [name="year"]     2025
    Click  button >> text=Add article
    Get Text  .flash-success  ==  Article added successfully.

Successful conference paper addition shows a confirmation message
    Go To  ${HOME_URL}/new_inproceedings
    Fill Text  [name="author"]     Alan Turing
    Fill Text  [name="title"]      A paper
    Fill Text  [name="booktitle"]  Proceedings
    Fill Text  [name="year"]       2026
    Click  button >> text=Add a conference paper
    Get Text  .flash-success  ==  Conference paper added successfully.

Deleting a source asks for confirmation
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     Ada Lovelace
    Fill Text  [name="title"]      A book to delete
    Fill Text  [name="publisher"]  Publisher
    Fill Text  [name="year"]       2024
    Click  button >> text=Add book

    Handle Future Dialogs  action=dismiss
    Click  .references button.danger
    Get Text  .references  *=  A book to delete

    Handle Future Dialogs  action=accept
    Click  .references button.danger
    Get Text  body  *=  No sources available.
