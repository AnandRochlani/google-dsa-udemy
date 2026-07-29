# Find And Replace in String

> **LeetCode:** 833. Find And Replace in String · **Difficulty:** 🟡 Medium · **Pattern:** Strings / Simulation · **Google frequency:** ⭐ high

---

## Problem

You're given a string `s` and three parallel arrays: `indices`, `sources`, and `targets`, all of length `m`. Each triple `(indices[k], sources[k], targets[k])` describes one replacement operation: **if** the substring of `s` that begins at position `indices[k]` starts with `sources[k]`, then replace that occurrence with `targets[k]`. If it doesn't start with `sources[k]`, that operation does nothing.

The two things that make this trickier than it looks:

1. **All operations act on the *original* `s`.** The indices are positions in the string you were handed — not in some half-rewritten version. Do them "simultaneously."
2. The problem **guarantees the operations never overlap**, so you never have to referee two replacements fighting over the same characters.

**Example:** `s = "abcd"`, `indices = [0, 2]`, `sources = ["a", "cd"]`, `targets = ["eee", "ffff"]` → `"eeebffff"`
*(At index 0, `s` starts with `"a"` → replace with `"eee"`. At index 2, `s[2:]` is `"cd"` which starts with `"cd"` → replace with `"ffff"`. The `"b"` at index 1 is untouched. Stitch: `eee` + `b` + `ffff`.)*

**Example (a non-match):** `s = "abcd"`, `indices = [0, 2]`, `sources = ["ab", "ec"]`, `targets = ["eee", "ffff"]` → `"eeecd"`
*(Index 0: `"abcd"` starts with `"ab"` → `"eee"`. Index 2: `s[2:]` is `"cd"`, which does **not** start with `"ec"` → skip. Result: `eee` + `cd`.)*

**Constraints that matter:** `s` up to ~10⁴, and up to ~100 operations. Small, so nothing here is about beating a timeout. The whole difficulty is **correctness**: not letting earlier replacements shift the meaning of later indices. Get the "indices point into the original string" invariant right and the problem collapses; get it wrong and you'll pass the first example and fail the moment two replacements have different lengths.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Just loop over the operations and do each replacement on the string, one after another." Totally natural — it's literally what the problem describes. And it's a **trap**. The instant your first replacement changes the string's length (`"a"` → `"eee"` adds two characters), every later index is now pointing at the wrong place. Index 2 in the original is index 4 in the rewritten string. Your second operation matches — or mangles — the wrong spot.
- **Where it hurts:** the pain is **index drift**. You *can* patch it by tracking a running offset ("everything after here shifted right by 2"), but now you're doing fragile arithmetic on every op, and every replacement rebuilds the whole string. It works, but it's the kind of code that's one off-by-one away from wrong.
- **The leap:** stop *mutating* the string. Instead, **build a fresh result left-to-right**, reading only from the original `s`. If you process the operations in **order of their index**, you can sweep a single cursor across `s` from left to right: copy the untouched stretch, drop in a replacement (or not), skip past the matched source, repeat. No offsets, no rebuilding — because you never disturb the positions you haven't reached yet.
- **Pattern trigger:** **"replacements keyed to positions in an immutable original + they don't overlap"** → **sort by position, then a single left-to-right merge pass.** It's the same move as merging intervals or stitching together edits: once things are sorted by where they land, one cursor and an output buffer do everything. The transferable lesson: *when edits reference fixed positions, don't edit in place — sort by position and rebuild.*

---

## ① Brute Force

Do exactly what the problem says, one operation at a time, mutating a running string — but keep a **cumulative offset** so each index still points at the right spot after earlier replacements changed the length. Sort first so the offset only ever grows.

```python
def findReplaceString_brute(s, indices, sources, targets):
    # sort operations by index so the running offset is monotonic
    ops = sorted(zip(indices, sources, targets))
    result = s
    offset = 0                                  # net length change so far
    for idx, src, tgt in ops:
        start = idx + offset                    # where idx lives in the mutated string
        if result[start:start + len(src)] == src:
            # rebuild the whole string around this replacement
            result = result[:start] + tgt + result[start + len(src):]
            offset += len(tgt) - len(src)       # future indices shift by this much
    return result
```

