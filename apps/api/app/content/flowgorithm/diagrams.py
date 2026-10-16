"""Хичээлүүдийн засварлаж, ажиллуулж болох бүтцэт схемүүд.

Frontend-ийн lib/flowgorithm/model.ts дахь version 1 форматтай таарна.
Хэлний plaintext утгыг хадгалж, Flowgorithm сургалтад тусгай засварлагч ашиглана.

`DIAGRAMS` нь хичээл бүрийн эхлэл схем (даалгаврын эхлэл), даалгаврын жишиг
шийдлийг мөн эдгээр туслахаар `diagram()` болгоно.
"""

import copy
import json
from itertools import count


def declare(name: str, data_type: str = "Integer") -> dict:
    return {"kind": "declare", "name": name, "dataType": data_type}


def assign(name: str, expression: str) -> dict:
    return {"kind": "assign", "name": name, "expression": expression}


def output(expression: str) -> dict:
    return {"kind": "output", "expression": expression, "newline": True}


def read(name: str) -> dict:
    return {"kind": "input", "name": name}


def ask(name: str, prompt: str) -> list[dict]:
    return [output(json.dumps(prompt, ensure_ascii=False)), read(name)]


def condition(expression: str, yes: list[dict], no: list[dict]) -> dict:
    return {"kind": "if", "expression": expression, "trueBranch": yes, "falseBranch": no}


def while_loop(expression: str, body: list[dict]) -> dict:
    return {"kind": "while", "expression": expression, "body": body}


def for_loop(end: str, body: list[dict], *, start: str = "1", step: str = "1") -> dict:
    return {
        "kind": "for",
        "name": "i",
        "start": start,
        "end": end,
        "step": step,
        "direction": "inc",
        "body": body,
    }


SCORE_CHECK = "(score < 0) or (score > 100)"
RETRY_SCORE = while_loop(SCORE_CHECK, ask("score", "0–100 хооронд дахин оруул:"))

