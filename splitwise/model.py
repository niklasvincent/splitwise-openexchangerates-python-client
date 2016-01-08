from collections import namedtuple

Category = namedtuple("Category", ["id", "name", "parent"])

class Expense(object):

    def __init__(self, id, user_id, year, month, day, week, description, category, cost):
        self.id = id
        self.user_id = user_id
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.description = description
        self.category = category
        self.cost = cost

    def asList(self):
        return [
            self.id,
            "%d-%d-%d" % (self.year, self.month, self.day),
            self.description,
            self.cost,
            self.category.parent,
            self.category.name
        ]
