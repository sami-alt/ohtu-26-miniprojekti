*** Settings ***
Resource  resource.robot
Library   OperatingSystem
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Keywords ***
Source Is Exported As BibTeX
    [Arguments]    ${type}    ${citation_key}    &{fields}
    Reset Database
    Add Source  ${type}  ${citation_key}  &{fields}
    Go To  ${HOME_URL}/export
    ${bibtex}=  Get Property  id=bibtex  value
    Should Contain  ${bibtex}  @${type}{${citation_key},
    FOR  ${name}  ${value}  IN  &{fields}
        Should Contain  ${bibtex}  ${name} = {${value}}
    END

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

Export without sources shows message
    Go To  ${HOME_URL}
    Click  text=Export BibTeX
    Get Url  ==  ${HOME_URL}/
    Get Text  .flashes  *=  No sources to export.

Export page shows saved sources as BibTeX
    Add Tricky Book
    Click  text=Export BibTeX
    Get Url  ==  ${HOME_URL}/export
    ${bibtex}=  Get Property  id=bibtex  value
    BibTeX Should Contain Tricky Book  ${bibtex}

Every source type is exported as BibTeX
    [Template]  Source Is Exported As BibTeX
    book           martin08
    ...            author=Robert C. Martin
    ...            title=Clean Code
    ...            publisher=Prentice Hall
    ...            year=2008
    article        hochreiter97
    ...            author=Sepp Hochreiter and Jürgen Schmidhuber
    ...            title=Long Short-Term Memory
    ...            journal=Neural Computation
    ...            year=1997
    ...            volume=9
    ...            number=8
    ...            pages=1735--1780
    inproceedings  beck89
    ...            author=Kent Beck and Ward Cunningham
    ...            title=A Laboratory for Teaching Object-Oriented Thinking
    ...            booktitle=OOPSLA '89
    ...            year=1989

Export page copies BibTeX to clipboard
    Add Tricky Book
    Grant Permissions  clipboard-read  clipboard-write
    Go To  ${HOME_URL}/export
    Click  button >> text=Copy to clipboard
    Get Text  id=copy-status  ==  Copied!
    ${clipboard}=  Evaluate JavaScript  ${None}  navigator.clipboard.readText()
    BibTeX Should Contain Tricky Book  ${clipboard}

Export page downloads a bib file
    Add Tricky Book
    Go To  ${HOME_URL}/export
    ${download}=  Promise To Wait For Download  ${OUTPUT DIR}/references.bib
    Click  text=Download .bib file
    ${file}=  Wait For  ${download}
    Should Be Equal  ${file.suggestedFilename}  references.bib
    ${content}=  Get File  ${file.saveAs}
    BibTeX Should Contain Tricky Book  ${content}

Export page combines multiple books into one BibTeX output
    Add Source  book  martin08  author=Robert C. Martin  title=Clean Code  publisher=Prentice Hall  year=2008
    Add Source  book  hunt99  author=Andrew Hunt  title=The Pragmatic Programmer  publisher=Addison-Wesley  year=1999
    Click  text=Export BibTeX
    ${bibtex}=  Get Property  id=bibtex  value
    Should Contain  ${bibtex}  @book{martin08,
    Should Contain  ${bibtex}  @book{hunt99,
    Should Contain  ${bibtex}  title = {Clean Code}
    Should Contain  ${bibtex}  title = {The Pragmatic Programmer}
