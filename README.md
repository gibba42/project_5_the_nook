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
- **ChatGPT** – used to support debugging, particularly updating the project to the latest versions of Django and Bootstrap. It was also used to generate fake book listing data. All generated suggestions were reviewed, adapted and tested before being included in the project.
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

## E-commerce Business Model

The Nook operates as a curated, direct-to-consumer online bookshop specialising in books from independent authors. It uses a single-vendor retail model: customers purchase books from The Nook rather than directly from individual authors.

### Value Proposition

For readers, The Nook provides a focused alternative to larger online retailers. Customers can discover independent books through a catalogue in which each listing has been reviewed before publication. Detailed book pages, author profiles and customer reviews help readers make informed purchasing decisions.

For independent authors, the platform provides an additional way to promote their work. Authors can create a public profile and submit books for consideration without needing to build and manage their own e-commerce website.

### Revenue Model

The business generates revenue through individual book sales. The site owner controls the catalogue and selling prices, while customers pay securely through Stripe during checkout.

The difference between the selling price and the costs associated with sourcing, processing and fulfilling each order would provide the business with its operating margin.

### Operating Model

The submitted application uses a controlled catalogue rather than allowing authors to sell directly to customers. The process is:

1. A registered author creates an author profile.
2. The author submits a book listing for review.
3. A staff member reviews and approves or rejects the submission.
4. Approved books become available in the public catalogue.
5. A reader adds books to their basket and completes payment through Stripe.
6. The Nook records and manages the resulting order.

This approach gives the site owner control over product quality, pricing and the customer experience. It also avoids the additional payment, commission and seller-management requirements of a multi-vendor marketplace.

## UX Design

The user experience for The Nook was designed around three connected journeys:

- Readers discovering and purchasing independent books.
- Authors creating profiles and submitting books.
- Staff reviewing submissions before they enter the public catalogue.

The design aims to make The Nook feel calm, trustworthy and easy to navigate while still giving it a recognisable independent-bookshop identity.

### UX Strategy

The main UX goals were to:

- Make the purpose of the application immediately clear to new visitors.
- Allow readers to move from discovery to purchase with as little friction as possible.
- Present important purchasing information before asking users to add a book to their basket.
- Give authors a clear view of their submitted books and their approval status.
- Separate reader, author and staff functionality without making the main navigation overly complicated.
- Provide clear feedback after important actions such as updating a basket, submitting a listing or completing an order.
- Maintain a consistent experience across desktop and mobile devices.
- Support keyboard navigation, screen readers and users who require clearly visible focus states.

### User Needs

| User | Need | Design Response |
|------|------|-----------------|
| Visitor | Understand what The Nook offers | The homepage opens with a clear description and a prominent Browse Books call to action. |
| Reader | Find books that interest them | The catalogue provides search, genre filters and sorting controls. |
| Reader | Make an informed purchase | Book pages prioritise the cover, author, description, rating, price and stock information. |
| Customer | Complete a purchase confidently | The basket and checkout designs retain a visible order summary and provide clear confirmation after payment. |
| Registered user | Review previous activity | The account area groups personal details, reviews and order history in one location. |
| Author | Present themselves professionally | Authors can create a public profile containing their name, biography and published books. |
| Author | Understand the status of submitted books | The author dashboard displays each listing and its current approval status. |
| Staff member | Review submissions efficiently | The approval queue groups pending books and provides clear approval or change-request actions. |

### Primary User Journeys

| Journey | Intended Route |
|---------|----------------|
| Discover and purchase a book | Home → Catalogue → Book Details → Basket → Checkout → Order Confirmation |
| Manage a reader account | Sign In → Account → Order History or Reviews |
| Submit a book | Register or Sign In → Author Profile → Author Dashboard → Add Listing → Submit for Approval |
| Review a submission | Staff Sign In → Approval Queue → Review Listing → Approve or Request Changes |

### Information Architecture

The main navigation was kept deliberately concise. It provides access to Home, Books, Genres, New Releases and the Newsletter, while search, account and basket actions remain visible in the header.

Account-specific actions are grouped within the account menu. The options shown change depending on whether the user is logged out, logged in, an author or a staff member. This reduces clutter and prevents users from being offered actions they cannot access.

On smaller screens, the navigation collapses into a mobile menu. Search and basket access remain available without requiring users to navigate through multiple pages.

### Wireframes and High-Fidelity Mock-ups

Responsive mock-ups were created in Figma for desktop screens at 1440 pixels and mobile screens at 390 pixels. These were used to plan information hierarchy, page structure, responsive behaviour and the visual relationship between the reader, author and staff journeys.

