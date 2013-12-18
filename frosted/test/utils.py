from __future__ import absolute_import, division, print_function, unicode_literals

import textwrap
from collections import namedtuple

from frosted import checker
from pies.overrides import *

PyCF_ONLY_AST = 1024
__all__ = ['flakes', 'Node', 'LoggingReporter']


def flakes(input, *expectedOutputs, **kw):
    tree = compile(textwrap.dedent(input), "<test>", "exec", PyCF_ONLY_AST)
    results = checker.Checker(tree, **kw)
    outputs = [type(message) for message in results.messages]
    expectedOutputs = list(expectedOutputs)
    outputs.sort(key=lambda t: t.__name__)
    expectedOutputs.sort(key=lambda t: t.__name__)
    assert outputs == expectedOutputs, ('\n'
                                        'for input:\n'
                                        '%s\n'
                                        'expected outputs:\n'
                                        '%r\n'
                                        'but got:\n'
                                        '%s') % (input, expectedOutputs,
                                                 '\n'.join([str(o) for o in results.messages]))
    return results


class Node(namedtuple('Node', ['lineno', 'col_offset'])):
    """
        A mock AST Node
    """

    def __new__(cls, lineno, col_offset=0):
        return super(Node, cls).__new__(cls, lineno, col_offset)


class LoggingReporter(namedtuple('LoggingReporter', ['log'])):
    """
        A mock Reporter implementation
    """

    def flake(self, message):
        self.log.append(('flake', str(message)))

    def unexpected_error(self, filename, message):
        self.log.append(('unexpected_error', filename, message))

    def syntax_error(self, filename, msg, lineno, offset, line):
        self.log.append(('syntax_error', filename, msg, lineno, offset, line))
