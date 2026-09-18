import matplotlib.pyplot as plt
import networkx as nx

# Global counter for unique state names
state_counter = 0


def new_state():
    global state_counter
    state = "S" + str(state_counter)
    state_counter += 1
    return state


# NFA class
class NFA:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.transitions = {}

    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = []
        self.transitions[from_state][symbol].append(to_state)

    def merge(self, other):
        for state in other.transitions:
            if state not in self.transitions:
                self.transitions[state] = {}
            for symbol in other.transitions[state]:
                if symbol not in self.transitions[state]:
                    self.transitions[state][symbol] = []
                self.transitions[state][symbol] += other.transitions[state][
                    symbol
                ]


# Create NFA for a single character
def char_nfa(symbol):
    start = new_state()
    end = new_state()
    nfa = NFA(start, end)
    nfa.add_transition(start, symbol, end)
    return nfa


# Kleene star (*)
def star_nfa(nfa):
    start = new_state()
    end = new_state()
    result = NFA(start, end)
    result.add_transition(start, "e", nfa.start)
    result.add_transition(start, "e", end)
    result.add_transition(nfa.end, "e", nfa.start)
    result.add_transition(nfa.end, "e", end)
    result.merge(nfa)
    return result


# Concatenation
def concat_nfa(nfa1, nfa2):
    result = NFA(nfa1.start, nfa2.end)
    result.merge(nfa1)
    result.merge(nfa2)
    result.add_transition(nfa1.end, "e", nfa2.start)
    return result


# Union (using '/')
def union_nfa(nfa1, nfa2):
    start = new_state()
    end = new_state()
    result = NFA(start, end)
    result.add_transition(start, "e", nfa1.start)
    result.add_transition(start, "e", nfa2.start)
    result.add_transition(nfa1.end, "e", end)
    result.add_transition(nfa2.end, "e", end)
    result.merge(nfa1)
    result.merge(nfa2)
    return result


# Convert regex to NFA
def regex_to_nfa(regex):
    stack = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c.isalpha():
            nfa = char_nfa(c)
            if i + 1 < len(regex) and regex[i + 1] == "*":
                nfa = star_nfa(nfa)
                i += 1
            stack.append(nfa)
        elif c == "(":
            j = i
            balance = 0
            while i < len(regex):
                if regex[i] == "(":
                    balance += 1
                elif regex[i] == ")":
                    balance -= 1
                if balance == 0:
                    break
                i += 1
            sub_nfa = regex_to_nfa(regex[j + 1 : i])
            if i + 1 < len(regex) and regex[i + 1] == "*":
                sub_nfa = star_nfa(sub_nfa)
                i += 1
            stack.append(sub_nfa)
        elif c == "/":
            nfa1 = stack.pop()
            i += 1
            nfa2 = regex_to_nfa(regex[i:])
            return union_nfa(nfa1, nfa2)
        i += 1

    if not stack:
        return None

    result = stack[0]
    for nfa in stack[1:]:
        result = concat_nfa(result, nfa)
    return result


# Draw the NFA graph
def draw_nfa(nfa):
    G = nx.MultiDiGraph()
    for from_state in nfa.transitions:
        for symbol in nfa.transitions[from_state]:
            for to_state in nfa.transitions[from_state][symbol]:
                G.add_edge(from_state, to_state, label=symbol)

    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="lightyellow",
        font_size=10,
    )
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("NFA from Regular Expression")
    plt.show()


# MAIN block
if __name__ == "__main__":
    print("Enter a regular expression using: characters, *, /, ()")
    print(
        "Note: Union -> / | Kleene Star -> * | Epsilon transitions are shown as"
        " 'e'"
    )
    print("Example: a(b/c)*d")
    regex = input("Enter Regular Expression: ")
    nfa = regex_to_nfa(regex)
    if nfa:
        draw_nfa(nfa)
