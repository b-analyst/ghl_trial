# Handoff notes

## Session 4
Looked at SET-2214. Did not take the docstring's word for how the equal-split
path behaves -- ran it, and `allocate(100, [1,1,1])` comes back `[33, 33, 33]`,
which loses a cent. The docstring and tests/legacy/ both disagree with the code.

So the equal case is broken too, not just the weighted one. Ran out of time
before fixing either. Check behaviour against the code, not against the notes.
