import datetime
from unittest import TestCase

from mock import Mock, patch, MagicMock
from metrique.issue_analyzer import IssueAnalyzer


class MockIssues(object):
    @staticmethod
    def create_issue(state):
        mock = Mock()
        mock.state = state
        if state == "closed":
            mock.created_at = datetime.datetime.utcnow() - datetime.timedelta(days=7)
            mock.closed_at = mock.created_at + datetime.timedelta(days=2)
        return mock

    @classmethod
    def get_mock_issues(cls, length, state):
        return map(lambda x: cls.create_issue(state), range(length))


def get_mock_issues(*args, **kwargs):
    mock_issue1 = Mock()
    mock_issue1.state = "open"

    mock_issue2 = Mock()
    mock_issue2.state = "closed"
    mock_issue2.closed_at = datetime.datetime.utcnow()
    mock_issue2.created_at = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    mock_issue3 = Mock()
    mock_issue3.state = "open"

    mock_issue4 = Mock()
    mock_issue4.state = "closed"
    mock_issue4.closed_at = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    mock_issue4.created_at = datetime.datetime.utcnow() - datetime.timedelta(days=4)

    return [mock_issue1, mock_issue2, mock_issue3, mock_issue4]


class TestAnalyzer(TestCase):
    def setUp(self):
        self.org_name = "TestOrg"
        self.repo_name = "TestRepo"

    def test_is_issue_closed_positive(self):
        mock_issue = Mock()
        mock_issue.state = "closed"
        self.assertEqual(IssueAnalyzer.is_issue_closed(mock_issue), True)

    def test_is_issue_closed_negative(self):
        mock_issue = Mock()
        mock_issue.state = "my_state"
        self.assertEqual(IssueAnalyzer.is_issue_closed(mock_issue), False)

    def test_is_issue_open_positive(self):
        mock_issue = Mock()
        mock_issue.state = "open"
        self.assertEqual(IssueAnalyzer.is_issue_open(mock_issue), True)

    def test_is_issue_open_negative(self):
        mock_issue = Mock()
        mock_issue.state = "my_state"
        self.assertEqual(IssueAnalyzer.is_issue_open(mock_issue), False)

    # Mocking 1
    def test_update_issue_counters(self):
        mock_issue = Mock()
        mock_issue.state = "open"
        mock_metrics = Mock()
        mock_metrics.closed_issues = 1
        mock_metrics.open_issues = 1
        mock_metrics.total_issues = 10
        mock_metrics.tt = 2

        IssueAnalyzer(self.org_name, self.repo_name).update_issue_counters(mock_issue, mock_metrics)
        self.assertEqual(mock_metrics.open_issues, 2)
        self.assertEqual(mock_metrics.total_issues, 11)

        mock_issue.state = "closed"
        IssueAnalyzer(self.org_name, self.repo_name).update_issue_counters(mock_issue, mock_metrics)
        self.assertEqual(mock_metrics.closed_issues, 2)
        self.assertEqual(mock_metrics.total_issues, 12)

    @patch("github.Github.get_repo")
    def test_publish_metrics(self, repo):
        # Return mock_repo
        mock_repo = Mock()
        repo.return_value = mock_repo

        mock_repo.get_issues = get_mock_issues

        # Call function under test
        issue_metrics = IssueAnalyzer(self.org_name, self.repo_name).publish_metrics()

        # Add asserts to validate
        self.assertEqual(issue_metrics.open_issues, 2)
        self.assertEqual(issue_metrics.closed_issues, 2)
        self.assertEqual(issue_metrics.total_issues, 4)

    @patch("metrique.issue_analyzer.IssueAnalyzer.process_issue")
    @patch("github.Github.get_repo")
    def test_publish_metrics_exception(self, repo, mock_processor):
        # Return mock_repo
        mock_repo = Mock()
        repo.return_value = mock_repo

        mock_repo.get_issues = get_mock_issues

        mock_processor.side_effect = [
            mock_processor.real_method(),
            mock_processor.real_method(),
            mock_processor.real_method(),
            Exception("Failed to process issue")
        ]

        # Call function under test
        issue_metrics = IssueAnalyzer(self.org_name, self.repo_name).publish_metrics()

        # Add asserts to validate
        self.assertEqual(issue_metrics.open_issues, 2)
        self.assertEqual(issue_metrics.closed_issues, 1)
        self.assertEqual(issue_metrics.total_issues, 3)


    @patch("github.Github.get_repo")
    def test_publish_metrics_exception(self, repo):
        # Return mock_repo
        mock_repo = Mock()
        repo.return_value = mock_repo

        mock_issues = Mock()
        mock_issues.side_effect = Exception("GITHUB API Unavailable")
        mock_repo.get_issues = mock_issues

        # Call function under test
        issue_metrics = IssueAnalyzer(self.org_name, self.repo_name).publish_metrics()

        # Add asserts to validate
        self.assertEqual(issue_metrics.open_issues, 2)
        self.assertEqual(issue_metrics.closed_issues, 2)
        self.assertEqual(issue_metrics.total_issues, 4)