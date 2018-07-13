#!/usr/local/bin/python
# -*- coding: utf-8 -*-


class BaseFilter(object):
    '''Base class for filters
    '''

    def check(self, row):
        return True

    def __call__(self, df):
        return df[[self.check(row) for k, row in df.iterrows()]]


class KeyFilter(BaseFilter):
    '''KeyFilter has 1 (principal) proptery

    key_condition: {key:condition}
    '''

    def __init__(self, key_condition):
        super(KeyFilter, self).__init__()
        self.key_condition = key_condition
    
    def check(self, row):
        return all([condition(row[key]) for key, condition in self.key_condition.items()])

    def __imul__(self, other):
        for key, condition in other.key_condition.items():
            if key in self.key_condition:
                self.key_condition.update({key: lambda x: self.key_condition[key](x) and condition(x)})
            else:
                self.key_condition.update({key: condition})


class StatFilter(BaseFilter):
    '''KeyFilter has 1 (principal) proptery

    key_condition: key condition
    stat: information of statistics
    '''
    def __init__(self, key_condition, stat):
        super(StatFilter, self).__init__()
        self.key_condition = key_condition
        self.stat = stat
    
    def check(self, row):
        return all([condition(row[key], self.stat[key]) for key, condition in self.key_condition.items()])
