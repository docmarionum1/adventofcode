class Node:
  def __init__(self, parent, size=0):
    self.parent = parent
    if size:
      self.children = None
    else:
      self.children = {}
    self.size = size

  def total_size(self):
    if self.children:
      return sum([c.total_size() for c in self.children.values()])

    return self.size

lines = open('input.txt').read().splitlines()

root = Node(None)
cwd = root
all_dirs = []
i = 0

while i < len(lines):
  cmd = lines[i]
  i += 1
  cmd, *args = cmd[2:].strip().split(' ')
  if cmd == "ls":
    while (i < len(lines)) and (lines[i][0] != "$"):
      t, name = lines[i].split(" ")
      n = Node(cwd, 0 if t == "dir" else int(t))
      if t == "dir":
        all_dirs.append(n)
      cwd.children[name] = n
      i += 1
  else:
    path = args[0]
    if path == "..":
      cwd = cwd.parent
    elif path == "/":
      cwd = root
    else:
      cwd = cwd.children[path]
  
# part 1
s = 0
for dir in all_dirs:
  ds = dir.total_size()
  if ds <= 100000:
    s += ds

print("Part 1:", s)

# part 2
disk_size = 70000000
needed_space = 30000000
current_size = root.total_size()
to_delete = current_size - (disk_size - needed_space)

s = current_size
for dir in all_dirs:
  ds = dir.total_size()
  if (ds >= to_delete) and (ds < s):
    s = ds

print("Part 2:", s)