from typing import Any

BIG_NUMBER = 100_000


def ifnone(a: Any, b: Any) -> Any:
    """`a` if `a` is not None, otherwise `b`."""
    return b if a is None else a


def levenshtein(s: str, t: str, ignore_case=False) -> int:
    """ Implementation of classic Levenshtein edit distance. """
    if s is None or t is None:
        return BIG_NUMBER
    if ignore_case:
        s = s.lower()
        t = t.lower()
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)
    v0 = list(range(len(t) + 1))
    v1 = v0.copy()
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return v1[len(t)]