DIAGRAMS: dict[str, list[dict]] = {
    # Модул 0–1: Declare-ийг «huvisagch-turul», Input-ийг «input-mendchilgee» заана.
    # Даалгавар бүр оролт уншдаг тул оролт авах Declare + Input бэлэн (C-ийн бэлэн
    # `scanf` мөртэй адил); сурагч зөвхөн Output-ийг засаж, нэмнэ. Модул 0-д текст
    # заагаагүй тул Input-ийн өмнө асуулт алга — засварлагч хувьсагчийн нэрээр асууна.
    "program-gej-yu-ve": [
        declare("price1, price2"),
        read("price1"),
        read("price2"),
        output("2000 + 1500"),
    ],
    "algoritm-alham": [declare("a, b"), read("a"), read("b"), output("a + b / 2")],
    "orolt-garalt": [
        declare("length, width"),
        read("length"),
        read("width"),
        output("length * width"),
    ],
    "suulgah-ehleh": [declare("age"), read("age"), output('"Сайн уу!"'), output("age")],
    "durs-sum": [declare("n"), read("n"), output("n"), output('"Хөөрлөө!"')],
    "anhnii-output": [
        declare("a, b"),
        read("a"),
        read("b"),
        output('"Сайн уу, дэлхий!"'),
        output("a + b"),
        output('"a + b"'),
    ],
    # Input бэлэн (дээрхтэй адил) — сурагч зөвхөн Declare нэмнэ. Нийт оноог бодох
    # Output нь бүгдийг String гэж зарлахад алдаа заана: төрлөө сонгох нь чухал.
    "huvisagch-turul": [
        read("name"),
        read("exams"),
        read("average"),
        output("name"),
        output("exams"),
        output("average"),
        output("average * exams"),
    ],
    "utga-onooh": [
        declare("score"),
        read("score"),
        output("score"),
        assign("score", "score + 5"),
        output("score"),
    ],
    "input-mendchilgee": [
        declare("name", "String"),
        *ask("name", "Нэрээ оруулна уу:"),
        output('"Сайн уу, " & name & "!"'),
    ],
    "niilber-dundaj": [
        declare("a, b, total, average", "Real"),
        *ask("a", "Эхний тоо:"),
        *ask("b", "Хоёр дахь тоо:"),
        assign("total", "a + b"),
        assign("average", "total / 2"),
        output('"Нийлбэр: " & total'),
        output('"Дундаж: " & average'),
    ],
    "operator-uldegdel": [
        output("2 + 3 * 4"),
        output("(2 + 3) * 4"),
        output("8 mod 2"),
        output("9 mod 2"),
    ],
    "alhamaar-shalgah": [
        declare("x, y"),
        assign("x", "4"),
        assign("y", "x + 2"),
        assign("x", "10"),
        assign("y", "y + x"),
        output("x"),
        output("y"),
    ],
    "hartsuulalt-boolean": [
        declare("score"),
        declare("passed", "Boolean"),
        assign("score", "60"),
        assign("passed", "score >= 60"),
        output("passed"),
    ],
    "if-hoyor-zam": [
        declare("score"),
        *ask("score", "Оноогоо оруул (0–100):"),
        condition("score >= 60", [output('"Тэнцлээ"')], [output('"Дахин давтаарай"')]),
        output('"Шалгалт дууслаа"'),
    ],
    "davhar-if": [
        declare("number"),
        *ask("number", "Бүхэл тоо оруул:"),
        condition(
            "number > 0",
            [output('"Эерэг"')],
            [condition("number < 0", [output('"Сөрөг"')], [output('"Тэг"')])],
        ),
    ],
    "logik-zuv-orolt": [
        declare("score"),
        *ask("score", "0–100 хооронд бүхэл оноо оруул:"),
        condition(
            "(score >= 0) and (score <= 100)",
            [output('"Зөв хүрээний оноо"')],
            [output('"0–100 хооронд оруулна уу"')],
        ),
    ],
    "ih-toog-oloh": [
        declare("a, b", "Real"),
        *ask("a", "Эхний тоо:"),
        *ask("b", "Хоёр дахь тоо:"),
        condition(
            "a > b", [output("a")], [condition("a < b", [output("b")], [output('"Тэнцүү"')])]
        ),
    ],
    "tegsh-sondgoi": [
        declare("number"),
        *ask("number", "Бүхэл тоо оруул:"),
        condition("number mod 2 == 0", [output('"Тэгш"')], [output('"Сондгой"')]),
    ],
    "while-davtalt": [
        declare("i"),
        assign("i", "1"),
        while_loop("i <= 5", [output("i"), assign("i", "i + 1")]),
        output('"Дууслаа"'),
    ],
    "for-tooluur": [declare("i"), for_loop("5", [output("i")])],
    "niilber-tsugluulah": [
        declare("n, i, total"),
        *ask("n", "1 буюу түүнээс их бүхэл тоо оруул:"),
        condition(
            "n >= 1",
            [assign("total", "0"), for_loop("n", [assign("total", "total + i")]), output("total")],
            [output('"1 буюу түүнээс их бүхэл тоо оруул"')],
        ),
    ],
    "orolt-dahin-asuu": [
        declare("score"),
        *ask("score", "0–100 хооронд бүхэл оноо оруул:"),
        RETRY_SCORE,
        output('"Хүлээн авсан оноо: " & score'),
    ],
    "tusul-delguur": [
        declare("price, quantity, budget, total"),
        *ask("price", "Нэгж үнэ (бүхэл төгрөг):"),
        *ask("quantity", "Тоо ширхэг:"),
        *ask("budget", "Өөрт байгаа мөнгө (бүхэл төгрөг):"),
        condition(
            "(price <= 0) or (quantity <= 0) or (budget < 0)",
            [output('"Үнэ, ширхэг эерэг; мөнгө 0-ээс багагүй байна."')],
            [
                assign("total", "price * quantity"),
                output('"Нийт үнэ: " & total'),
                condition(
                    "budget >= total",
                    [output('"Үлдэх мөнгө: " & (budget - total)')],
                    [output('"Дутах мөнгө: " & (total - budget)')],
                ),
            ],
        ),
    ],
    "tusul-dundaj-soril": [
        declare("i, score, total"),
        declare("average", "Real"),
        assign("total", "0"),
        for_loop(
            "3",
            [
                output('"Оноо " & i & " (0–100):"'),
                read("score"),
                RETRY_SCORE,
                assign("total", "total + score"),
            ],
        ),
        assign("average", "total / 3"),
        output('"Дундаж: " & average'),
        condition("average >= 60", [output('"Тэнцлээ"')], [output('"Дахин давтаарай"')]),
    ],
}


def diagram(nodes: list[dict]) -> str:
    """Засварлагчийн ачаалах JSON — дүрс бүрт `node-N` гэсэн id өгнө."""
    nodes = copy.deepcopy(nodes)
    ids = count(1)

    def identify(items: list[dict]) -> None:
        for node in items:
            node["id"] = f"node-{next(ids)}"
            for branch in ("body", "trueBranch", "falseBranch"):
                if branch in node:
                    identify(node[branch])

    identify(nodes)
    return json.dumps(
        {"format": "medleghub-flowgorithm", "version": 1, "nodes": nodes},
        ensure_ascii=False,
        indent=2,
    )


def lesson_diagram(slug: str) -> str:
    return diagram(DIAGRAMS[slug])
