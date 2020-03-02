import re


exp = r"\d+"
print(re.findall(exp, "мама вымыла 2 рамы"))
exp = "....мы"
print(re.findall(exp, "мама вымыла 2 рамы"))
exp = "м.+?ы"
print(re.findall(exp, "мама вымыла 2 рамы"))
exp = "мы"
print(re.findall(exp, "мама вымыла 2 рамы"))
exp = r"а.\D"
print(re.findall(exp, "мама вымыла 2 рамы"))
exp = "м.*?ы"
print(re.findall(exp, "мама вымыла 2 рамы"))
exp = "м.*ы"
print(re.findall(exp, "мама вымыла 2 рамы"))
