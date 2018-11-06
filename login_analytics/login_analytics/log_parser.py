# -*- coding: utf-8 -*-

"""
Implements Abstract Parser.
"""


class BaseLogParser(object):
    """
    Base class for log parser
    """

    def flatten(self, dct):
        """
        Flatten a dictionary data (usually from json)

        :param dct:
        :return: another dictionary with no nesting.
        """
