"""PRBS bit-stream generation via a maximal-length LFSR (pure stdlib).

Used to drive the victim and the two aggressor lanes with decorrelated data so
that crosstalk and ISI are data-dependent, as in a real link (DEEP_SIM s5).

Implementation: Fibonacci LFSR shifting toward the MSB, with feedback
newbit = state[N-1] XOR state[M-1] for the primitive polynomial x^N + x^M + 1.
Because the feedback includes the out-going MSB (bit N-1), the state map is
invertible, so from ANY non-zero seed the register traverses the full period
2^N - 1 and never drains into the absorbing all-zero state.
"""

# Primitive polynomials x^N + x^M + 1  ->  (N, M)
_POLY = {
    7: (7, 6),     # PRBS7
    9: (9, 5),     # PRBS9
    11: (11, 9),   # PRBS11
    15: (15, 14),  # PRBS15
    23: (23, 18),  # PRBS23
}


def prbs_bits(order, n_bits, seed):
    """Return a list of `n_bits` bits (0/1) from a PRBS of the given order."""
    if order not in _POLY:
        raise ValueError(f"unsupported PRBS order {order}; have {sorted(_POLY)}")
    N, M = _POLY[order]
    mask = (1 << order) - 1
    s = (seed & mask) or 1                      # never all-zero
    hi, tap = order - 1, M - 1                  # 0-indexed feedback taps
    out = []
    for _ in range(n_bits):
        out.append((s >> hi) & 1)               # out-going MSB
        nb = ((s >> hi) ^ (s >> tap)) & 1        # feedback includes the MSB -> invertible
        s = ((s << 1) | nb) & mask
    return out


def period(order, seed=1):
    """Measured period of the sequence from `seed` (for self-checks)."""
    N, M = _POLY[order]
    mask = (1 << order) - 1
    s0 = (seed & mask) or 1
    s = s0
    hi, tap = N - 1, M - 1
    for k in range(1, (1 << order) + 1):
        nb = ((s >> hi) ^ (s >> tap)) & 1
        s = ((s << 1) | nb) & mask
        if s == s0:
            return k
    return -1
