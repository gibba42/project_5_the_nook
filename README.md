# project_5_the_nook
A full stack e-commerce project that allows authors to publish their own books and for readers to buy them.

## Bugs

| Title | Description | Fix | Status |
|-------|-------------|-----|--------|
| Book model tests failing | The test for when a reviewer is deleted books they reviewed should remain failed. | This was due to outstanding migrations in the book model. Applying the migrations resolved the issue. Tests were re-run and all passed. | Resolved |
| Account templates not loading | A number of the account template pages were failing to load. | The issue was caused by crispy forms not being loaded in the templates. Added {% load crispy_forms_tags %} to the affected pages. | Resolved |