from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from authors.models import AuthorProfile
from books.models import Book, Genre


class Command(BaseCommand):
    """
    Seed The Nook with example authors, genres and books.

    The command is safe to run multiple times because authors and genres
    are matched by name and books are matched using their unique ISBN.
    """

    help = "Create example authors, genres and books for development."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating example data for The Nook...")

        genres = self.create_genres()
        authors = self.create_authors()
        self.create_books(authors, genres)

        self.stdout.write(
            self.style.SUCCESS(
                "Example book data created successfully."
            )
        )

    def create_genres(self):
        """Create the example book genres."""

        genre_data = {
            "Fantasy": (
                "Imaginative fiction featuring magical worlds, "
                "mythic creatures and extraordinary adventures."
            ),
            "Science Fiction": (
                "Stories exploring technology, space, society and "
                "possible futures."
            ),
            "Mystery": (
                "Stories centred on secrets, investigations and "
                "unanswered questions."
            ),
            "Romance": (
                "Character-driven stories focused on love, "
                "relationships and emotional connection."
            ),
            "Historical Fiction": (
                "Fictional stories inspired by real historical "
                "periods, places and events."
            ),
            "Horror": (
                "Dark fiction designed to unsettle, frighten or "
                "explore the unknown."
            ),
            "Contemporary Fiction": (
                "Modern character-focused stories grounded in "
                "recognisable everyday life."
            ),
            "Adventure": (
                "Fast-moving stories involving exploration, danger "
                "and discovery."
            ),
        }

        genres = {}

        for name, description in genre_data.items():
            genre, created = Genre.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                },
            )

            genres[name] = genre

            if created:
                self.stdout.write(f"  Created genre: {name}")

        return genres

    def create_authors(self):
        """Create fictional independent authors."""

        author_data = [
            {
                "display_name": "Mara Vale",
                "bio": (
                    "Mara Vale writes atmospheric fantasy about forgotten "
                    "places, difficult choices and the people who refuse to "
                    "leave them behind. She lives near the Northumberland "
                    "coast with an unreasonable number of houseplants."
                ),
                "website": "https://example.com/mara-vale",
                "is_approved": True,
            },
            {
                "display_name": "Elias North",
                "bio": (
                    "Elias North is an independent mystery writer fascinated "
                    "by isolated communities, old technology and secrets that "
                    "refuse to stay buried."
                ),
                "website": "https://example.com/elias-north",
                "is_approved": True,
            },
            {
                "display_name": "Clara Finch",
                "bio": (
                    "Clara Finch writes warm contemporary romance about "
                    "ordinary people navigating complicated lives. Her "
                    "stories usually contain coffee, rain and at least one "
                    "questionable life decision."
                ),
                "website": "https://example.com/clara-finch",
                "is_approved": True,
            },
            {
                "display_name": "Jonas Wren",
                "bio": (
                    "Jonas Wren writes speculative fiction about exploration, "
                    "memory and humanity's relationship with technology."
                ),
                "website": "https://example.com/jonas-wren",
                "is_approved": True,
            },
            {
                "display_name": "Beatrice Holloway",
                "bio": (
                    "Beatrice Holloway writes historical fiction inspired by "
                    "overlooked lives and small moments hidden inside major "
                    "events."
                ),
                "website": "https://example.com/beatrice-holloway",
                "is_approved": True,
            },
            {
                "display_name": "Rowan Black",
                "bio": (
                    "Rowan Black writes folk horror rooted in rural legends, "
                    "old customs and landscapes that remember more than the "
                    "people living on them."
                ),
                "website": "https://example.com/rowan-black",
                "is_approved": True,
            },
            {
                "display_name": "Amelia Hart",
                "bio": (
                    "Amelia Hart writes contemporary fiction about families, "
                    "friendships and the quiet decisions that change people's "
                    "lives."
                ),
                "website": "https://example.com/amelia-hart",
                "is_approved": True,
            },
            {
                "display_name": "Theo Mercer",
                "bio": (
                    "Theo Mercer writes adventure fiction full of lost maps, "
                    "remote places and characters who should probably have "
                    "stayed at home."
                ),
                "website": "https://example.com/theo-mercer",
                "is_approved": True,
            },
        ]

        authors = {}

        for data in author_data:
            author, created = AuthorProfile.objects.update_or_create(
                display_name=data["display_name"],
                defaults={
                    "bio": data["bio"],
                    "website": data["website"],
                    "is_approved": data["is_approved"],
                },
            )

            authors[data["display_name"]] = author

            if created:
                self.stdout.write(
                    f'  Created author: {data["display_name"]}'
                )

        return authors

    def create_books(self, authors, genres):
        """Create example books across several states and genres."""

        books = [
            {
                "title": "The Glass Orchard",
                "author": "Mara Vale",
                "genre": "Fantasy",
                "isbn": "9780000000001",
                "description": (
                    "Every autumn the trees of Bellweather Orchard bear "
                    "transparent fruit that cannot be eaten and cannot be "
                    "broken. When the harvest begins appearing months early, "
                    "botanist Elian Moss returns to the village she abandoned "
                    "and discovers something beneath the roots has started "
                    "to wake."
                ),
                "price": Decimal("12.99"),
                "publication_date": date(2025, 9, 18),
                "stock_quantity": 18,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Where the Stone Remembers",
                "author": "Mara Vale",
                "genre": "Fantasy",
                "isbn": "9780000000002",
                "description": (
                    "In the mountain city of Caldris, memories can be carved "
                    "into stone. Apprentice mason Nera discovers a monument "
                    "containing a memory that the city's rulers insist never "
                    "happened."
                ),
                "price": Decimal("14.50"),
                "publication_date": date(2026, 2, 12),
                "stock_quantity": 11,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "A Lantern for Winter",
                "author": "Mara Vale",
                "genre": "Fantasy",
                "isbn": "9780000000003",
                "description": (
                    "A travelling lamplighter reaches a town where nobody "
                    "allows their lanterns to go dark, even in daylight. "
                    "When his own flame begins whispering his name, he learns "
                    "why the townspeople fear the coming winter."
                ),
                "price": Decimal("10.99"),
                "publication_date": date(2024, 11, 7),
                "stock_quantity": 4,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Saltwater Signals",
                "author": "Elias North",
                "genre": "Mystery",
                "isbn": "9780000000004",
                "description": (
                    "Radio operator Daniel Harker spends his nights listening "
                    "to empty frequencies from a lighthouse off the Cornish "
                    "coast. Then a ship that vanished thirty years ago starts "
                    "transmitting."
                ),
                "price": Decimal("9.99"),
                "publication_date": date(2025, 4, 3),
                "stock_quantity": 23,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Last Room Upstairs",
                "author": "Elias North",
                "genre": "Mystery",
                "isbn": "9780000000005",
                "description": (
                    "The residents of a converted London townhouse agree on "
                    "one thing: the building has five floors. So why does the "
                    "lift sometimes offer a sixth?"
                ),
                "price": Decimal("11.50"),
                "publication_date": date(2026, 1, 22),
                "stock_quantity": 15,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Crowbridge Letters",
                "author": "Elias North",
                "genre": "Mystery",
                "isbn": "9780000000006",
                "description": (
                    "A bookseller receives six letters addressed to customers "
                    "who have not visited his shop yet. Each contains a "
                    "warning. Five come true."
                ),
                "price": Decimal("8.99"),
                "publication_date": date(2023, 10, 14),
                "stock_quantity": 0,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Second Cup",
                "author": "Clara Finch",
                "genre": "Romance",
                "isbn": "9780000000007",
                "description": (
                    "After inheriting half of a struggling café, Sophie Lane "
                    "discovers the other half belongs to the man she spent "
                    "three years trying to forget."
                ),
                "price": Decimal("8.50"),
                "publication_date": date(2025, 2, 14),
                "stock_quantity": 30,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Meet Me After Closing",
                "author": "Clara Finch",
                "genre": "Romance",
                "isbn": "9780000000008",
                "description": (
                    "Two neighbouring shop owners have spent years competing "
                    "for the same customers. A broken water pipe forces them "
                    "to share one premises for six weeks."
                ),
                "price": Decimal("9.50"),
                "publication_date": date(2024, 6, 20),
                "stock_quantity": 12,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Letters from Platform Nine",
                "author": "Clara Finch",
                "genre": "Romance",
                "isbn": "9780000000009",
                "description": (
                    "Every Friday morning, Anna finds a handwritten note "
                    "tucked beneath the same railway-station bench. She has "
                    "no idea who writes them, but she begins replying."
                ),
                "price": Decimal("10.00"),
                "publication_date": date(2026, 5, 1),
                "stock_quantity": 19,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Antenna",
                "author": "Jonas Wren",
                "genre": "Science Fiction",
                "isbn": "9780000000010",
                "description": (
                    "Humanity's first permanent station beyond Mars detects "
                    "a repeating signal from empty space. Engineer Cora Venn "
                    "is the first person to realise the signal is responding "
                    "to them."
                ),
                "price": Decimal("13.99"),
                "publication_date": date(2025, 8, 9),
                "stock_quantity": 17,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Quiet Between Worlds",
                "author": "Jonas Wren",
                "genre": "Science Fiction",
                "isbn": "9780000000011",
                "description": (
                    "A survey crew sent through humanity's newest gateway "
                    "finds a perfect copy of Earth on the other side, except "
                    "every city is empty."
                ),
                "price": Decimal("15.00"),
                "publication_date": date(2026, 3, 17),
                "stock_quantity": 8,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Three Minutes of Sunlight",
                "author": "Jonas Wren",
                "genre": "Science Fiction",
                "isbn": "9780000000012",
                "description": (
                    "On a planet locked beneath permanent cloud, sunlight "
                    "reaches the surface for only three minutes each year. "
                    "This year, something descends with it."
                ),
                "price": Decimal("11.99"),
                "publication_date": date(2024, 8, 28),
                "stock_quantity": 7,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Seamstress of Blackfriars",
                "author": "Beatrice Holloway",
                "genre": "Historical Fiction",
                "isbn": "9780000000013",
                "description": (
                    "London, 1912. A seamstress working behind the grand "
                    "windows of a fashionable department store becomes the "
                    "unlikely keeper of a secret shared by women from every "
                    "level of society."
                ),
                "price": Decimal("12.50"),
                "publication_date": date(2025, 3, 6),
                "stock_quantity": 16,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "When the Sirens Stopped",
                "author": "Beatrice Holloway",
                "genre": "Historical Fiction",
                "isbn": "9780000000014",
                "description": (
                    "In the summer of 1945, three families return to the same "
                    "London street and discover that surviving the war was "
                    "only the beginning."
                ),
                "price": Decimal("10.99"),
                "publication_date": date(2024, 9, 2),
                "stock_quantity": 10,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Cartographer's Daughter",
                "author": "Beatrice Holloway",
                "genre": "Historical Fiction",
                "isbn": "9780000000015",
                "description": (
                    "When her father disappears in 1891, Eleanor Ash discovers "
                    "his final map contains streets that do not appear on any "
                    "official plan of London."
                ),
                "price": Decimal("13.25"),
                "publication_date": date(2026, 6, 11),
                "stock_quantity": 14,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Under the Hawthorn",
                "author": "Rowan Black",
                "genre": "Horror",
                "isbn": "9780000000016",
                "description": (
                    "Nobody in Harrow Fell cuts the hawthorn trees. When a "
                    "developer clears an old field for new houses, the village "
                    "learns the tradition was never superstition."
                ),
                "price": Decimal("10.50"),
                "publication_date": date(2025, 10, 1),
                "stock_quantity": 9,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Bells Beneath the Lake",
                "author": "Rowan Black",
                "genre": "Horror",
                "isbn": "9780000000017",
                "description": (
                    "During a summer drought, the ruins of a drowned village "
                    "emerge from a reservoir. On the first night, its church "
                    "bell begins ringing beneath the water."
                ),
                "price": Decimal("11.75"),
                "publication_date": date(2024, 10, 20),
                "stock_quantity": 13,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "A House Full of Feathers",
                "author": "Rowan Black",
                "genre": "Horror",
                "isbn": "9780000000018",
                "description": (
                    "Following her grandmother's death, Mae inherits a cottage "
                    "with one unusual instruction: every feather found inside "
                    "the house must be burned before sunset."
                ),
                "price": Decimal("9.75"),
                "publication_date": date(2026, 7, 3),
                "stock_quantity": 6,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "All the Small Departures",
                "author": "Amelia Hart",
                "genre": "Contemporary Fiction",
                "isbn": "9780000000019",
                "description": (
                    "Four siblings return home to clear their childhood house "
                    "after their mother moves away, each carrying a different "
                    "version of why the family fell apart."
                ),
                "price": Decimal("9.99"),
                "publication_date": date(2025, 5, 15),
                "stock_quantity": 20,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Borrowed Sundays",
                "author": "Amelia Hart",
                "genre": "Contemporary Fiction",
                "isbn": "9780000000020",
                "description": (
                    "Every Sunday, two strangers sit at opposite ends of the "
                    "same park bench. Over the course of a year, the distance "
                    "between them slowly disappears."
                ),
                "price": Decimal("8.99"),
                "publication_date": date(2024, 4, 7),
                "stock_quantity": 22,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "The Mapmaker's Compass",
                "author": "Theo Mercer",
                "genre": "Adventure",
                "isbn": "9780000000021",
                "description": (
                    "A damaged compass, an unfinished map and a message from "
                    "a missing explorer send Ada Mercer into a mountain range "
                    "that appears differently on every chart."
                ),
                "price": Decimal("12.00"),
                "publication_date": date(2025, 7, 12),
                "stock_quantity": 18,
                "is_featured": True,
                "status": Book.Status.APPROVED,
            },
            {
                "title": "Beyond the Red Horizon",
                "author": "Theo Mercer",
                "genre": "Adventure",
                "isbn": "9780000000022",
                "description": (
                    "When a desert expedition uncovers the remains of a road "
                    "running directly into an unmapped canyon, explorer Sam "
                    "Vale makes the mistake of following it."
                ),
                "price": Decimal("13.50"),
                "publication_date": date(2026, 4, 9),
                "stock_quantity": 12,
                "is_featured": False,
                "status": Book.Status.APPROVED,
            },

            # Non-public books below are useful for testing workflow states.
            {
                "title": "The Lighthouse at World's End",
                "author": "Elias North",
                "genre": "Mystery",
                "isbn": "9780000000023",
                "description": (
                    "A newly appointed lighthouse keeper discovers that his "
                    "predecessor recorded a ship arriving every thirteen years "
                    "despite there being no harbour."
                ),
                "price": Decimal("10.99"),
                "publication_date": date(2026, 9, 24),
                "stock_quantity": 10,
                "is_featured": False,
                "status": Book.Status.PENDING,
            },
            {
                "title": "The Garden After Midnight",
                "author": "Mara Vale",
                "genre": "Fantasy",
                "isbn": "9780000000024",
                "description": (
                    "A forgotten garden appears behind a different house each "
                    "night, offering visitors one chance to recover something "
                    "they have lost."
                ),
                "price": Decimal("12.25"),
                "publication_date": None,
                "stock_quantity": 0,
                "is_featured": False,
                "status": Book.Status.DRAFT,
            },
            {
                "title": "Greywater",
                "author": "Rowan Black",
                "genre": "Horror",
                "isbn": "9780000000025",
                "description": (
                    "After weeks of rain, dark water begins rising through the "
                    "floorboards of homes in an isolated village."
                ),
                "price": Decimal("10.25"),
                "publication_date": date(2026, 8, 1),
                "stock_quantity": 5,
                "is_featured": False,
                "status": Book.Status.REJECTED,
                "rejection_reason": (
                    "Example rejected listing for development testing."
                ),
            },
        ]

        created_count = 0
        updated_count = 0

        for data in books:
            author = authors[data["author"]]
            genre = genres[data["genre"]]

            defaults = {
                "author": author,
                "genre": genre,
                "title": data["title"],
                "description": data["description"],
                "price": data["price"],
                "publication_date": data["publication_date"],
                "stock_quantity": data["stock_quantity"],
                "is_featured": data["is_featured"],
                "is_active": True,
                "status": data["status"],
                "rejection_reason": data.get(
                    "rejection_reason",
                    "",
                ),
            }

            book, created = Book.objects.update_or_create(
                isbn=data["isbn"],
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    f'  Created book: {book.title}'
                )
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Books: {created_count} created, "
                f"{updated_count} updated."
            )
        )