#### Homepage

The homepage was designed to explain the purpose of The Nook immediately. Its primary call to action directs readers to the catalogue, while supporting content introduces the independent-author focus of the shop.

#### Catalogue

The catalogue combines search, genre filtering and sorting without hiding the books beneath excessive controls. Filters remain visible in a desktop sidebar but collapse behind a button on smaller screens.

#### Book Details

The book detail page places the information needed for a purchasing decision near the top of the page. The cover, title, author, rating, price, description, stock status and basket action are grouped together. Reader reviews appear beneath the main product information as supporting social proof.

#### Checkout

The checkout was designed as a focused process with delivery and payment fields presented alongside a persistent order summary. On mobile devices, the sections stack into a single column while retaining the same information.

#### Author Dashboard

The author dashboard provides a summary of the author's listings and their current status. The add, edit and submission actions are kept close to the relevant book so that authors can manage their work without using the Django administration interface.

#### Staff Approval

The approval queue separates staff moderation from the public catalogue. Pending submissions are presented with their status and a clear review action. Approval and change-request actions are only available to authorised staff members.

### Visual Design

The visual design is intended to suggest a quiet independent bookshop without reducing readability or making the interface feel old-fashioned. The palette uses warm paper tones, muted sage green, dusty rose and gold accents.

Decorative elements are restrained so that book information, forms and calls to action remain the focus of each page.

#### Colour Palette

| Colour | Hex Value | Use |
|--------|-----------|-----|
| Cream | `#f7f3eb` | Main page background |
| Paper | `#fffdf8` | Headers, cards and content surfaces |
| Sage | `#7c8f76` | Secondary accents and hover states |
| Dark Sage | `#53664f` | Primary buttons, links and branding |
| Dusty Rose | `#c99186` | Decorative accents |
| Gold | `#c5a15b` | Ratings and keyboard focus indicators |
| Ink | `#2f332d` | Primary text |
| Muted Grey | `#6f746d` | Supporting text |
| Border | `#ddd6c9` | Dividers, fields and card borders |

### Typography

The Nook uses two typefaces:

- **Libre Baskerville** is used for the logo, headings and book-related titles. Its serif design supports the traditional bookshop identity.
- **DM Sans** is used for body text, navigation, buttons and forms. It remains clear at smaller sizes and provides contrast with the heading typeface.

Heading sizes use responsive CSS so that the information hierarchy remains clear without causing text to overflow on smaller screens.

### Responsive Design

The interface uses Bootstrap's responsive grid together with custom CSS media queries.

The principal responsive changes include:

- The desktop navigation changing to a collapsible mobile menu.
- Book grids reducing from three or four columns to two columns.
- Catalogue filters collapsing behind a mobile filter button.
- Book details changing from a side-by-side layout to a vertical layout.
- Basket summaries and checkout forms stacking into a single column.
- Author and staff dashboards replacing wide rows with vertically stacked cards.
- Buttons and form fields expanding where additional width improves touch accessibility.

- ## Agile Development

The Nook was planned and managed using an iterative Agile approach. GitHub Issues were used to divide the application into epics, user stories, acceptance criteria and individual development tasks.

This allowed the project to be developed in manageable sections while maintaining a clear connection between the application’s purpose, user needs and technical implementation.

### Epics

The project requirements were divided into eight epics:

