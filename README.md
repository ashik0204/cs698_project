# Neighborhood Stability in Assignments on Graphs — CS698I paper study

Presentation and report on the paper
**[Neighborhood Stability in Assignments on Graphs](https://arxiv.org/abs/2407.05240)**
by Haris Aziz, Grzegorz Lisowski, Mashbat Suzuki and Jeremy Vollen (2024).

Course: CS698I, Relational Structures in Games, IIT Kanpur (instructor: Sunil Simon).
Authors: Ashik Stenny (230224) and Achyuth H Warrier (230052).

## The paper in one paragraph

Agents are seated on the vertices of a graph. Each agent approves some others, and its utility is the number of approved neighbours. An assignment is *neighbourhood stable* if no two adjacent agents would both gain by swapping seats. The paper shows that such assignments can fail to exist (on complete bipartite seat graphs), that letting agents swap can cycle forever even on a 4-cycle, but that a neighbourhood stable assignment always exists, and can be computed in polynomial time, on cycles and paths. It also gives a sufficient condition for general seat graphs based on leaves and directed feedback vertex sets.

## Contents

| Folder | What it contains |
|---|---|
| [`slides/`](slides) | Beamer slides for the 35-minute talk ([`slides.pdf`](slides/slides.pdf)), speaker notes with timings ([`notes.pdf`](slides/notes.pdf)), and the LaTeX source. |
| [`report/`](report) | The written report ([`report.pdf`](report/report.pdf)) and its LaTeX source. |
| [`verification/`](verification) | Python scripts that check the examples and claims used in the slides and report. |

The report explains every result of the paper with a single running example, connects it to course topics (potential games and the finite improvement property, PLS, colouring games on DAGs, hedonic games), and adds our own observations, marked **[ours]** in the text:

- an exact characterisation of envy in the paper's counterexample (Theorem 1),
- a tighter `O(n^2)` running time for the path algorithm (Theorem 3),
- a five-agent instance showing why distance-2 stability fails on cycles,
- two boundary cases (exactly one or two paths) not covered by the written proof of the main lemma for cycles, with patches checked computationally.

## Building

Requires a LaTeX installation with `beamer` and `tikz`.

```sh
./slides/build.sh     # produces slides/slides.pdf and slides/notes.pdf
./report/build.sh     # produces report/report.pdf
```

## Running the checks

Python 3, standard library only.

```sh
python3 verification/examples.py     # exhaustive checks of all small examples
python3 verification/algorithm1.py   # Algorithm 1 (cycles) with patches, 60,000 random instances
```

`examples.py` checks the running example, the swap cycle of Proposition 1, the `K(3,3)` counterexample, the two-triangle example, every preference graph on four agents, the path algorithm on random instances, and the examples discussed in the report. `algorithm1.py` implements the cycle algorithm as written in the paper, asserts the properties used in its proof at every step, and reports how often each repair case occurs.
