# Quiet Proof

## What counts when nothing happened?

Public systems often need to prove a negative: no recall was posted, no closure appeared, or no required notice entered the record. A missing keyword on one page is not proof. Quiet Proof freezes the exact signal definition, the observation time, and two to five independently hosted source slots before anyone looks.

## Observation rule

After `not_before`, any wallet may trigger the observation. Every source is fetched inside nondeterministic execution and bound to its slot by a SHA-256 digest. Validators independently inspect the same bodies and every proposed label. The stored result is deliberately small:

- `PRESENT` if any source explicitly carries the signal.
- `ABSENT` only if every readable source covers the subject and lacks the signal.
- `INCONCLUSIVE` if even one source is semantically ambiguous and none proves presence.

This is not a generic truth vote. Its reusable primitive is multi-source negative evidence with an asymmetric decision rule: one positive defeats absence, while absence requires complete coverage.

## Lifecycle and failure map

`WAITING -> PRESENT | ABSENT | INCONCLUSIVE`

The owner may cancel only before observation. Duplicate identifiers, repeated hostnames, malformed HTTPS paths, early observation, unreadable sources, malformed labels, altered digests, and replay are rejected. Source failures stay explicit instead of being counted as absence.

## Review bench

```text
genvm-lint contracts/contract.py
python -m pytest -q
```

The direct suite covers all-absent, one-present, ambiguous, duplicate-origin, early-call, forged-label, forged-digest, authorization, cancellation, and duplicate-ID paths.

