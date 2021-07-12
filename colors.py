#!/usr/bin/env python3
# -*- coding: utf-8 -*-

colornames = {
    "black": "#000000",
    "white": "#ffffff",
    "gray": "#7f7f7f",
    "red": "#ff0000",
    "green": "#007f00",
    "lime": "#00ff00",
    "blue": "#0000ff",
    "cyan": "#00ffff",
    "yellow": "#ffff00",
    "orange": "#ff7f00",
    "purple": "	#800080",
    "gold": "#ffd700",
    "magenta": "#ff00ff",
}

ru_colors = {
    "чёрный": "black",
    "белый": "white",
    "серый": "gray",
    "красный": "red",
    "зелёный": "green",
    "лаймовый": "lime",
    "синий": "blue",
    "голубой": "cyan",
    "жёлтый": "yellow",
    "оранжевый": "orange",
    "фиолетовый": "purple",
    "золотой": "gold",
    "розовый": "magenta",
    "малиновый": "magenta",
    "рыжий": "orange",
}


def isvalidcolor(s):
    if s in ru_colors.keys():
        s = ru_colors[s]
    if s in colornames.keys():
        return True
    if not s or s[0] != "#":
        return False
    if len(s) not in [4, 7]:
        return False
    for i in s.lower()[1:]:
        if i not in "abcdef1234567890":
            return False
    return True
