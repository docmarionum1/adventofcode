# Used to give each room and amphipod a unique ID for hashing
IDS = iter(range(100))

class Node:
    def __init__(self, room, contents=None):
        self.id = next(IDS)
        self.room = room
        self.neighbors = set()
        self.contents = None
        if contents:
            contents._set_node(self)

    def add_neighbor(self, node):
        self.neighbors.add(node)
        node.neighbors.add(self)
        return self

    def is_outside_room(self):
        return (
            (self.room is None) and 
            (len([n for n in self.neighbors if n.room]) > 0)
        )

    def is_pure(self):
        if self.room:
            other = [n for n in self.neighbors if n.room == self.room][0]
            return (
                (
                    (self.contents is None) or 
                    (self.contents.type == self.room)
                ) and
                (
                    (other.contents is None) or 
                    (other.contents.type == other.room)
                )
            )

        return True

    def is_end(self):
        return len(self.neighbors) == 1

    def __repr__(self):
        return f"{str(self.room)[0]}{self.id}"

class Amphipod:
    def __init__(self, type, node=None):
        self.id = next(IDS)
        self.type = type
        self.cost = 10**("abcd".index(self.type))
        self.node = None
        if node:
            self._set_node(node)

    def _set_node(self, node):
        assert node.contents is None

        if self.node:
            self.node.contents = None
        
        node.contents = self
        self.node = node

    def get_valid_moves(self):
        if (self.node.room == self.type) and self.node.is_pure():
            return []

        # Stay in the back of the room if it's already there and correct
        if (self.node.room == self.type) and self.node.is_end():
            return []

        visited = set()
        to_visit = [(self.node, 0)]
        valid = []

        while to_visit:
            curr, m = to_visit.pop()
            visited.add(curr)

            # If we can to go to the back of our room, go straight there
            if (curr.room == self.type) and curr.is_end():
                return [(curr, m)]

            if (
                (curr != self.node) and 
                (not curr.is_outside_room()) and
                ((self.node.room is not None) or curr.room) and 
                ((curr.room is None) or (curr.room == self.type)) and
                curr.is_pure()
            ):
                valid.append((curr, m))

            for n in curr.neighbors:
                if n not in visited and n.contents is None:
                    #if self.node.room is None and n.room and n.room != self.type:
                    #    continue
                    to_visit.append((n, m+1))

        return valid

    def __repr__(self):
        return f"{self.type}{self.id}@{self.node}"

amphipods = {k: [Amphipod(k) for _ in range(2)] for k in "abcd"}

# Mine
#############
#...........#
###B#A#A#D###
  #B#C#D#C#
  #########

room_a = Node("a", amphipods["b"].pop()).add_neighbor(Node("a", amphipods["b"].pop()))
room_b = Node("b", amphipods["a"].pop()).add_neighbor(Node("b", amphipods["c"].pop()))
room_c = Node("c", amphipods["a"].pop()).add_neighbor(Node("c", amphipods["d"].pop()))
room_d = Node("d", amphipods["d"].pop()).add_neighbor(Node("d", amphipods["c"].pop()))

hallway = Node(None)
hallway = Node(None).add_neighbor(hallway)
hallway = Node(None).add_neighbor(hallway).add_neighbor(room_d)
hallway = Node(None).add_neighbor(hallway)
hallway = Node(None).add_neighbor(hallway).add_neighbor(room_c)
hallway = Node(None).add_neighbor(hallway)
hallway = Node(None).add_neighbor(hallway).add_neighbor(room_b)
hallway = Node(None).add_neighbor(hallway)
hallway = Node(None).add_neighbor(hallway).add_neighbor(room_a)
hallway = Node(None).add_neighbor(hallway)
hallway = Node(None).add_neighbor(hallway)

def get_amphipods(state):
    all_nodes = set()
    to_visit = [state]

    while to_visit:
        curr = to_visit.pop()
        all_nodes.add(curr)
        for n in curr.neighbors:
            if n not in all_nodes:
                to_visit.append(n)

    amphipods = []
    for n in all_nodes:
        if n.contents:
            amphipods.append(n.contents)

    return amphipods

def is_solved(amphipods):
    for a in amphipods:
        if a.type != a.node.room:
            return False

    return True

def hash_amphipods(amphipods):
    return str(sorted(amphipods, key=lambda amp: amp.id))

memo = {}

def min_cost_to_solve(state):
    amphipods = get_amphipods(state)
    hashed = hash_amphipods(amphipods)

    if hashed in memo:
        return memo[hashed]

    if is_solved(amphipods):
        return 0

    min_cost = 2**63

    for amphipod in amphipods:
        for node, moves in amphipod.get_valid_moves():
            # Move the amphipod, saving it's previous location
            original_node = amphipod.node
            amphipod._set_node(node)

            cost = min_cost_to_solve(state)
            cost += moves * amphipod.cost
            if cost < min_cost:
                min_cost = cost

            # Revert the movement back to the original state
            amphipod._set_node(original_node)

    memo[hashed] = min_cost

    return min_cost

print(min_cost_to_solve(hallway))