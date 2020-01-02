"""
Defines a special Termination Error which can be catched by model. Used for syscall 10
"""


__author__ = "Elnifio"


class Termination(ValueError):
    pass