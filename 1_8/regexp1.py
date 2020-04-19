def calculate(data, findall):
    matches = findall(r"([abc])([+-]?=)([abc]?)([+-]?\d*)")  # Если придумать хорошую регулярку, будет просто
    # for m in matches:
    #    print(m)
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        #     # Если бы могло быть только =, вообще одной строкой все считалось бы, вот так:
        #     data[v1] = data.get(v2, 0) + int(n or 0)
        print(v1, s, v2, n)
        print(f"v1{v1}, s{s}, v2{v2}, n{n}")
        q1 = data[v1]
        q2 = data.get(v2, 0)
        q3 = int(n or 0)
        if s == "=":
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s == "+=":
            if q2 != 0 and q3 != 0:
                data[v1] = data[v1] + (data.get(v2, 0) + int(n or 0))
            elif q2 == 0 and q3 != 0:
                data[v1] = data[v1] + int(n or 0)
            elif q2 != 0 and q3 == 0:
                data[v1] = data[v1] + data.get(v2, 0)
        elif s == "-=":
            if q2 != 0 and q3 != 0:
                data[v1] = data[v1] - (data.get(v2, 0) + int(n or 0))
            elif q2 == 0 and q3 != 0:
                data[v1] = data[v1] - int(n or 0)
            elif q2 != 0 and q3 == 0:
                data[v1] = data[v1] - data.get(v2, 0)
        print(data)
    return data
