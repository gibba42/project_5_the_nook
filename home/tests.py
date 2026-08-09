from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class NavigationTests(TestCase):
    """Tests for the shared site navigation in user story 1.1."""

    def setUp(self):
        """Create a user for the authenticated navigation tests."""

        self.user = get_user_model().objects.create_user(
            username='navigation_user',
            email='navigation@example.com',
            password='test-password-123',
        )

    def test_shared_navigation_and_footer_render_across_pages(self):
        """The navbar and footer should be inherited from base.html."""

        for url_name in ('home', 'book_list', 'view_bag'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(
                    response,
                    'includes/main-nav.html',
                )
                self.assertTemplateUsed(
                    response,
                    'includes/footer.html',
                )

    def test_anonymous_navigation_contains_required_links(self):
        """Visitors should see every public navigation destination."""

        response = self.client.get(reverse('home'))

        expected_links = (
            reverse('home'),
            reverse('book_list'),
            f"{reverse('book_list')}?show_filters=1#catalogue-filters",
            f"{reverse('home')}#newsletter",
            reverse('account_login'),
            reverse('account_signup'),
            reverse('view_bag'),
        )

        for link in expected_links:
            with self.subTest(link=link):
                self.assertContains(
                    response,
                    f'href="{link}"',
                )

        self.assertNotContains(
            response,
            f'href="{reverse("profile")}"',
        )

    def test_authenticated_navigation_contains_account_links(self):
        """Signed-in users should see their account navigation."""

        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))

        for url_name in (
            'profile',
            'author_dashboard',
            'account_logout',
        ):
            with self.subTest(url_name=url_name):
                self.assertContains(
                    response,
                    f'href="{reverse(url_name)}"',
                )

        self.assertNotContains(
            response,
            f'href="{reverse("account_login")}"',
        )

        self.assertNotContains(
            response,
            f'href="{reverse("account_signup")}"',
        )

    def test_public_navigation_destinations_do_not_break(self):
        """Every public page linked from the navigation should load."""

        for url_name in (
            'home',
            'book_list',
            'view_bag',
            'account_login',
            'account_signup',
        ):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)

        books_response = self.client.get(reverse('book_list'))
        home_response = self.client.get(reverse('home'))

        self.assertContains(
            books_response,
            'id="catalogue-filters"',
        )

        self.assertContains(
            home_response,
            'id="newsletter"',
        )

    def test_authenticated_navigation_destinations_do_not_break(self):
        """Every signed-in account destination should load."""

        self.client.force_login(self.user)

        for url_name in (
            'profile',
            'author_dashboard',
            'account_logout',
        ):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)

    def test_current_page_is_identified_in_main_navigation(self):
        """Home and catalogue pages should expose an active link."""

        for url_name in ('home', 'book_list'):
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))

                self.assertContains(
                    response,
                    'aria-current="page"',
                    count=1,
                )

    def test_genres_navigation_opens_filter_panel(self):
        """The Genres link should reveal the collapsible genre controls."""

        response = self.client.get(
            reverse('book_list'),
            {'show_filters': '1'},
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'collapse show',
        )

        self.assertContains(
            response,
            'aria-expanded="true"',
        )

        self.assertContains(
            response,
            'aria-current="page"',
            count=1,
        )