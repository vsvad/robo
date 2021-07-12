#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class RobocodeError(Exception):
    def __str__(self):
        res = ""
        for e in self.args:
            res += f"строка {e['line']}: {e['text']}\n"
        return res.strip()
