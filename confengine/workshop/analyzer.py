from github import Github


class IssueMetrics(object):
    def __init__(self):
        self.total_issues = 0
        self.open_issues = 0
        self.closed_issues = 0
        self.total_comments_on_issues = 0
        self.average_issue_closure_time = 0
        self.average_comments_per_issue = 0
        self.longest_issue = None
        self.issue_with_most_comments = None

    def __repr__(self):
        string = ""
        for key, value in self.__dict__.items():
            string += str(key) + " : " + str(value) + "\n"
        return string


class IssueAnalyzer(object):
    def __init__(self, org, repo):
        self.org = org
        self.repo = repo
        self.gh = Github()
        self.gh_repo = self.gh.get_repo("%s/%s" % (self.org, self.repo))
        self.issue_metrics = IssueMetrics()

        # Temp Variables
        self.total_issue_closure_time = 0
        self.max_issue_closure_time = 0
        self.max_issue_comments = 0

    def is_issue_closed(self, issue):
        return issue.state == 'closed'

    def is_issue_open(self, issue):
        return issue.state == 'open'

    def update_issue_counters(self, issue):
        self.issue_metrics.total_issues += 1
        if self.is_issue_open(issue):
            self.issue_metrics.open_issues += 1
        elif self.is_issue_closed(issue):
            self.issue_metrics.closed_issues += 1

    def process_closure_time(self, issue):
        if issue.state == 'closed':
            issue_closure_time = (issue.closed_at - issue.created_at).total_seconds()
            if issue_closure_time > self.max_issue_closure_time:
                self.max_issue_closure_time = issue_closure_time
                self.issue_metrics.longest_issue = issue
            self.total_issue_closure_time += issue_closure_time

    def process_comments(self, issue):
        self.issue_metrics.total_comments_on_issues += issue.comments
        if issue.comments > self.max_issue_comments:
            self.issue_metrics.issue_with_most_comments = issue

    def process_issue(self, issue):
        self.update_issue_counters(issue)
        self.process_closure_time(issue)
        self.process_comments(issue)

    def calculate_metrics(self):
        self.issue_metrics.average_issue_closure_time = self.total_issue_closure_time/self.issue_metrics.closed_issues
        self.issue_metrics.average_comments_per_issue = self.issue_metrics.total_comments_on_issues/self.issue_metrics.total_issues
        self.issue_metrics.average_issue_closure_time = self.issue_metrics.average_issue_closure_time / 86400.0

    def publish_metrics(self):
        for issue in self.gh_repo.get_issues(state='all'):
            print issue
            self.process_issue(issue)
            # print self.issue_metrics
        self.calculate_metrics()
        return self.issue_metrics


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
