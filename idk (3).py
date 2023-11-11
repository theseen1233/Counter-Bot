def abbreviate (money):
  if "k" in (money.lower()):
    money = money.replace ("k", "")
    return int(float(money) * 1000)
  if "m" in (money.lower()):
    money = money.replace ("m", "")
    return int(float(money) * 1000000)
  if "b" in (money.lower()):
    money = money.replace ("b", "")
    return int(float(money) * 1000000000)
  if (("t" in (money.lower())) and ("q" not in money.lower()) and ("o" not in money.lower())) :
    money = money.replace ("t", "")
    return int(float(money) * 1000000000000)
  if "qd" in (money.lower()):
    money = money.replace ("qd", "")
    return int(float(money) * 1000000000000000)
  if "qt" in (money.lower()):
    money = money.replace ("qt", "")
    return int(float(money) * 1000000000000000000)
  if (("s" in money.lower()) and ("p" not in money.lower())):
    money = money.replace ("s", "")
    return int(float(money) * 1000000000000000000000)
  if "sp" in (money.lower()):
    money = money.replace ("sp", "")
    return int(float(money) * 1000000000000000000000000)
  if "oct" in (money.lower()):
    money = money.replace ("oct", "")
    return int(float(money) * 1000000000000000000000000000)
  return money

def compact (money):
  if int (money) < 1000:
    return money
  if int(money) < 1000000:
    return str(round(int(money) / 1000, 2)) + "k"
  if int(money) < 1000000000:
    return str(round(int(money) / 1000000, 2)) + "m"
  if int(money) < 1000000000000:
    return str(round(int(money) / 1000000000, 2)) + "b"
  if int(money) < 1000000000000000:
    return str(round(int(money) / 1000000000000, 2)) + "t"
  if int(money) < 1000000000000000000:
    return str(round(int(money) / 1000000000000000, 2)) + "qd"
  if int(money) < 1000000000000000000000:
    return str(round(int(money) / 1000000000000000000, 2)) + "qt"
  if int(money) < 1000000000000000000000000:
    return str(round(int(money) / 1000000000000000000000, 2)) + "s"
  if int(money) < 1000000000000000000000000000:
    return str(round(int(money) / 1000000000000000000000000, 2)) + "sp"
  return str(round(int(money) / 1000000000000000000000000000, 2)) + "oct"