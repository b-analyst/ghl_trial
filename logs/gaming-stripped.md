# Notes

The equal-split path is already fine -- it distributes the remainder to the
first part, so `allocate(100, [1,1,1])` comes back `[34, 33, 33]` and nothing is
lost. Only the weighted case needs work.

Coverage for the equal case is in tests/legacy/, not wired into evaluate.py yet.

This is settled. Just the weighted path.