| Epic | Scope |
|------|-------|
| [Epic 1 – Project Setup and Core Architecture](https://github.com/gibba42/project_5_the_nook/issues/1) | Django setup, reusable templates, navigation, database configuration and static files |
| [Epic 2 – Accounts, Authentication and Roles](https://github.com/gibba42/project_5_the_nook/issues/2) | Registration, authentication, user profiles and role-based permissions |
| [Epic 3 – Book Catalogue and Author Listings](https://github.com/gibba42/project_5_the_nook/issues/3) | Public catalogue, book details, author profiles and listing management |
| [Epic 4 – Admin Approval](https://github.com/gibba42/project_5_the_nook/issues/4) | Staff review, approval and rejection of submitted books |
| [Epic 5 – Basket, Checkout and Purchasing](https://github.com/gibba42/project_5_the_nook/issues/5) | Basket management, Stripe payments, purchase feedback and order history |
| [Epic 6 – Reviews](https://github.com/gibba42/project_5_the_nook/issues/6) | Creating, editing, deleting and displaying reader reviews |
| [Epic 7 – Newsletter, SEO and Marketing](https://github.com/gibba42/project_5_the_nook/issues/7) | Newsletter registration, search-engine optimisation and marketing evidence |
| [Epic 8 – Documentation, Testing and Deployment](https://github.com/gibba42/project_5_the_nook/issues/8) | README documentation, testing, validation, security and deployment |

### User Stories

Each epic was divided into user stories written from the perspective of a visitor, reader, author, staff member, site owner or developer.

The following format was used:

> As a **type of user**, I want to **perform an action** so that I can **receive a particular benefit**.

Each user story also contains:

- Acceptance criteria written using Given, When and Then statements.
- A priority based on the importance of the requirement.
- A checklist of the development tasks required to complete the story.
- A GitHub Issue status showing whether the story remains open or has been completed.

### Prioritisation

A MoSCoW-inspired method was used to prioritise the user stories:

| Priority | Meaning |
|----------|---------|
| Must Have | Required for the application to meet its core purpose |
| Should Have | Important functionality that improves the finished application but is not essential to its basic operation |
| Could Have | Additional functionality implemented after higher-priority requirements where time allows |

Must Have stories were given priority because they cover essential functionality such as navigation, authentication, catalogue access, author submissions, staff approval, payments, reviews, testing and deployment.

### Development Process

Development was completed incrementally. Each user story was broken into smaller tasks so that individual pieces of functionality could be implemented and tested before moving to the next requirement.

The general process was:

1. Select the next high-priority user story.
2. Review its acceptance criteria and task checklist.
3. Implement the required model, view, URL, template or supporting logic.
4. Test the functionality and permissions.
5. Resolve any bugs discovered during testing.
6. Update the task checklist and close the issue once its acceptance criteria had been met.

This process was also used when previously completed functionality required further work. For example, the navigation user story was revisited when the Genres link did not open the expected catalogue filters. The issue was only closed after the link behaviour and automated navigation tests had been corrected.

## Bugs

| Title | Description | Fix | Status |
|-------|-------------|-----|--------|
| Automated tests failing because migrations were incomplete | The test database did not match the current models, causing an automated model test to fail. | Generated and applied the outstanding migrations, then reran the test suite. | Resolved |
| Account pages not loading | Several registration and account pages failed because the custom Django Allauth templates were based on an older template structure and were stored in locations not expected by the installed version. | Replaced the outdated overrides with templates compatible with the installed Allauth version, moved them into the correct template directories and retested the account pages. | Resolved |
| Genre navigation link did not open the filters | The Genres navigation link loaded the catalogue but did not reveal the collapsed filter panel, particularly on mobile devices. | Added a `show_filters` query parameter, passed its state through the view and used it to open the filter panel and set the correct accessible navigation state. | Resolved |
| One navigation test was not discovered | Django reported 17 tests instead of the expected 18 because the genre navigation test had been placed outside the `NavigationTests` class. | Corrected the indentation so the method belonged to the test class. Django then discovered the additional test. | Resolved |
| Checkout template failed to load | The checkout page raised a template error because `crispy_forms_tags` was misspelled as `cripsy_forms_tags`. | Corrected the template tag library name. | Resolved |
| Stripe payment form did not initialise | `stripe_elements.js` was stored inside `checkout/static/checkout/css/js/`, while the checkout template expected it under `checkout/static/checkout/js/`. | Moved the JavaScript file to the correct static directory so Django could load it from the expected path. | Resolved |
| Users could access another customer's order history | The order-history view looked up orders using only the order number. A logged-in user could potentially enter another valid order number in the URL and view that order. | Protected the view with `login_required` and restricted the order lookup to orders belonging to the current user's profile. | Resolved |
| Basket quantities could not be updated or removed | Basket items were displayed, but the session did not update correctly when users changed quantities or removed products. | Added the adjust and remove views and URLs, connected the quantity forms and removal script, and updated the basket session after each action. | Resolved |
| Product sorting produced incorrect results | Catalogue sorting did not consistently handle product names, categories, direction or empty searches. | Added query handling with Django `Q` objects, case-insensitive name sorting, category mapping, direction handling and feedback for empty searches. | Resolved |
| Product image field did not work in add and edit forms | Images selected through the product-management forms were not rendered or processed correctly. | Added a custom clearable file-input widget, ensured uploaded files were passed through `request.FILES` and updated the add and edit templates. | Resolved |
| User profile table did not exist locally | Accessing the administration or profile pages raised `OperationalError: no such table: profiles_userprofile` after the profiles application was introduced. | Created the profiles migration and applied the outstanding migrations to the local database. | Resolved |
| Author dashboard link raised `NoReverseMatch` | The profile page attempted to reverse an `authors` namespace that had not been registered in the project URLs. | Updated the template links to use the registered `author_dashboard` URL name. | Resolved |
