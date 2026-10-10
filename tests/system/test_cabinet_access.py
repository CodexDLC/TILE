from unittest.mock import patch

from cabinet.views.analytics import AnalyticsReportsView, analytics_dashboard_view
from cabinet.views.users import UserListView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse


class CabinetStaffAccessTests(TestCase):
    routes = (
        "cabinet:users_list",
        "cabinet:analytics_reports",
        "cabinet:analytics_dashboard",
    )

    def setUp(self):
        self.member = get_user_model().objects.create_user(username="member")
        self.editor = get_user_model().objects.create_user(username="editor", is_staff=True)
        self.owner = get_user_model().objects.create_user(username="owner", is_superuser=True)

    def test_anonymous_cannot_reach_staff_pages(self):
        for route in self.routes:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertIn(response.status_code, (302, 403))

    def test_member_cannot_read_staff_pages_or_invoke_providers(self):
        self.client.force_login(self.member)
        with (
            patch("cabinet.views.users.UserService.get_list_context", return_value={}) as users,
            patch("cabinet.views.analytics.AnalyticsService.get_reports_context", return_value={}) as reports,
            patch("cabinet.views.analytics.dashboard_view", return_value=HttpResponse()) as dashboard,
        ):
            for route in self.routes:
                with self.subTest(route=route):
                    self.assertEqual(self.client.get(reverse(route)).status_code, 403)
            users.assert_not_called()
            reports.assert_not_called()
            dashboard.assert_not_called()

    def test_active_editor_and_superuser_keep_access(self):
        for user in (self.editor, self.owner):
            self.client.force_login(user)
            for route in self.routes:
                with self.subTest(user=user.username, route=route):
                    response = self.client.get(reverse(route))
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.wsgi_request.cabinet_space, "staff")
                    expected_module = "users" if route.endswith("users_list") else "analytics"
                    self.assertEqual(response.wsgi_request.cabinet_module, expected_module)

    def test_inactive_staff_and_superuser_are_denied_before_provider(self):
        factory = RequestFactory()
        for user in (self.editor, self.owner):
            user.is_active = False
            for view in (UserListView.as_view(), AnalyticsReportsView.as_view(), analytics_dashboard_view):
                request = factory.get("/cabinet/")
                request.user = user
                with self.subTest(user=user.username, view=view), self.assertRaises(PermissionDenied):
                    view(request)

    def test_class_views_deny_anonymous_before_provider(self):
        request = RequestFactory().get("/cabinet/")
        request.user = AnonymousUser()
        for view in (UserListView.as_view(), AnalyticsReportsView.as_view()):
            with self.subTest(view=view), self.assertRaises(PermissionDenied):
                view(request)
