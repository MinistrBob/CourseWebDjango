def calculate(data, findall):
    matches = findall(r"([abc])([+-]?=)([abc]?)([+-]?\d*)")
    for v1, s, v2, n in matches:
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
