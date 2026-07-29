# Number of Matching Subsequences

> **LeetCode:** 792. Number of Matching Subsequences · **Difficulty:** 🟡 Medium · **Pattern:** Bucketing / Multiple Pointers · **Google frequency:** ⭐ high

---

## Problem

You're given one string `s` and an array `words`. Return **how many** of the words are **subsequences** of `s`. A subsequence keeps the original left-to-right order but is allowed to skip characters — so `"ace"` is a subsequence of `"abcde"`, but `"aec"` is not (the `c` comes before the `e` in `s`).

**Example:** `s = "abcde"`, `words = ["a","bb","acd","ace"]` → `3`
*( `"a"` ✓, `"bb"` ✗ (only one `b` in `s`), `"acd"` ✓ (a·c·d), `"ace"` ✓ (a·c·e) )*

**Constraints that matter:** `s` can be up to `5·10⁴` characters, and `words` can hold up to `5·10³` entries with total length up to `5·10⁴`. The trap is the *combination*: checking each word independently against `s` is `O(|words| · |s|)`, which is `5000 · 50000 = 2.5·10⁸` in the worst case — right on the edge of a Time Limit Exceeded. The whole game is doing **one pass over `s`** and letting every word ride along on that single pass.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "A subsequence check is easy — two pointers. Walk `s`, walk the word, advance the word pointer on a match. If the word pointer reaches the end, it matched." Totally correct for *one* word. So just loop that over all the words. That's the brute force, and it's the right starting point to say out loud.
- **Where it hurts:** you re-scan `s` from the top for **every single word**. Word #1 walks all of `s`. Word #2 walks all of `s` again. Word #5000 walks all of `s` yet again. `s` is the big expensive thing, and you're traversing it thousands of times. The words themselves are short — the waste is entirely in re-reading `s`.
- **The leap:** flip the loop inside out. Instead of *"for each word, scan `s`,"* do *"scan `s` once, and let every word wait for the character it needs next."* At any moment a word only cares about **one** character — its next unmatched one. So park each word in a bucket keyed by that character. When we reach character `c` while walking `s`, wake up **everyone** waiting on `c`, advance them by one, and re-park them on their *new* next character. One sweep of `s` feeds all the words.
- **Pattern trigger:** **"many small patterns, all matched against one big sequence, each caring about only its next character"** → **bucket by next-needed character + a single pass**. The transferable move is *invert the loop and index by what each item is waiting for*. The same shape shows up whenever you'd otherwise re-scan one long stream once per query.

---

## ① Brute Force

For each word, run a two-pointer subsequence check against `s` from the start.

```python
def num_matching_subseq_brute(s, words):
    def is_subseq(w):
        it = iter(s)                    # fresh scan of s for THIS word
        # every char of w must appear, in order, somewhere ahead in s
        return all(ch in it for ch in w)  # `ch in it` advances the iterator

    return sum(is_subseq(w) for w in words)
```

**Why it's the natural first attempt:** the subsequence check is a textbook two-pointer, and `all(ch in it for ch in w)` is the slick Python idiom for it — the iterator `it` keeps its position across the `in` checks, so it never rewinds *within* one word. It's clean and obviously correct.

**Why it's not enough:** the iterator is *fresh for every word*. Each word pays a full walk of `s`. With `|words|` up to 5000 and `|s|` up to 50000, that's `O(|words| · |s|)` ≈ `2.5·10⁸` character comparisons — the classic "passes the samples, times out on the big hidden test" outcome. `s` is scanned thousands of times when once would do.

**Complexity:** Time `O(|words| · |s|)`, Space `O(1)` extra.

---

## ② Optimised Solution

**Bucket the words by the character they're waiting on, then sweep `s` exactly once.** Key insight: a word only ever cares about its *next* unmatched character. Keep a dictionary `waiting` from a character → the list of `(word, next_index)` pairs currently blocked on that character. Seed it by parking every word on its **first** character. Now walk `s`; when you hit character `c`, grab **everyone** waiting on `c`, advance each by one, and either count it (fully matched) or re-park it on its new next character.

```python
from collections import defaultdict

def num_matching_subseq(s, words):
    # waiting[c] = list of (word, index) blocked on character c next
    waiting = defaultdict(list)
    for w in words:
        waiting[w[0]].append((w, 0))     # park each word on its first char

    matched = 0
    for c in s:                          # ONE pass over s
        # take everyone waiting on c and clear the bucket first...
        blocked = waiting[c]
        waiting[c] = []                  # ...so re-parked words aren't re-seen this step
        for w, i in blocked:
            i += 1                        # c matched this word's char at index i
            if i == len(w):
                matched += 1              # ran off the end → full subsequence
            else:
                waiting[w[i]].append((w, i))  # re-park on the NEXT needed char
    return matched
```

**Walk the example** `s = "abcde"`, `words = ["a","bb","acd","ace"]`:

Seed the buckets on each word's first char:
- `waiting['a'] = [("a",0), ("acd",0), ("ace",0)]`
- `waiting['b'] = [("bb",0)]`

| Read `c` | Bucket taken (`waiting[c]`) | Advance each | Result / re-park |
|---|---|---|---|
| `a` | `("a",0), ("acd",0), ("ace",0)` | →1, →1, →1 | `"a"` hits end → **matched=1**; `"acd"`→ `waiting['c']`; `"ace"`→ `waiting['c']` |
| `b` | `("bb",0)` | →1 | `"bb"` → `waiting['b']` (still needs another `b`) |
| `c` | `("acd",1), ("ace",1)` | →2, →2 | `"acd"` → `waiting['d']`; `"ace"` → `waiting['e']` |
| `d` | `("acd",2)` | →3 | `"acd"` hits end → **matched=2** |
| `e` | `("ace",2)` | →3 | `"ace"` hits end → **matched=3** |

