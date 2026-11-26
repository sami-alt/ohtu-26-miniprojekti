*** Settings ***
Library  Browser

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      500ms
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chromium
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Reset Database
    Go To  ${RESET_URL}

Add Source
    [Arguments]    ${type}    ${citation_key}    &{fields}
    Go To  ${HOME_URL}/new_source?type=${type}
    Fill Text  [name="citation_key"]  ${citation_key}
    FOR  ${name}  ${value}  IN  &{fields}
        Fill Text  [name="${name}"]  ${value}
    END
    Click  form[method="post"] button

Add Tricky Book
    Add Source  book  oberg500
    ...  author=Åsa Öberg and Seán O'Brien
    ...  title=Tips & Tricks: 100% C# for $5 in snake_case
    ...  publisher=Allen & Unwin
    ...  year=-500

BibTeX Should Contain Tricky Book
    [Arguments]    ${bibtex}
    Should Contain  ${bibtex}  @book{oberg500,
    Should Contain  ${bibtex}  author = {Åsa Öberg and Seán O'Brien}
    Should Contain  ${bibtex}  title = {Tips \\& Tricks: 100\\% C\\# for \\$5 in snake\\_case}
    Should Contain  ${bibtex}  publisher = {Allen \\& Unwin}
    Should Contain  ${bibtex}  year = {-500}
