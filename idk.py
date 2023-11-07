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
  if "t" in (money.lower()):
    money = money.replace ("t", "")
    return int(float(money) * 1000000000000)
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
  return str(round(int(money) / 1000000000000, 2)) + "t"