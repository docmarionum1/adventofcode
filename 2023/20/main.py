from aoc.common import *

lines = read_input()

node_types = {'%': 'flipflop', '&': 'conjunction', '': 'identity'}
pulse_counts = {False: 0, True: 0}
pulse_queue = []

class Node:
  def __init__(self, name, node_type):
    self.name = name
    self.node_type = node_types[node_type]
    self.inputs = {}
    self.outputs = []
    self.state = False

  def pulse(self, input, val):
    # Track pulses
    pulse_counts[val] += 1

    if self.node_type == 'flipflop':
      if val: # Do nothing on high pulse
        return

      self.state = not self.state

      for output in self.outputs:
        pulse_queue.append((output, self.name, self.state))

    if self.node_type == 'conjunction':
      self.inputs[input] = val
      output_val = not all(self.inputs.values())
      for output in self.outputs:
        pulse_queue.append((output, self.name, output_val))

    if self.node_type == 'identity':
      for output in self.outputs:
        pulse_queue.append((output, self.name, val))


  def __repr__(self):
    return f"{self.node_type} {self.inputs} {self.outputs}"


nodes = {}

for line in lines:
  node_type, node_name = re.match(r'([%&]{0,1})([a-z]+) -> .*', line).groups()
  nodes[node_name] = Node(node_name, node_type)

for line in lines:
  input_node, output_nodes = re.match(r'[%&]{0,1}([a-z]+) -> (.*)', line).groups()
  output_nodes = split(output_nodes, ",")
  nodes[input_node].outputs = output_nodes
  for output_node in output_nodes:
    if output_node not in nodes:
      nodes[output_node] = Node(output_node, '')
    nodes[output_node].inputs[input_node] = False

part1 = None
part2 = dict(nodes[list(nodes['rx'].inputs.keys())[0]].inputs)

for i in range(1, 5000):
  pulse_queue.append(('broadcaster', 'button', False))
  while pulse_queue:
    output, input, val = pulse_queue.pop(0)
    nodes[output].pulse(input, val)

    # Handle part 2
    if output == "nc":
      for j,v in nodes["nc"].inputs.items():
        if v and part2[j] is False:
          part2[j] = i

  if i == 1000:
    part1 = np.product(list(pulse_counts.values()))

print("Part 1:", part1)
print("Part 2:", functools.reduce(math.lcm, part2.values()))