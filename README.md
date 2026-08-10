# The Nook

The Nook is a full-stack e-commerce application designed to help readers discover and purchase books from independent authors.

Readers can browse and search a curated catalogue, view detailed book and author information, add books to their basket, complete purchases securely and leave reviews. Registered authors can create an author profile and submit their books for consideration, while staff members review listings before they become available in the public catalogue.

The submitted application is designed as a controlled bookshop rather than an unrestricted multi-vendor marketplace. The Nook manages the catalogue and sales process while giving independent authors a platform through which they can showcase their work. This approval process helps maintain a consistent standard across the catalogue and gives readers confidence in the books being offered.

The application is built using Django. It includes authentication, role-based author and staff functionality, user-owned account information, catalogue management and Stripe payment processing.

## Live Site

- Live site: **To be added following deployment**
- Repository: [The Nook GitHub Repository](https://github.com/gibba42/project_5_the_nook)

- ## Technologies Used

- **HTML5** – used to structure the application’s pages and content.
- **CSS3** – used for the custom styling, responsive layouts and watercolour-inspired visual design.
- **JavaScript** – used to provide interactive behaviour, including the checkout process.
- **Python** – used for the application’s back-end logic.
- **Django 5.2.16** – used as the main web application framework.
- **SQLite** – used as the relational database during local development.
- **Bootstrap 5** – used to support responsive layouts and reusable interface components.
- **jQuery** – used for interface behaviour and displaying Django toast messages.
- **Django Allauth** – used for account registration, login, logout and authentication.
- **Django Crispy Forms** and **Crispy Bootstrap 5** – used to render and style application forms.
- **Stripe** – used to process payments securely.
- **Django Countries** – used to provide country choices within checkout and delivery forms.
- **Pillow** – used to support image uploads and processing for book covers and author profiles.
- **Font Awesome** – used to provide icons throughout the application.
- **Google Fonts** – used to provide the Libre Baskerville and DM Sans typefaces.
- **Git** – used for version control.
- **GitHub** – used to store the repository and manage the project through epics, user stories and tasks.
- **Figma** – used to plan the application’s page layouts and responsive design.
- **Visual Studio Code** – used as the main development environment.
- **ChatGPT** – used to support debugging, particularly updating the project to the latest versions of Django and Bootstrap. All generated suggestions were reviewed, adapted and tested before being included in the project.
- **Heroku** - used to host the live deployment of the project.

- ## Project Purpose

Independent authors can struggle to gain visibility through traditional booksellers, while readers may find it difficult to discover new books outside established publishing channels. The Nook is designed to bring these two groups together through an accessible online bookshop.

The application allows readers to discover independent books, learn more about their authors, make secure purchases and share their opinions through reviews. Authors can create a public profile and submit book listings, giving them a dedicated space to present their work to potential readers.

Unlike an unrestricted marketplace, every submitted book must be approved by a staff member before it appears in the public catalogue. This controlled approach allows The Nook to maintain the quality and consistency of its listings while providing readers with a more trustworthy shopping experience.

The project therefore has three main goals:

- Help readers discover and purchase books from independent authors.
- Give independent authors a structured way to showcase their work.
- Provide the site owner with a manageable e-commerce model through which listings, customers and purchases can be administered.

- ## Target Audience

The Nook is designed for three main user groups:

### Readers

The primary audience is readers who want to discover and purchase books from independent authors. These users need a straightforward way to browse the catalogue, search for books, view detailed book and author information, complete secure purchases, and leave reviews.

### Independent Authors

The application is also aimed at independent authors who want to increase the visibility of their work. Registered authors can create a public author profile, submit books for approval, and manage their submitted listings through an author dashboard.

### Site Administrators

Staff members are responsible for managing the shop and maintaining the quality of its catalogue. They can review submitted books, approve or reject listings, and manage the application’s users, products and orders through the Django administration interface.

## Bugs

| Title | Description | Fix | Status |
|-------|-------------|-----|--------|
| Book model tests failing | The test for when a reviewer is deleted books they reviewed should remain failed. | This was due to outstanding migrations in the book model. Applying the migrations resolved the issue. Tests were re-run and all passed. | Resolved |
| Account templates not loading | A number of the account template pages were failing to load. | The issue was caused by crispy forms not being loaded in the templates. Added {% load crispy_forms_tags %} to the affected pages. | Resolved |
| Genre link not working in the nav bar | The genre link in the nav bar just took users to the book list. | Updated the genre link to show filters. | Resolved |
| Home/tests.py not running all tests | Home/tests.py was only running 17 out of 18 tests. | The issue was caused by incorrect indention. Outdented the impacted test. | Resolved |
