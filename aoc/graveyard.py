# Graveyard; weren't necessary but maybe useful later

def consumes_all(numbers, pattern):
  i = 0
  j = 0
  while j < len(numbers):
    if pattern[i % len(pattern)] != numbers[j]:
      return False

    i += 1
    j += 1

  return True

def find_pattern(df):
  numbers = df[1].values
  string = ','.join(df[1].astype(str))

  for i in range(len(numbers)):
    for j in range(i+1, len(numbers)):
      substring = ','.join(numbers[i:j].astype(str))
      if string.count(substring) == 1:
        break

      if (
        string.count(substring) > 1 and
        string.count(substring+","+substring) > 0 and
        consumes_all(numbers[i:], numbers[i:j])
      ):
        return numbers[i:j]