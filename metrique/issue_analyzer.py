from github import Github
from metrique.issue_metrics import IssueMetrics

print "log 1"
print "log 2"
class IssueAnalyzer(object):
    def __init__(self, org, repo):
        self.org = org
        self.repo = repo
        self.gh = Github()
        self.gh_repo = self.gh.get_repo("%s/%s" % (self.org, self.repo))

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

    def process_issue(self, issue, issue_metrics):
        self.update_issue_counters(issue, issue_metrics)
        self.process_closure_time(issue, issue_metrics)

    def publish_metrics(self):
        issue_metrics = IssueMetrics()
        for issue in self.gh_repo.get_issues(state='all'):
            print issue.title
            #print issue_metrics
            self.process_issue(issue, issue_metrics)
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
