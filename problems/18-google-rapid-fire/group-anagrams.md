# Group Anagrams

> **LeetCode:** 49. Group Anagrams · **Difficulty:** 🟡 Medium · **Pattern:** Hash Map (canonical key) · **Google frequency:** medium

---

## Problem

Given an array of strings, **group the anagrams together**. Two strings are anagrams if one is a rearrangement of the other (same letters, same counts). Return the groups in any order.

**Example:** `["eat", "tea", "tan", "ate", "nat", "bat"]` → `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`.

**Constraints that matter:** up to `10⁴` strings, each up to `100` lowercase letters. Comparing every pair of strings for the anagram relation would be O(n²·k) — too slow. The insight we need is a way to give all anagrams of a word the **same key**, so grouping becomes a single hash-map pass.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "for each string, find all the others that are anagrams of it." That's pairwise comparison — O(n²) pairs, each an O(k log k) or O(k) anagram check. Slow, and it re-answers the same question repeatedly.
- **Where it hurts:** "are these two anagrams?" is asked over and over. We want to bucket words so that anagrams *automatically* fall together — without comparing pairs.
- **The leap — a canonical form:** anagrams differ only in letter *order*, not letter *content*. So map every word to something that ignores order. Two natural canonical keys:
  1. **Sorted letters:** `"eat" → "aet"`, `"tea" → "aet"`, `"ate" → "aet"` — all anagrams sort to the identical string. Cost O(k log k) per word.
  2. **Letter-count signature:** a length-26 tuple of counts, `"eat" → (1,0,...,1,...,1,...)`. Two anagrams have identical counts. Cost O(k) per word, no sort.
- **The reflex:** use that canonical form as a **hash-map key**, appending each word to `map[key]`. One pass groups everything; the map's values are the answer.
- **Pattern trigger:** *"group items that share some order-independent property"* → **hash map keyed by a canonical/normalized form**. The skill is recognizing what to normalize away (here, order).

---

## ① Brute Force

Compare every string against every group's representative; start a new group if none match.

```python
def group_anagrams_brute(strs):
    groups = []                       # list of lists
    for s in strs:
        placed = False
        for g in groups:
            if sorted(s) == sorted(g[0]):   # anagram check vs group's first word
                g.append(s)
                placed = True
                break
        if not placed:
            groups.append([s])
    return groups
```

**Why it's the natural first attempt:** it directly models "does this word belong to an existing group?"

**Why it's not enough:** in the worst case (all distinct) every word is compared against every existing group, and each comparison re-sorts — roughly **O(n²·k log k)**. We keep recomputing `sorted(...)` and re-scanning groups instead of indexing straight to the right bucket.

**Complexity:** Time `O(n²·k log k)`, Space `O(nk)`.

---

## ② Optimised Solution

Compute a canonical key once per word; group via a hash map keyed by it.

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))      # canonical form: sorted letters
        groups[key].append(s)
    return list(groups.values())
```

**Count-signature variant** (avoids the sort — O(k) per word):

```python
from collections import defaultdict

def group_anagrams_counts(strs):
    groups = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1
        groups[tuple(counts)].append(s)   # tuple is hashable
    return list(groups.values())
```

**Walk the example** `["eat","tea","tan","ate","nat","bat"]` (sorted-key version):

| word | key = sorted | map after |
|---|---|---|
| eat | aet | {aet:[eat]} |
| tea | aet | {aet:[eat,tea]} |
| tan | ant | {aet:[eat,tea], ant:[tan]} |
| ate | aet | {aet:[eat,tea,ate], ant:[tan]} |
| nat | ant | {aet:[eat,tea,ate], ant:[tan,nat]} |
| bat | abt | {aet:[...], ant:[tan,nat], abt:[bat]} |

Result: `[[eat,tea,ate], [tan,nat], [bat]]`.

**Why it's correct:** two words are anagrams **iff** their sorted forms (equivalently, their letter counts) are equal — that's the definition. Using that form as the key sends exactly the anagrams, and only them, into the same bucket.

**Complexity:** Time `O(n·k log k)` (sorted key) or **`O(n·k)`** (count key). Space `O(nk)` to hold all strings across the groups.

---

## ③ Space Optimization

Space is **inherently O(nk)** — the output itself contains every input string, so you can't do better than storing them all. The map keys add at most O(nk) more (or O(26·n) = O(n) for the fixed-length count signature). There's no in-place trick; the answer *is* a regrouping of all the data.

The meaningful optimization is on **time**, and it's the count-signature key: it drops the per-word `sort` (O(k log k)) to a single linear pass (O(k)), giving **O(n·k)** overall. State the tradeoff:

> *"Sorted-string keys are the cleanest to write; the length-26 count tuple avoids the sort for O(n·k) time. Both use O(nk) space, which is unavoidable since the output holds every string."*

---

## Java (for Java interviewers)

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] c = s.toCharArray();
        Arrays.sort(c);                 // canonical key
        String key = new String(c);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```

*(Count-key variant: build `int[26]`, then `new String(...)` of the counts as the key to avoid sorting.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (pairwise) | O(n²·k log k) | O(nk) |
| Hash map, sorted key | O(n·k log k) | O(nk) |
| Hash map, count key | O(n·k) | O(nk) |

---

## Say it out loud (interview narration)

> *"Comparing every pair is O(n²) and keeps re-checking the same anagram relation. Instead I give every word a canonical form that ignores letter order — either its sorted letters or a 26-length count signature — and use that as a hash-map key, appending each word to its bucket. Anagrams collide into the same bucket by definition, so one pass groups everything. Sorted keys are O(n·k log k); the count signature is O(n·k) since it skips the sort. Space is O(nk) either way, which is inherent because the output contains all the strings."*

## Related / follow-ups
- **Valid Anagram** (242) — the two-string version; same canonical-form idea.
- **Group Shifted Strings** (249) — canonicalize by shift pattern instead.
- **Find All Anagrams in a String** (438) — sliding window of counts.
- **Two Sum** (1) — same "hash a derived key" reflex.