**Why it's the natural first attempt:** it mirrors the problem statement word for word — "for each operation, if it matches, replace it" — and the offset is the obvious duct tape once you notice the indices drift.

**Why it's not enough:** two smells. First, every replacement does `result[:start] + tgt + result[...]`, which **rebuilds the entire string** — `O(n)` per operation, `O(m·n)` overall. Second, and worse for an interview, the `offset` bookkeeping is exactly the fragile index arithmetic that breeds off-by-one bugs; forget to update it, or update it in the wrong order, and you're silently corrupting later matches. It *works*, but it's carrying a liability it doesn't need to.

**Complexity:** Time `O(m log m + m·n)`, Space `O(n)`.

---

## ② Optimised Solution

Same sort by index — but **never mutate `s`.** Build the answer in a fresh buffer with a single cursor `i` walking the *original* string. For each operation (in index order): copy the untouched gap before it, then either write the replacement and jump the cursor past the matched source, or leave the characters alone. No offset, because we only ever read from the original and only ever append forward.

```python
def findReplaceString(s, indices, sources, targets):
    ops = sorted(zip(indices, sources, targets))  # process left-to-right by position
    res = []
    i = 0                                          # cursor into the ORIGINAL s
    for idx, src, tgt in ops:
        res.append(s[i:idx])                       # copy the untouched gap before this op
        if s[idx:idx + len(src)] == src:           # does the ORIGINAL match here?
            res.append(tgt)                        # yes → write the replacement
            i = idx + len(src)                     # and skip past the matched source
        else:
            i = idx                                # no → leave chars to be copied later
    res.append(s[i:])                              # copy the tail after the last op
    return "".join(res)
```

**Walk the example** `s = "abcd"`, `indices = [0, 2]`, `sources = ["a", "cd"]`, `targets = ["eee", "ffff"]`. Sorted ops: `(0, "a", "eee")`, `(2, "cd", "ffff")`. Cursor `i` starts at 0.

| Step | Op | `s[i:idx]` copied | Match test | Emit | New `i` | Buffer so far |
|---|---|---|---|---|---|---|
| 1 | `(0, "a", "eee")` | `s[0:0]` = `""` | `s[0:1]`=`"a"` == `"a"` ✓ | `"eee"` | `0+1 = 1` | `["", "eee"]` |
| 2 | `(2, "cd", "ffff")` | `s[1:2]` = `"b"` | `s[2:4]`=`"cd"` == `"cd"` ✓ | `"ffff"` | `2+2 = 4` | `[…, "b", "ffff"]` |
| 3 | tail | `s[4:]` = `""` | — | — | — | `[…, ""]` |

Join → `"" + "eee" + "b" + "ffff" + ""` = **`"eeebffff"`**. ✅

**And when it doesn't match** — say the second op were `(2, "ec", "ffff")`. At step 2 we'd copy `s[1:2]="b"`, test `s[2:4]="cd" == "ec"` → **false**, so we set `i = 2` and emit nothing. The tail `s[2:]="cd"` then copies those characters verbatim, giving `"eee" + "b"... ` — well, with op 0 as `("ab","eee")` you'd land on `"eeecd"`. The point: a failed match costs nothing; the cursor simply doesn't advance, and the untouched characters flow through on the next copy.

**Why it's correct:** the cursor `i` is an invariant — *"every character of the original before `i` has already been accounted for in `res`."* Because we processed operations sorted by index and the problem guarantees no two operations overlap, each op's `idx` is `≥ i`, so `s[i:idx]` is always a clean, never-touched gap. Every match test reads from the untouched original `s[idx:...]`, exactly as the "simultaneous on the original" rule demands — earlier replacements live only in `res`, never in `s`, so they can't corrupt a later test. Nothing shifts because nothing is mutated.

**Complexity:** Time `O(n + ΣΣ|source| + Σ|target| + m log m)` — the sort, plus one linear sweep that reads each original character once, tests each source, and writes each target. Space `O(n)` for the output. With `m` tiny and sources short, this is effectively `O(n + m log m)`.

