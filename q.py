check = "00:01"
def toUTC(t):
    t2 = int(t[:2])
    if t2 - 8 < 0:
        t2 += 24
    t2 -= 8
    t = str(t2) + t[2:]
    return t
print(toUTC(check))