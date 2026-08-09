# project_5_the_nook
A full stack e-commerce project that allows authors to publish their own books and for readers to buy them.

## Bugs

| Title | Description | Fix | Status |
|-------|-------------|-----|--------|
| Book model tests failing | The test for when a reviewer is deleted books they reviewed should remain failed. | This was due to outstanding migrations in the book model. Applying the migrations resolved the issue. Tests were re-run and all passed. | Resolved |
| Account templates not loading | A number of the account template pages were failing to load. | The issue was caused by crispy forms not being loaded in the templates. Added {% load crispy_forms_tags %} to the affected pages. | Resolved |
| Genre link not working in the nav bar | The genre link in the nav bar just took users to the book list. | Updated the genre link to show filters. | Resolved |
| Home/tests.py not running all tests | Home/tests.py was only running 17 out of 18 tests. | The issue was caused by incorrect indention. Outdented the impacted test. | Resolved |