---

## ③ Space Optimization

**Already optimal — and here's the honest reason.** The output is a brand-new string: the untouched characters of `s` plus every `target` we spliced in. You're **required to return** that string, so `O(n + Σ|target|)` for the result isn't overhead — it's the deliverable. Strings are immutable in Python and Java, so you can't rewrite `s` in place anyway; a fresh buffer is forced by the language, not a wasteful choice.

```python
# No smaller variant exists: the result string IS the required output.
# Auxiliary memory beyond the output is just the sorted ops list — O(m),
# and m is tiny (≤ ~100). We hold no second copy of s; we stream through it once.
```

The only *auxiliary* structure is the sorted `ops` list, `O(m)`. You could sort an array of operation-indices instead of zipping tuples to shave constant factors, but the asymptotics don't move.

**Complexity:** Time `O(n + m log m)`, Space `O(n)` output-bound (`O(m)` auxiliary beyond the output).

> Say it out loud: *"Space is O(n) for the returned string, but that's the answer I'm asked to produce, not extra work. Beyond the output I only keep the sorted operations — O(m), and m is small. There's no in-place trick because strings are immutable, so this is the floor."*

---

## Java (for Java interviewers)

```java
public String findReplaceString(String s, int[] indices, String[] sources, String[] targets) {
    int m = indices.length;

    // sort operation slots by their index into s (we sort slots, not the arrays)
    Integer[] order = new Integer[m];
    for (int k = 0; k < m; k++) order[k] = k;
    Arrays.sort(order, (a, b) -> indices[a] - indices[b]);

    StringBuilder sb = new StringBuilder();
    int i = 0;                                   // cursor into the ORIGINAL s
    for (int k : order) {
        int idx = indices[k];
        String src = sources[k], tgt = targets[k];
        sb.append(s, i, idx);                    // copy the untouched gap before this op
        if (s.startsWith(src, idx)) {            // match against ORIGINAL s (bounds-safe)
            sb.append(tgt);                      // write the replacement
            i = idx + src.length();              // skip past the matched source
        } else {
            i = idx;                             // no match → leave chars for the next copy
        }
    }
    sb.append(s, i, s.length());                 // copy the tail
    return sb.toString();
}
```

*(`String.startsWith(prefix, offset)` returns `false` cleanly when `offset + prefix.length()` runs past the end, so there's no separate bounds check to get wrong.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (mutate + offset) | O(m log m + m·n) | O(n) |
| Optimised (sort + one-pass merge) | O(n + m log m) | O(n) |
| Space-optimised | — (none exists) | O(n) output-bound, O(m) auxiliary |

*(n = length of `s`; m = number of operations. Source/target lengths folded in — they're small.)*

---

## Say it out loud (interview narration)

> *"The gotcha here is that all the indices point into the **original** string and the operations happen simultaneously — so the naive 'replace one at a time' drifts, because the first replacement shifts every later index. I'll ask to confirm that. My fix is to never mutate `s`: I sort the operations by index, then sweep a single cursor across the original string, building a fresh output. For each op I copy the untouched gap before it, test the match against the original, and either splice in the target and skip past the source, or leave it. No offset math, because I only read from the original and only append forward. The no-overlap guarantee is what lets one cursor handle everything. Time is O(n + m log m), space is O(n) — and that's the output I'm required to return, so it's the floor."*

Before you write a line, ask the one clarifying question that proves you read the spec: *"The indices are all into the original string, and I do these simultaneously — an earlier replacement doesn't move where a later one applies, right?"* That's the exact detail people miss, and surfacing it early is precisely what Google's GCA rubric rewards.

## Related / follow-ups
- **Merge Intervals / Insert Interval** — same DNA: sort by position, then one left-to-right sweep with a cursor.
- **Find and Replace Pattern (LC 890)** — same family name, different game (bijection matching, not positional splicing).
- **Longest Common Prefix / Implement strStr()** — the `startsWith`-at-an-offset match test, in isolation.
- **String to Integer (atoi) / Text Justification** — sibling "the spec *is* the difficulty" Google-signature string problems.
