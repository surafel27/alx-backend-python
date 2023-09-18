#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from unittest.mock import PropertyMock, patch

import client
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @parameterized.expand([("google"), ("abc")])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org, mock_org):
        """Tests the `org` method."""
        org_test = GithubOrgClient(org)
        test_response = org_test.org
        self.assertEqual(test_response, mock_org.return_value)
        mock_org.assert_called_once()

    def test_public_repos_url(self):
        """Tests the `_public_repos_url` property."""
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as m:
            m.return_value = {"repos_url": "89"}
            test_org = GithubOrgClient("holberton")
            test_repo_url = test_org._public_repos_url
            self.assertEqual(test_repo_url, m.return_value.get("repos_url"))
            m.assert_called_once()

    @patch(
        "client.get_json",
        return_value=[{"name": "Holberton"}, {"name": "89"}, {"name": "alx"}],
    )
    def test_public_repos(self, mock_repo):
        """Tests the `public_repos` method."""
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/",
        ) as m:
            test_client = GithubOrgClient("holberton")
            test_repo = test_client.public_repos()
            for idx in range(3):
                self.assertIn(mock_repo.return_value[idx]["name"], test_repo)
            mock_repo.assert_called_once()
            m.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Tests the `has_license` method."""
        test_instance = GithubOrgClient("holberton")
        license_available = test_instance.has_license(repo, license_key)
        self.assertEqual(license_available, expected)


def requests_get(*args, **kwargs):
    """
    Function that mocks requests.get function
    Returns the correct json data based on the given input url
    """

    class MockResponse:
        """
        Mock response
        """

        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == "https://api.github.com/orgs/google":
        return MockResponse(TEST_PAYLOAD[0][0])
    if args[0] == TEST_PAYLOAD[0][0]["repos_url"]:
        return MockResponse(TEST_PAYLOAD[0][1])


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(TEST_PAYLOAD[0][0], TEST_PAYLOAD[0][1],
      TEST_PAYLOAD[0][2], TEST_PAYLOAD[0][3])],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""

    @classmethod
    def setUpClass(cls):
        """Sets up class fixtures before running tests."""
        cls.get_patcher = patch("utils.requests.get", side_effect=requests_get)
        cls.get_patcher.start()
        cls.client = GithubOrgClient("google")

    def test_public_repos(self):
        """Tests the `public_repos` method."""
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"), self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls):
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()
