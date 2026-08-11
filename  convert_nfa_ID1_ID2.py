import sys
from collections import defaultdict, deque

# ---------- Format DFA state ----------
def format_state(state):
    if len(state) == 0:
        return "{}"
    return "{" + ",".join(sorted(state)) + "}"

# ---------- Read NFA ----------
def read_nfa(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    states = lines[0].split(":")[1].split()
    alphabet = lines[1].split(":")[1].split()
    start = lines[2].split(":")[1].strip()
    finals = set(lines[3].split(":")[1].split())

    transitions = defaultdict(lambda: defaultdict(set))

    for line in lines[5:]:
        parts = line.split()
        src, symbol = parts[0], parts[1]

        if parts[2] != "-":
            for dest in parts[2:]:
                transitions[src][symbol].add(dest)

    return states, alphabet, start, finals, transitions

# ---------- Subset Construction (BFS order guaranteed) ----------
def nfa_to_dfa(states, alphabet, start, finals, transitions):
    start_state = frozenset([start])

    queue = deque([start_state])
    visited = []
    dfa_trans = {}

    while queue:
        current = queue.popleft()

        if current in visited:
            continue

        visited.append(current)
        dfa_trans[current] = {}

        for symbol in alphabet:
            next_state = set()

            for s in current:
                next_state |= transitions[s][symbol]

            next_state = frozenset(next_state)
            dfa_trans[current][symbol] = next_state

            if next_state not in visited and next_state not in queue:
                queue.append(next_state)

    # DFA final states
    dfa_finals = []
    for state in visited:
        if any(s in finals for s in state):
            dfa_finals.append(state)

    return visited, alphabet, start_state, dfa_finals, dfa_trans

# ---------- Write Output ----------
def write_output(filename, all_results, student_ids):
    with open(filename, 'w') as f:
        f.write(f"# Student IDs: {student_ids}\n\n")

        for idx, (states, alphabet, start, finals, trans) in enumerate(all_results):

            f.write("States: " + " ".join(format_state(s) for s in states) + "\n")
            f.write("Alphabet: " + " ".join(alphabet) + "\n")
            f.write("Start: " + format_state(start) + "\n")
            f.write("Final: " + " ".join(format_state(s) for s in finals) + "\n")
            f.write("Transitions:\n")

            for state in states:
                for symbol in alphabet:
                    f.write(f"{format_state(state)} {symbol} {format_state(trans[state][symbol])}\n")

            if idx != len(all_results) - 1:
                f.write("\n")  # separate DFAs

# ---------- Main ----------
def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_nfa_ID1_ID2.py input1.txt input2.txt")
        return

    # 🔥 CHANGE THIS
    student_ids = "1820232039"

    all_results = []

    for file in sys.argv[1:]:
        nfa = read_nfa(file)
        dfa = nfa_to_dfa(*nfa)
        all_results.append(dfa)

    write_output("output.txt", all_results, student_ids)

if __name__ == "__main__":
    main()