`"bb"` is still stranded in `waiting['b']` at the end — there was never a second `b` — so it's never counted. Final answer: **3**. ✅

**Why it's correct:** the invariant is *"a word sits in `waiting[c]` exactly when `c` is the next character it needs."* Seeding puts every word on its first char, so the invariant holds before the sweep. Each time we read a `c` from `s`, we advance precisely the words whose next need is `c`, and re-park each on its brand-new next need — restoring the invariant. Because we **clear the bucket before re-adding**, a word that advances from `c` to some later `c` isn't matched twice against the *same* position of `s`. And because we honor `s`'s left-to-right order, a word only advances on characters that appear *after* the ones it already matched — which is exactly the subsequence rule. A word reaches `i == len(w)` iff all its characters were found in order.

**Complexity:** Time `O(|s| + Σ|words|)` — each character of `s` is read once, and each character across all words is processed exactly once (a word is touched only when its single waited-on char shows up). Space `O(Σ|words|)` for the pairs held in the buckets.

---

## ③ Space Optimization

**Store an index, not a copy of the word — and even that is already tight.** The buckets hold one `(word, index)` pair per *live* word, so at any instant the extra memory is `O(number of words)` references plus the seed pass, i.e. `O(Σ|words|)` in the honest worst case where the words themselves are the input you must hold anyway. We are *not* copying substrings on each re-park — we keep the same word object and just bump an integer index, so re-bucketing is `O(1)` per move with no string slicing.

```python
# Micro-optimisation: iterate s's characters directly and index into the word.
# Storing (word, i) — an object reference + an int — avoids ever slicing w[i:],
# which would turn each re-park into an O(len(w)) copy and blow up both time and space.
# The buckets never hold more than one entry per word, so auxiliary space is O(#words).
```

**Complexity:** Time `O(|s| + Σ|words|)`, Space `O(Σ|words|)` for the parked pairs.

> Say so out loud: *"Space is bounded by the words themselves — one small `(word, index)` pair in flight per word, never a substring copy. I can't beat `O(total word length)` because I have to remember where every unfinished word is up to. That's the floor, not overhead."* Some solutions instead binary-search each word's characters against precomputed **index lists** of `s` (a `char → sorted positions` map) — same time class, `O(|s|)` extra for the position map. Worth naming as an alternative; it shines when `words` is *streaming* and `s` is fixed.

---

## Java (for Java interviewers)

```java
public int numMatchingSubseq(String s, String[] words) {
    // waiting[c] holds int[]{wordIndex, charIndex} pairs blocked on char c
    List<Deque<int[]>> waiting = new ArrayList<>(26);
    for (int c = 0; c < 26; c++) waiting.add(new ArrayDeque<>());

    for (int w = 0; w < words.length; w++) {
        waiting.get(words[w].charAt(0) - 'a').add(new int[]{w, 0});  // park on first char
    }

    int matched = 0;
    for (char c : s.toCharArray()) {
        Deque<int[]> bucket = waiting.get(c - 'a');
        int size = bucket.size();               // snapshot: only entries present now
        for (int k = 0; k < size; k++) {        // re-parked words land at the tail, skipped this round
            int[] pair = bucket.poll();
            String w = words[pair[0]];
            int i = pair[1] + 1;                 // c matched this word's char
            if (i == w.length()) {
                matched++;                       // full subsequence
            } else {
                waiting.get(w.charAt(i) - 'a').add(new int[]{pair[0], i});  // re-park on next char
            }
        }
    }
    return matched;
}
```

*(The `size` snapshot plays the same role as clearing the Python bucket: we only process the entries that were waiting on `c` when this step began, so a word that re-parks onto a later `c` isn't advanced twice against one position of `s`. Buckets are `char → 0..25` since inputs are lowercase letters.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (scan `s` per word) | O(\|words\| · \|s\|) | O(1) |
| Optimised (buckets, one pass) | O(\|s\| + Σ\|words\|) | O(Σ\|words\|) |
| Space-optimised (index, no slicing) | O(\|s\| + Σ\|words\|) | O(Σ\|words\|) — the floor |

*(Σ\|words\| = total characters across all words. The buckets hold at most one live pair per word.)*

---

## Say it out loud (interview narration)

> *"The easy version is a two-pointer subsequence check per word — correct, but it re-scans `s` once per word, so it's O(words × |s|), and with both up to tens of thousands that times out. The waste is obvious: `s` is the expensive thing and I'm reading it thousands of times. So I invert the loop. I scan `s` exactly once. Each word only ever waits on one character — its next unmatched one — so I bucket every word by that character. When I read a character `c` from `s`, I wake everyone waiting on `c`, advance each by one, and re-park them on their new next character; if a word runs off its end, it matched. I clear the bucket before re-adding so nothing double-counts on the same position. That's O(|s| + total word length) time, O(total word length) space. And I'd store an index, not a substring copy, so re-parking stays O(1)."*

Before coding, ask the one clarifying question that shows you read the constraints: *"How many words, and how long is `s`? If words is large, per-word scanning of `s` will blow up — I'll bucket instead."* Naming *why* you're choosing the harder solution is exactly the General Cognitive Ability signal Google's rubric rewards.

## Related / follow-ups
- **Is Subsequence (LC 392)** — the single-word core; the follow-up ("many words / streaming queries against a fixed `s`") is literally this problem.
- **Shortest Way to Form String (LC 1055)** — greedy subsequence matching with a twist (how many copies of `s` needed).
- **Longest Word in Dictionary through Deleting (LC 524)** — subsequence checks over a word list, plus a tiebreak.
- **Group Anagrams (LC 49)** — same "bucket items by a key, then process" muscle, different key.
