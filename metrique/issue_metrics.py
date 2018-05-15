import copy


class IssueMetrics(object):
    def __init__(self):
        self.total_issues = 0
        self.open_issues = 0
        self.closed_issues = 0
        self.longest_issue = None
        self.max_closure_time = 0

    def __eq__(self, other):
        return other.to_dict() == self.__dict__

    def __repr__(self):
        string = ""
        for key, value in self.__dict__.items():
            string += str(key) + " : " + str(value) + "\n"
        return string

    def to_dict(self):
        return copy.deepcopy(self.__dict__)
