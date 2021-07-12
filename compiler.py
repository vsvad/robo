#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
from math import sin, cos, pi
import random

from moves import *
from colors import *
from exceptions import RobocodeError

sys.setrecursionlimit(1_000_000)

ext = None
end_styles = {
    "нет": "Flat",
    "квадрат": "Square",
    "круг": "Round"
}


def randombyte():
    b = hex(random.randint(0, 255))[2:]
    if len(b) == 1:
        b = "0" + b
    return b


def randomcolor():
    res = "#"
    for i in range(3):
        res += randombyte()
    return res


def randomheader():
    random_a = [
        "случайны",
        "красивы",
        "странны",
        "обычны",
        "круто",
        "умны",
        "весёлы",
        "дики"
    ]
    random_b = [
        "прохожий",
        "пейзаж",
        "алгоритм",
        "случай",
        "код",
        "мой автор",
        "клоун",
        "лев"
    ]
    random_c = [
        "судьба твоя",
        "картина",
        "программа",
        "ёлка",
        "персона",
        "идея",
        "выдумка",
        "затея",
        "кошка"
    ]
    if sum(os.urandom(1024)) % 2:
        a = random.choice(random_a) + "й "
        lst = random_b
    else:
        a = random.choice(random_a)[:-1] + "ая "
        lst = random_c
    b = random.choice(lst)
    return (a + b).title()


def get_point_from(x, y, d, angle):
    rad = angle * pi / 180
    px = x + d * cos(rad)
    py = y - d * sin(rad)
    return px, py


def roboscript2robocode(code, in_statement=False):
    global x, y
    res = ""
    err = []
    if not in_statement:
        x = 0
        y = 0
    saved_code = ""
    saved_data = {}
    do = True
    indent = 0
    for i, line in enumerate(code.splitlines(), start=1):
        orig_line = re.sub("\\-\\-.*$", "", line.strip())
        line = orig_line.split(" ")
        if len(line) == 1:
            cmd = line[0].strip()
            args = []
        else:
            cmd, *args = line
        args = [j for j in args if j.strip()]
        if not do and cmd == "повторить":
            indent += 1
            if indent >= 1000:
                err.append(
                    {"line": i, "text": "слишком большая вложенность"}
                )
                raise RobocodeError(*err)
        elif not do and cmd != "конец":
            saved_code += orig_line + "\n"
        elif not do and cmd == "конец" and indent == 1:
            do = True
            res += roboscript2robocode(saved_code * saved_data["times"], True)
            res += "\n"
            indent -= 1
        elif not cmd.strip():
            pass
        elif cmd == "не":
            if args == []:
                err.append(
                    {"line": i, "text": "отрицание без причины"}
                )
            elif args[0] == "рисовать":
                if len(args) > 1:
                    err.append(
                        {"line": i, "text": "дополнение, которое не требуется"}
                    )
                else:
                    res += "HIDDEN\n"
            else:
                err.append(
                    {"line": i, "text": f'что это вообще такое - "{cmd + " " + args[0]}"?'}
                )
        elif cmd == "рисовать":
            if len(args) > 0:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            else:
                res += "VISIBLE\n"
        elif cmd in ru_directions.keys():
            if len(args) > 1:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            else:
                if len(args) == 1:
                    mv = args[0]
                    if not mv.isdigit():
                        err.append(
                            {"line": i, "text": "не число"}
                        )
                    else:
                        mv = int(mv)
                else:
                    mv = MOVE_STEP
                d = ru_directions[cmd]
                if d[0] == "x":
                    if d[1] == "+":
                        x += mv
                    elif d[1] == "-":
                        x -= mv
                elif d[0] == "y":
                    if d[1] == "+":
                        y += mv
                    elif d[1] == "-":
                        y -= mv
                res += f"{x}x{y}\n"
        elif cmd == "цвет":
            if len(args) > 1:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            else:
                if not args:
                    args.append(randomcolor())
                clr = args[0].lower()
                if not isvalidcolor(clr):
                    err.append(
                        {"line": i, "text": "не цвет"}
                    )
                else:
                    if clr in ru_colors.keys():
                        clr = ru_colors[clr]
                    res += "SETCOLOR " + clr + "\n"
        elif cmd == "фон":
            if len(args) > 1:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            else:
                if not args:
                    args.append(randomcolor())
                clr = args[0].lower()
                if not isvalidcolor(clr):
                    err.append(
                        {"line": i, "text": "не цвет"}
                    )
                else:
                    res += "SETBG " + clr + "\n"
        elif cmd == "перо":
            if len(args) > 1:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            elif not args:
                args.append("4")
            else:
                n = args[0]
                if not n.isdigit():
                    err.append(
                        {"line": i, "text": "не число"}
                    )
                else:
                    res += "SETWIDTH " + n + "\n"
        elif cmd == "концы":
            if len(args) > 1:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            else:
                if not args:
                    args.append("нет")
                if args[0] not in "квадрат нет круг".split():
                    err.append(
                        {"line": i, "text": "не конец линии"}
                    )
                else:
                    res += "SETCAP " + end_styles[args[0]] + "\n"
        elif cmd == "повторить":
            if len(args) > 1:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            elif not args:
                args.append("2")
            else:
                n = args[0]
                if not n.isdigit():
                    err.append(
                        {"line": i, "text": "не число"}
                    )
                    raise RobocodeError(*err)
                else:
                    n = int(n)
                    do = False
                    saved_data["times"] = n
                    indent += 1
        elif cmd == "круг":
            err = False
            for n in args:
                if not n.isdigit():
                    err.append(
                        {"line": i, "text": "не число"}
                    )
                    err = True
            if err:
                continue

            if len(args) == 1:
                r = int(args[0])
                args = [x - r, y - r, x + r, y + r]
            elif len(args) == 2:
                args = [x, y, x + int(args[0]), y + int(args[1])]
            elif len(args) == 3:
                r = int(args[2])
                args = [
                    int(args[0]) - r,
                    int(args[1]) - r,
                    int(args[0]) + r,
                    int(args[1]) + r
                ]
            elif len(args) > 4:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            elif not args:
                err.append(
                    {"line": i, "text": "недостаточно данных"}
                )
            args[2] -= args[0]
            args[3] -= args[1]
            args = list(map(str, args))
            res += "CIRCLE " + " ".join(args) + "\n"
        elif cmd == "заголовок":
            header = " ".join(args)
            if not header:
                header = randomheader()
            res += "TITLE " + header + "\n"
        elif cmd.rstrip("!") == "заново":
            res += "CLEAR\n"
        elif cmd == "иди":
            if len(args) > 2:
                err.append(
                    {"line": i, "text": "дополнение, которое не требуется"}
                )
            elif len(args) < 2:
                err.append(
                    {"line": i, "text": "недостаточно данных"}
                )
            else:
                for n in args:
                    if not n.isdigit():
                        err.append(
                            {"line": i, "text": "не число"}
                        )
                else:
                    args = list(map(int, args))
                    args[1] %= 360
                    x, y = get_point_from(x, y, args[0], args[1])
                    x = round(x)
                    y = round(y)
                    res += f"{x}x{y}" + "\n"
        elif cmd == "робокод":
            res += " ".join(args)
        else:
            err.append(
                {"line": i, "text": f"что это вообще такое - \"{cmd}\"?"}
            )
    if not do:
        err.append(
            {"line": len(code.splitlines()), "text": f"где конец?"}
        )
    if err:
        raise RobocodeError(*err)
    res = res.strip()
    return res
