from unittest import TestCase

from nose_parameterized import parameterized

from metrique.issue_metrics import IssueMetrics


class TestMetrics(TestCase):

    # Case 1
    def test_equals_positive(self):
        im1 = IssueMetrics()
        im1.closed_issues = 3
        im1.open_issues = 5

        im2 = IssueMetrics()
        im2.closed_issues = 3
        im2.open_issues = 5

        self.assertEqual(im1 == im2, True)

    def test_equals_negative(self):
        im1 = IssueMetrics()
        im1.closed_issues = 3
        im1.open_issues = 5

        im2 = IssueMetrics()
        im2.closed_issues = 3
        im2.open_issues = 8

        self.assertEqual(im1 == im2, False)

    # Case 3
    @parameterized.expand([
        ("positive", 3, 5, 3, 5, True),
        ("negative", 3, 5, 3, 8, False),
        ("negative_none", None, None, None, None, True),
    ])
    def test_equals(self, name, im1_ci, im1_oi, im2_ci, im2_oi, result):
        im1 = IssueMetrics()
        im1.closed_issues = im1_ci
        im1.open_issues = im1_oi

        im2 = IssueMetrics()
        im2.closed_issues = im2_ci
        im2.open_issues = im2_oi

        self.assertEqual(im1 == im2, result)







