# The Nook

The Nook is a full-stack e-commerce application designed to help readers discover and purchase books from independent authors.

Readers can browse and search a curated catalogue, view detailed book and author information, add books to their basket, complete purchases securely and leave reviews. Registered authors can create an author profile and submit their books for consideration, while staff members review listings before they become available in the public catalogue.

The submitted application is designed as a controlled bookshop rather than an unrestricted multi-vendor marketplace. The Nook manages the catalogue and sales process while giving independent authors a platform through which they can showcase their work. This approval process helps maintain a consistent standard across the catalogue and gives readers confidence in the books being offered.

The application is built using Django. It includes authentication, role-based author and staff functionality, user-owned account information, catalogue management and Stripe payment processing.

## Live Site

- Live site: **To be added following deployment**
- Repository: [The Nook GitHub Repository](https://github.com/gibba42/project_5_the_nook)

## Bugs

| Title | Description | Fix | Status |
|-------|-------------|-----|--------|
| Book model tests failing | The test for when a reviewer is deleted books they reviewed should remain failed. | This was due to outstanding migrations in the book model. Applying the migrations resolved the issue. Tests were re-run and all passed. | Resolved |
| Account templates not loading | A number of the account template pages were failing to load. | The issue was caused by crispy forms not being loaded in the templates. Added {% load crispy_forms_tags %} to the affected pages. | Resolved |
| Genre link not working in the nav bar | The genre link in the nav bar just took users to the book list. | Updated the genre link to show filters. | Resolved |
| Home/tests.py not running all tests | Home/tests.py was only running 17 out of 18 tests. | The issue was caused by incorrect indention. Outdented the impacted test. | Resolved |
