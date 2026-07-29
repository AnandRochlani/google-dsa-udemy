# Sentence Screen Fitting

> **LeetCode:** 418. Sentence Screen Fitting · **Difficulty:** 🟡 Medium · **Pattern:** Strings / Simulation · **Google frequency:** ⭐ high

---

## Problem

You're given a `sentence` as a list of words and a screen `rows` tall and `cols` wide. You lay the sentence onto the screen left-to-right, top-to-bottom, repeating it over and over. The rules: a word can **never** be split across a line, and consecutive words on the same line are separated by **exactly one space**. Count how many **complete** copies of the whole sentence fit on the screen.

**Example:** `sentence = ["a","bcd","e"]`, `rows = 3`, `cols = 6` → `2`

```
Row 0: "a bcd "     (a, bcd — 5 chars fit, e won't)
Row 1: "e a "       (e, a — then bcd won't fit)
Row 2: "bcd e "     (bcd, e)
```

Reading top-to-bottom you get `a bcd e | a bcd e` — the sentence laid down **twice**, so the answer is `2`.

**Constraints that matter:** `rows` and `cols` go up to `~20000`, and the sentence up to `~100` words. A per-cell simulation is `O(rows × cols)` — up to `4×10^8` character placements, right on the edge of a timeout. The target is to make the cost depend on `rows`, not `rows × cols`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** literally simulate it. Walk row by row; on each row keep placing the next word while it still fits, wrapping the word index back to 0 every time you finish the sentence. Count each wrap. This is correct and it's exactly how you'd do it by hand — but you touch roughly every cell of the screen.
- **Where it hurts:** the screen is enormous and mostly repetition. The same sentence tiles across it again and again. You're re-deciding "does the next word fit here?" for millions of positions, when the *pattern* of how the sentence wraps is short and repeats.
- **The leap:** stop thinking in words and start thinking in **one long ribbon of characters**. Build `s = " ".join(sentence) + " "` — the sentence with a trailing space so every word (including the last) is followed by a separator. Now imagine that ribbon repeated infinitely. Placing the sentence on the screen is just laying this ribbon across the rows. Keep a single pointer `start` into the infinite ribbon. Each row advances the pointer by `cols`. The only question per row is: **did that jump land in the middle of a word, and if so, how far do I back up** so the line ends on a clean word boundary?
- **Pattern trigger:** *"a repeating string tiled onto a fixed-width grid"* → **flatten to characters + modular pointer**. The trailing space is the trick that turns "does this word fit?" into "is the character under my pointer a space?" One character lookup replaces a whole fit-check loop.

---

## ① Brute Force

Simulate placement literally: for each row, greedily place words while they fit; wrap the word index and bump a counter each time the sentence completes.

```python
def words_typing_brute(sentence, rows, cols):
    n = len(sentence)
    lengths = [len(w) for w in sentence]
    count = 0          # completed sentences
    idx = 0            # index of the next word to place
    for _ in range(rows):
        remaining = cols
        # place words while the next one (plus its trailing space) fits
        while remaining >= lengths[idx]:
            remaining -= lengths[idx]   # lay the word down
            remaining -= 1              # one space after it
            idx += 1
            if idx == n:                # finished a full copy of the sentence
                count += 1
                idx = 0
    return count
```

**Why it's the natural first attempt:** it mirrors the physical act — fill a line word by word, start a new line, keep going, tally each time you've written the whole sentence.

**Why it's not enough:** the inner `while` can run once per *word* placed on a line, and across all rows that's proportional to the number of characters on the screen — `O(rows × cols)` in the worst case. With both up to `2×10^4`, that's hundreds of millions of steps. It's not *wrong*, it's *too slow* for the big cases, and it re-derives the same wrap pattern on every identical-looking row.

**Complexity:** Time `O(rows × cols)`, Space `O(1)` extra (beyond the word lengths).

---

## ② Optimised Solution

Flatten the sentence to a character ribbon `s = " ".join(sentence) + " "`, then slide **one** pointer through its infinite repetition. Each row advances the pointer by `cols`; a single character lookup tells you whether the line broke cleanly or landed mid-word, and if mid-word you back the pointer up to the previous space.

```python
def words_typing(sentence, rows, cols):
    s = " ".join(sentence) + " "   # trailing space: every word ends in a separator
    length = len(s)                # one full copy of the sentence, in characters
    start = 0                      # pointer into the INFINITE repetition of s
    for _ in range(rows):
        start += cols              # tentatively consume a full row's width
        if s[start % length] == " ":
            # landed exactly on a separator → the previous word ended cleanly.
            # skip that trailing space so the next row starts on a real word.
            start += 1
        else:
            # landed in the middle of a word → back up to the last space,
            # i.e. pull the whole partial word onto the next line instead.
            while start > 0 and s[(start - 1) % length] != " ":
                start -= 1
    return start // length         # each full `length` of ribbon = one sentence
```

**Walk the example** `sentence = ["a","bcd","e"]`, `rows = 3`, `cols = 6`. The ribbon is `s = "a bcd e "`, `length = 8`:

```
index:  0  1  2  3  4  5  6  7
char:   a  ' ' b  c  d  ' ' e  ' '
```

| Row | `start += cols` | `s[start % 8]` | Action | `start` after |
|---|---|---|---|---|
| 0 | `0 + 6 = 6` | `s[6] = 'e'` → not space | back up while prev ≠ space: `s[5]=' '` already, so stop | `6` |
| 1 | `6 + 6 = 12` | `s[12%8]=s[4]='d'` → not space | back up: `s[3]='c'`,`s[2]='b'`, then `s[1]=' '` stop | `10` |
| 2 | `10 + 6 = 16` | `s[16%8]=s[0]='a'` → not space | back up: `s[7]=' '` already, so stop | `16` |

