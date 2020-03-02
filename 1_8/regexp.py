import re


def calculate(data, findall):
    matches = findall(r"\b[abc][+-]{0,}=\d{0,}[abc]{0,}[+-]\d{0,}\b", data, re.MULTILINE)  # Если придумать хорошую регулярку, будет просто
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        data[v1] = data.get(v2, 0) + int(n or 0)

    return data
