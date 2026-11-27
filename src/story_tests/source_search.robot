*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
Source filtering controls are available on the home page
    [Tags]  story17
    Go To  ${HOME_URL}
    ${field_states}=  Get Element States  select[name="field"]
    Should Contain  ${field_states}  visible
    ${value_states}=  Get Element States  input[name="value"]
    Should Contain  ${value_states}  visible
    Get Text  body  *=  Clear filters
    FOR  ${field}  IN  author  title  publisher  year  journal  volume  number  pages  booktitle  type
        Get Element Count  select[name="field"] >> option[value="${field}"]  ==  1
    END

Sources can be filtered by author
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  author
    Fill Text  input[name="value"]  Mira AuthorNorth
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by title
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  title
    Fill Text  input[name="value"]  FilterBookAlpha
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by year
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  year
    Fill Text  input[name="value"]  2032
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by article volume
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  volume
    Fill Text  input[name="value"]  FilterVolumeBeta42
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by article number
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  number
    Fill Text  input[name="value"]  FilterIssueBeta7
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by pages
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  pages
    Fill Text  input[name="value"]  FilterArticlePages101-109
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by book publisher
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  publisher
    Fill Text  input[name="value"]  FilterPressAlpha
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by journal
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  journal
    Fill Text  input[name="value"]  FilterJournalBeta
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterPaperGamma

Sources can be filtered by conference booktitle
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  booktitle
    Fill Text  input[name="value"]  FilterMeetingGamma
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterPaperGamma
    Should Not Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterArticleBeta

Sources can be filtered by source type
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  type
    Fill Text  input[name="value"]  book
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterBookAlpha
    Should Not Contain  ${references}  FilterArticleBeta
    Should Not Contain  ${references}  FilterPaperGamma

Multiple filters show only sources matching every condition
    [Tags]  story17
    Add combined filter fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"] >> nth=0  value  author
    Fill Text  input[name="value"] >> nth=0  FilterSharedAuthor
    Click  text=Add filter
    Select Options By  select[name="field"] >> nth=1  value  year
    Fill Text  input[name="value"] >> nth=1  2041
    Click  text=Search
    ${references}=  Get Text  .references
    Should Contain  ${references}  FilterAndMatch
    Should Not Contain  ${references}  FilterAndWrongYear
    Should Not Contain  ${references}  FilterAndWrongAuthor

Clear filters restores the complete source listing
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  author
    Fill Text  input[name="value"]  Mira AuthorNorth
    Click  text=Search
    ${filtered_references}=  Get Text  .references
    Should Contain  ${filtered_references}  FilterBookAlpha
    Should Not Contain  ${filtered_references}  FilterArticleBeta
    Click  text=Clear filters
    ${all_references}=  Get Text  .references
    Should Contain  ${all_references}  FilterBookAlpha
    Should Contain  ${all_references}  FilterArticleBeta
    Should Contain  ${all_references}  FilterPaperGamma

An empty result shows a no matching sources message
    [Tags]  story17
    Add filtering source fixtures
    Go To  ${HOME_URL}
    Select Options By  select[name="field"]  value  author
    Fill Text  input[name="value"]  NoMatchingAuthor2044
    Click  text=Search
    Get Text  body  *=  No matching sources found.

*** Keywords ***
Add filtering source fixtures
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     Mira AuthorNorth
    Fill Text  [name="title"]      FilterBookAlpha
    Fill Text  [name="publisher"]  FilterPressAlpha
    Fill Text  [name="year"]       2031
    Click  button >> text=Add book

    Go To  ${HOME_URL}/new_article
    Fill Text  [name="author"]   Niko AuthorSouth
    Fill Text  [name="title"]    FilterArticleBeta
    Fill Text  [name="journal"]  FilterJournalBeta
    Fill Text  [name="year"]     2032
    Fill Text  [name="volume"]   FilterVolumeBeta42
    Fill Text  [name="number"]   FilterIssueBeta7
    Fill Text  [name="pages"]    FilterArticlePages101-109
    Click  button >> text=Add article

    Go To  ${HOME_URL}/new_inproceedings
    Fill Text  [name="author"]     Oona AuthorWest
    Fill Text  [name="title"]      FilterPaperGamma
    Fill Text  [name="booktitle"]  FilterMeetingGamma
    Fill Text  [name="year"]       2033
    Click  css=form[action*="inproceedings"] button[type="submit"]

Add combined filter fixtures
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="author"]     FilterSharedAuthor
    Fill Text  [name="title"]      FilterAndMatch
    Fill Text  [name="publisher"]  FilterAndPublisher
    Fill Text  [name="year"]       2041
    Click  button >> text=Add book

    Go To  ${HOME_URL}/new_article
    Fill Text  [name="author"]   FilterSharedAuthor
    Fill Text  [name="title"]    FilterAndWrongYear
    Fill Text  [name="journal"]  FilterAndJournal
    Fill Text  [name="year"]     2042
    Click  button >> text=Add article

    Go To  ${HOME_URL}/new_inproceedings
    Fill Text  [name="author"]     FilterOtherAuthor
    Fill Text  [name="title"]      FilterAndWrongAuthor
    Fill Text  [name="booktitle"]  FilterAndConference
    Fill Text  [name="year"]       2041
    Click  css=form[action*="inproceedings"] button[type="submit"]
