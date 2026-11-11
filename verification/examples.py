"""Brute-force checks of the small examples used in the report (run: python3 examples.py)."""
import itertools, random
def util(L, i, seat, adj):
    k = seat.index(i); return sum(L[i][seat[v]] for v in adj[k])
def blocking(L, seat, adj, adjacent_only=True, within=None):
    """Blocking pairs; adjacent_only: only neighbouring seats; within: only seats at index distance <= within."""
    out = []
    for a, b in itertools.combinations(range(len(seat)), 2):
        ia, ib = seat.index(a), seat.index(b)
        if adjacent_only and ib not in adj[ia]: continue
        if within is not None and abs(ia - ib) > within: continue
        sw = seat[:]; sw[ia], sw[ib] = b, a
        if util(L, a, sw, adj) > util(L, a, seat, adj) and util(L, b, sw, adj) > util(L, b, seat, adj):
            out.append((a, b))
    return out
def cyc(n): return {k: [(k-1) % n, (k+1) % n] for k in range(n)}
def path(n): return {k: [x for x in (k-1, k+1) if 0 <= x < n] for k in range(n)}
def prefs(names, arcs):
    idx = {c: i for i, c in enumerate(names)}; L = [[0]*len(names) for _ in names]
    for a in arcs.split(): L[idx[a[0]]][idx[a[2]]] = 1
    return L, idx
def seat_of(s, idx): return [idx[c] for c in s]
def nm(pairs, names="abcd"): return ["".join(names[x] for x in p) for p in pairs]

# Fig. 2 running example: a<->c, b<->d, b->a, d->c
L, I = prefs("abcd", "a>c c>a b>d d>b b>a d>c")
print("Fig2 a-d-b-c on path: adjacent blocking pairs", nm(blocking(L, seat_of("adbc", I), path(4))))
print("Fig2 a-b-d-c on path: any blocking pair", blocking(L, seat_of("abdc", I), path(4), False))
print("Fig2 Case-1 greedy b,a,c,d on C4: blocking", blocking(L, seat_of("bacd", I), cyc(4)))
print("Fig2 greedy/Thm4 a,c,d,b on path: any blocking", blocking(L, seat_of("acdb", I), path(4), False))
print("Fig2 wrong sink seat a,d,c,b on path: adjacent blocking", nm(blocking(L, seat_of("adcb", I), path(4))))
# Fig. 6: c->a, a->b, a->d, b->d, d->c
L6, I6 = prefs("abcd", "c>a a>b a>d b>d d>c")
seat = seat_of("abcd", I6)
for step in range(4):
    bp = blocking(L6, seat, cyc(4)); print("Fig6 step", step, "".join("abcd"[x] for x in seat), "blocking pairs:", ["".join("abcd"[x] for x in p) for p in bp])
    a, b = bp[0]; ia, ib = seat.index(a), seat.index(b); seat[ia], seat[ib] = b, a
print("Fig6 back to start:", "".join("abcd"[x] for x in seat))
print("Fig6 #NS seatings on C4:", sum(1 for p in itertools.permutations(range(4)) if not blocking(L6, list(p), cyc(4))), "of 24")
print("Fig6 partition {a->d->c},{b} seated a,d,c,b: blocking", nm(blocking(L6, seat_of("adcb", I6), cyc(4))))
# K(3,3)
ag = ["11", "12", "13", "21", "22", "23"]; arcs = []
for j in range(1, 4):
    arcs += [f"1{j}>2{j}", f"2{j}>1{j}", f"1{j}>1{j%3+1}", f"2{j}>2{j%3+1}"]
LK = [[0]*6 for _ in range(6)]
for a in arcs: x, y = a.split(">"); LK[ag.index(x)][ag.index(y)] = 1
k33 = {s: [t for t in range(6) if (s < 3) != (t < 3)] for s in range(6)}
print("K33: NS seatings among 720:", sum(1 for p in itertools.permutations(range(6)) if not blocking(LK, list(p), k33)))
# Example 2: two triangles, directed 6-cycle
L2 = [[int(j == (i+1) % 6) for j in range(6)] for i in range(6)]
tri = {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4, 5], 4: [3, 5], 5: [3, 4]}
P = [list(p) for p in itertools.permutations(range(6))]
print("Example 2: all NS:", all(not blocking(L2, p, tri) for p in P), " any stable:", any(not blocking(L2, p, tri, False) for p in P))
# +-1 values on a path of three seats (friendship graph a directed 3-cycle)
V = [[0 if i == j else (1 if j == (i+1) % 3 else -1) for j in range(3)] for i in range(3)]
print("+-1 on 3-seat path: NS seatings:", sum(1 for p in itertools.permutations(range(3)) if not blocking(V, list(p), path(3))))
# Theorem 2 existence: every digraph on 4 agents, seat graph C4
pairs = [(i, j) for i in range(4) for j in range(4) if i != j]; bad = 0
for mask in range(1 << 12):
    L4 = [[0]*4 for _ in range(4)]
    for b, (i, j) in enumerate(pairs):
        if mask >> b & 1: L4[i][j] = 1
    if not any(not blocking(L4, list(p), cyc(4)) for p in itertools.permutations(range(4))): bad += 1
print("All 4096 digraphs on 4 agents: instances with no NS seating on C4:", bad)
# Theorem 3 greedy on paths: no blocking pair within distance 2
random.seed(1); fails = 0
for _ in range(20000):
    n = random.randint(3, 8); q = random.random()
    Lr = [[0 if i == j else int(random.random() < q) for j in range(n)] for i in range(n)]
    rem = list(range(n)); random.shuffle(rem); order = [rem.pop()]
    while rem:
        Q = [l for l in rem if Lr[l][order[-1]]]; x = random.choice(Q) if Q else random.choice(rem); rem.remove(x); order.append(x)
    if blocking(Lr, order, path(n), adjacent_only=False, within=2): fails += 1
print("Theorem 3 greedy: failures in 20000 random runs:", fails)
# 5 agents on a 5-cycle: no stable seating (distance <= 2 covers all pairs on C5)
L5, I5 = prefs("abcde", "a>c a>e b>a b>e c>a c>d d>b d>c e>b e>d")
seats = [[0]+list(p) for p in itertools.permutations(range(1, 5))]
print("5-agent instance: stable seatings on C5:", sum(1 for s in seats if not blocking(L5, s, cyc(5), False)),
      " NS seatings (of 24 with a fixed):", sum(1 for s in seats if not blocking(L5, s, cyc(5))))
# single-path gap instance: a->b, a->c, b->c, b->d, c->d, d->a
LG, IG = prefs("abcd", "a>b a>c b>c b>d c>d d>a")
print("Single-path instance b,d,a,c: blocking", ["".join("abcd"[x] for x in p) for p in blocking(LG, seat_of("bdac", IG), cyc(4))],
      "; repaired b,c,d,a: blocking", blocking(LG, seat_of("bcda", IG), cyc(4)))
