from github import Github

from metrique.issue_metrics import IssueMetrics


class IssueAnalyzer(object):
    def __init__(self, org, repo):
        self.org = org
        self.repo = repo
        self.gh = Github()
        self.gh_repo = self.gh.get_repo("%s/%s" % (self.org, self.repo))

        # Temp Variables
        # self.total_issue_closure_time = 0
        # self.max_issue_closure_time = 0
        # self.max_issue_comments = 0

    @classmethod
    def is_issue_closed(cls, issue):
        return issue.state == 'closed'

    @classmethod
    def is_issue_open(cls, issue):
        return issue.state == 'open'

    def update_issue_counters(self, issue, issue_metrics):
        issue_metrics.total_issues += 1
        if self.is_issue_open(issue):
            issue_metrics.open_issues += 1
        elif self.is_issue_closed(issue):
            issue_metrics.closed_issues += 1

    def process_closure_time(self, issue, issue_metrics):
        if issue.state == 'closed':
            issue_closure_time = (issue.closed_at - issue.created_at).total_seconds()
            if issue_closure_time > issue_metrics.max_closure_time:
                issue_metrics.max_closure_time = issue_closure_time
                issue_metrics.longest_issue = issue
            # self.total_issue_closure_time += issue_closure_time

    # def process_comments(self, issue):
    #     self.issue_metrics.total_comments_on_issues += issue.comments
    #     if issue.comments > self.max_issue_comments:
    #         self.issue_metrics.issue_with_most_comments = issue

    def process_issue(self, issue, issue_metrics):
        self.update_issue_counters(issue, issue_metrics)
        self.process_closure_time(issue, issue_metrics)
        # self.process_comments(issue)

    # def calculate_metrics(self):
    #     self.issue_metrics.average_issue_closure_time = self.total_issue_closure_time/self.issue_metrics.closed_issues
    #     self.issue_metrics.average_comments_per_issue = self.issue_metrics.total_comments_on_issues/self.issue_metrics.total_issues
    #     self.issue_metrics.average_issue_closure_time = self.issue_metrics.average_issue_closure_time / 86400.0

    def publish_metrics(self):
        issue_metrics = IssueMetrics()
        for issue in self.gh_repo.get_issues(state='all'):
            self.process_issue(issue, issue_metrics)
            # print self.issue_metrics
        # self.calculate_metrics()
        return issue_metrics


def main():
    """
        argv1: Org Name
        argv2: Repo Name
    """
    import sys
    ia = IssueAnalyzer(sys.argv[1], sys.argv[2])
    metrics = ia.publish_metrics()
    print metrics


if __name__ == '__main__':
    main()
