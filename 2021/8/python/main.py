def decode(signals):
  signals = ["".join(sorted(sig)) for sig in signals.strip().split(" ")]

  lens = {}
  for sig in signals:
    if len(sig) not in lens:
      lens[len(sig)] = []
    lens[len(sig)].append(sig)

  zero = None
  one = lens[2][0]
  two = None
  three = None
  four = lens[4][0]
  five = None
  six = None
  seven = lens[3][0]
  eight = lens[7][0]
  nine = None

  for sig in lens[6]:
    if len(set(sig).intersection(one)) == 1:
      six = sig
    elif len(set(sig).intersection(four)) == 4:
      nine = sig
    else:
      zero = sig

  for sig in lens[5]:
    if len(set(sig).intersection(one)) == 2:
      three = sig
    elif len(set(sig).intersection(nine)) == 5:
      five = sig
    else:
      two = sig
  
  mapping = {
    0: zero,
    1: one,
    2: two,
    3: three,
    4: four,
    5: five,
    6: six,
    7: seven,
    8: eight,
    9: nine,
  }

  return {v: str(k) for k,v in mapping.items()}

with open('../input.txt') as f:
  output_sum = 0

  for line in f.readlines():
    signals, output = line.strip().split("|")
    mapping = decode(signals)
    output = ["".join(sorted(s.strip())) for s in output.strip().split(" ")]
    output = "".join(mapping[s] for s in output)
    output_sum += int(output)

  print(output_sum)