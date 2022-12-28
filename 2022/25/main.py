from functools import reduce

numbers = open('input.txt').read().splitlines()

digits = {
  "2": 2,
  "1": 1,
  "0": 0,
  "-": -1,
  "=": -2,    
}

rev = {v:k for k,v in digits.items()}

def to_decimal(snafu):
  s = 0
  for i in range(len(snafu)):
    s += digits[snafu[i]]*(5**(len(snafu) - 1 - i))

  return s

def to_snafu(decimal):
  i = 0
  snafu = ""
  carry = 0
  invert = -1 if decimal < 0 else 1
  while decimal:
    remainder = decimal % (invert * 5**(i+1))
    digit = (remainder // 5**i + carry)
    if digit > 2:
      carry = 1
      digit -= 5
    elif digit < -2:
      carry = -1
      digit += 5
    else:
      carry = 0
    snafu = rev[digit] + snafu
    decimal -= remainder
    i += 1

  return snafu

print("Part 1v1:", to_snafu(sum(map(to_decimal, numbers))))

def add_snafu(a, b):
  """
  Add two numbers in snafu format without converting bases
  """
  max_len = max(len(a), len(b))
  a = a.zfill(max_len)
  b = b.zfill(max_len)
  c = ""
  i = max_len - 1
  carry = 0
  while i > -1:
    s = digits[a[i]] + digits[b[i]] + carry

    if s < -2:
      carry = -1
      s = s + 5
    elif s > 2:
      carry = 1
      s = s - 5
    else:
      carry = 0

    c = rev[s] + c
    i -= 1

  if carry:
    c = rev[carry] + c

  return c

print("Part 1v2:", reduce(add_snafu, numbers))