Answer = `start // length = 16 // 8 = 2`. ✅ Trace what each row swallowed: row 0 covered indices 0–5 (`"a bcd"`), row 1 covered 6–9 (`"e a"`), row 2 covered 10–15 (`"bcd e"`) — exactly the two copies we drew by hand.

Second check — `sentence = ["hello","world"]`, `rows = 2`, `cols = 8`. Ribbon `"hello world "`, `length = 12`.
Row 0: `start = 8`, `s[8]='r'` mid-word → back up through `world` to the space at index 5 → `start = 6`. Row 1: `start = 6+8 = 14`, `s[14%12]=s[2]='l'` mid-word → back up through `world` (wrapping) to the space at index 11 → `start = 12`. Answer `12 // 12 = 1`. ✅

**Why it's correct:** `start` counts, exactly, how many characters of the infinite ribbon we've validly laid onto the screen so far. Advancing by `cols` claims a full line's width; the character *at* the pointer decides the boundary. If it's a space, the previous word ended precisely at the line edge — we just hop over that one separator so the next row begins on a fresh word. If it's a letter, we chopped a word in half, which is illegal, so we rewind to the most recent space — that pulls the entire partial word down to the next line, which is what "words can't split" means. The trailing space we appended guarantees even the sentence's *last* word is followed by a separator, so the "landed on a space" case fires correctly at copy boundaries. Since a completed copy is exactly `length` characters, `start // length` is the number of whole sentences placed.

**Complexity:** Time `O(rows)` amortised after an `O(C)` build of `s` (where `C` is the total characters in the sentence — the back-up loop across all rows rewinds at most one word's worth each time, bounded by the longest word). Space `O(C)` for the ribbon.

---

## ③ Space Optimization

**Already optimal for what the problem hands us.** The one real allocation is the ribbon `s`, which is `O(C)` where `C` is the total length of the sentence's characters — and you need those characters available to test boundaries, so there's no way to avoid holding them. Everything else is a fixed handful of integers (`start`, `length`, the loop counter): `O(1)`.

```python
# No smaller variant exists: `s` holds the sentence's characters once (O(C)),
# and the pointer arithmetic adds only O(1). Nothing scales with rows or cols
# in memory — that's the whole win over the per-cell simulation.
```

**Complexity:** Time `O(rows)` (+ `O(C)` build), Space `O(C)` for `s`, `O(1)` auxiliary beyond it.

> Say it out loud: *"Space is O(C) for the flattened sentence, and that's a floor, not overhead — I have to see the characters to know where words end. The pointer itself is O(1), and crucially nothing grows with the screen size."* That last clause is the point: the brute force's cost scaled with `rows × cols`; here memory is independent of the screen entirely.

---

## Java (for Java interviewers)

```java
public int wordsTyping(String[] sentence, int rows, int cols) {
    String s = String.join(" ", sentence) + " ";  // trailing space = clean separators
    int length = s.length();                       // one copy of the sentence, in chars
    int start = 0;                                 // pointer into infinite repetition of s
    for (int i = 0; i < rows; i++) {
        start += cols;                             // claim a full row's width
        if (s.charAt(start % length) == ' ') {
            // landed on a separator → previous word ended cleanly; skip the space
            start++;
        } else {
            // landed mid-word → rewind to the last space (pull the word to next line)
            while (start > 0 && s.charAt((start - 1) % length) != ' ') {
                start--;
            }
        }
    }
    return start / length;                         // whole copies of the sentence placed
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (per-cell simulation) | O(rows × cols) | O(1) |
| Optimised (flatten + modular pointer) | O(rows) (+ O(C) build) | O(C) |
| Space-optimised | — (none smaller exists) | O(C) for the ribbon, O(1) auxiliary |

*(C = total characters across all words + separators. The optimised memory is independent of `rows` and `cols`.)*

---

## Say it out loud (interview narration)

> *"My first idea is to simulate it directly — go row by row, place words while they fit, and count each time I complete the sentence. That's correct, but with rows and cols both up to twenty thousand it's O(rows × cols) and will time out. So the key move: I flatten the sentence into one string with a trailing space, `\" \".join(words) + \" \"`, and treat it as an infinite ribbon. I keep a single pointer and, for each row, jump it forward by cols. If the character I land on is a space, the last word ended cleanly and I step over that one space. If it's a letter, I split a word, so I back up to the previous space to pull that whole word to the next line. After all the rows, the pointer divided by the ribbon length is the number of complete sentences. That's O(rows) time and O(C) space, and the memory doesn't depend on the screen size at all."*

Before coding, ask the one clarifying question that shows you read the spec: *"Exactly one space between words, and a word can never be split across a line — right?"* Confirming the split rule up front is exactly the General Cognitive Ability signal Google rewards.

## Related / follow-ups
- **Rearrange Spaces Between Words (LC 1592)** — same "join words with spaces, do the arithmetic" muscle, on distributing spaces evenly.
- **Text Justification (LC 68)** — the heavier cousin: fixed-width lines with greedy packing plus a per-line rendering rule.
- **String Compression / Repeated String patterns** — reasoning about an infinitely-tiled string via modular indexing.
- **Robot Bounded In Circle** — another "simulate, but spot the short repeating cycle instead of iterating forever" problem.
