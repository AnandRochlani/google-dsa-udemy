# 🎬 Recording Script — Accounts Merge
**Pattern: Tries & Union-Find · LeetCode 721 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the reusable `UnionFind` class from Number of Provinces & Redundant Connection. The new idea: choosing *what* the nodes are.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a messy list of user accounts, all named "John", some sharing an email. Lines connect the ones that share; they collapse into distinct person-cards.]**

> Real-world data problem, and a classic Google interview: you've got user accounts, each with a name and some emails. Two accounts are the **same person** if they share *any* email. Names lie — lots of people are named "John" — so you can only trust the emails. Merge everything and list each real person once.
>
> The catch is *transitivity*: if account A shares an email with B, and B with C, then all three are one person — even if A and C share nothing directly. Chase that with pairwise comparisons and you get a horrible re-merging loop.
>
> By the end you'll solve it cleanly with Union-Find — and the whole trick is one non-obvious choice: *what do we make the nodes?* Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, four accounts listed with their emails; the two Johns sharing `johnsmith` highlighted.]**

> One line: **merge accounts that share any email into one person, then output each person's name and their sorted, de-duplicated emails.**
>
> Tiny example:

```
["John", johnsmith, john_newyork]
["John", johnsmith, john00]
["Mary", mary]
["John", johnnybravo]
```

> The first two Johns both have `johnsmith` — same person, merge them. The third John and Mary share nothing — they stay separate. So three people come out: one merged John (three emails), Mary, and the lone John. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:35`
*(worked example — let them feel the waste)*

**[VISUAL: every pair of accounts compared for shared emails. A merge happens, which creates a new overlap, forcing another full pass. A "passes" counter climbs.]**

> Brute force: compare every pair of accounts; if their email sets intersect, merge them. But merging is transitive — fusing A and B might now make the combined set overlap C, which you'd already passed. So you loop over everything *again*… and again… until a full pass changes nothing.
>
> **[VISUAL: pairwise arrows, a merge, then arrows restart from the top.]**
>
> That's O(accounts² × emails) *per pass*, times multiple passes — cubic and ugly. The re-merging loop is the tell that we're using the wrong tool.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the transitive chain A–B–C. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The pain is transitivity — a merge creates new overlaps, forcing repeated passes. And Union-Find is *built* for transitive grouping. But there's a decision to make first.
>
> **LEARNER:** Right, Union-Find. So I make each *account* a node and union accounts that share an email?
>
> **TEACHER:** You *could* — but then you're back to comparing accounts pairwise to find shared emails. Pause and predict: **what if the nodes weren't the accounts at all? What single thing, if you made *it* the node, would turn "share an email" into "these are literally the same node"?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: each distinct EMAIL becomes a node dot. Within an account, all its emails get wired together. Shared emails automatically fuse two accounts' clusters.]**

> Here's the aha — and it's the whole problem: **make each distinct email a node, not each account.**
>
> Within a single account, union all its emails together — they obviously belong to one person. Now watch the magic: if two accounts share an email, that shared email is *the same node*, so unioning inside each account automatically fuses both accounts into one set — transitively, for free, no pairwise comparison.
>
> **[VISUAL: Account 1 unions {johnsmith, john_newyork}. Account 2 unions {johnsmith, john00}. Because johnsmith is one shared node, all four emails land in one set.]**
>
> After unioning everything, **group emails by their root** — each root is one person. Attach the owner's name (remembered per email), sort the emails, done.
>
> Why emails as nodes wins: the *connection itself* is the shared email. Making emails the nodes turns "they share an email" into "they touch the same node" — union does the transitive fusing with zero re-merge loops.

---

## 6. THE KEY MOVE (signaling) — `4:25`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Make the shared entity (the email) the node. Union within each record. Group by root."]**

> The key move: **make the shared key — the email — the Union-Find node; union all emails inside each account; then group by root.**
>
> Trigger phrase: *"merge records linked through shared keys, transitively"* → Union-Find keyed by the shared entity. That reframe — *what is the node?* — is the entire insight.

---

## 7. CODE IT — LIVE & CHUNKED — `5:05`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 — the same reusable class.]**

> Same Union-Find class you already know. `union` here doesn't need to return anything.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
```

> **[VISUAL: add chunk 2 — map every email to an integer id and remember its owner.]** Union-Find works on integers, so give each distinct email an id, and record its name.

```python
def accountsMerge(accounts):
    email_id = {}                       # email -> integer id
    email_name = {}                     # email -> owner name
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_id:
                email_id[email] = len(email_id)
            email_name[email] = name
```

> **[VISUAL: add chunk 3 — union emails within each account.]** Union every email in an account to its *first* email — that chains them all together.

```python
    uf = UnionFind(len(email_id))
    for account in accounts:
        first = email_id[account[1]]
        for email in account[2:]:
            uf.union(first, email_id[email])
```

> **[VISUAL: add chunk 4 — group by root.]** Bucket every email under its set root.

```python
    from collections import defaultdict
    groups = defaultdict(list)
    for email, idx in email_id.items():
        groups[uf.find(idx)].append(email)
```

> **[VISUAL: add chunk 5 — build the sorted output.]** Each group is one person: name plus sorted emails.

```python
    result = []
    for root, emails in groups.items():
        name = email_name[emails[0]]
        result.append([name] + sorted(emails))
    return result
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why each piece.
>
> `email_id` — Union-Find indexes integers, so every distinct email gets a stable integer id. A duplicate email reuses its id — that's what makes two accounts point at the *same* node.
>
> `email_name` — we lose track of which account an email came from once we union, so we stash the owner name per email up front. Names are consistent within a set, so any email in the group gives the right name.
>
> `uf.union(first, email_id[email])` — union each of an account's emails to its first. That's enough to chain them all: if a-b-c-d are in one account, unioning first `a` to each of b, c, d puts all four in one set.
>
> **LEARNER:** Why union everything to the *first* email? Why not union each email to the *next* one in a chain?
>
> **TEACHER:** Both work identically — union is transitive, so "a to b, a to c, a to d" produces the exact same set as "a to b, b to c, c to d." Anchoring on the first is just the simplest to write: one fixed reference, loop the rest. The resulting set — and its root — is the same either way.
>
> `groups[uf.find(idx)]` — bucket by root, so every email that traces to the same person lands together. Then `sorted(emails)` satisfies the required sorted output.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it, close the loop)*

**[VISUAL: emails assigned ids, sets merging, then final grouped output.]**

> Trace it. Ids: `johnsmith=0, john_newyork=1, john00=2, mary=3, johnnybravo=4`.

| account | unions | sets |
|---|---|---|
| `[John, 0, 1]` | union(0,1) | {0,1} |
| `[John, 0, 2]` | union(0,2) | {0,1,2} |
| `[Mary, 3]` | none | {3} |
| `[John, 4]` | none | {4} |

> Group by root: `{0,1,2}` → John with johnsmith, john_newyork, john00; `{3}` → Mary; `{4}` → John (johnnybravo). Sort each group's emails →

```
["John","john00","john_newyork","johnsmith"]
["Mary","mary"]
["John","johnnybravo"]
```

> Exactly the three people we predicted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:00`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(accounts³ × emails). Union-Find: O(E log E). E = total emails.]**

> Say it, with `E` = total emails: *"The pairwise-merge brute force is cubic in accounts because transitivity forces repeated passes. With Union-Find, the union pass is near-linear — O(E times alpha of E). The only real cost is sorting each group's emails, which totals O(E log E). Space is O(E) for the maps and the arrays."*
>
> Headline: *"The log factor is *only* from the required sorted output — the merging itself is effectively linear."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:40`
*(depth + honesty)*

**[VISUAL: the two maps + Union-Find arrays; note "O(E) — output lists all E emails anyway".]**

> Space is O(E) — the `email_id` and `email_name` maps plus the Union-Find arrays. You can't beat it: the output alone lists all `E` emails, so O(E) is the floor.
>
> Minor lever: you could skip `email_name` and record the name once per root the first time you see it — a constant-factor tweak. The `E log E` sort is unavoidable given the required sorted output. Say it: *"Already optimal at O(E); the real cleverness was choosing emails, not accounts, as the nodes — that's what made the merge transitive and linear instead of a repeated pairwise scan."*

---

## 12. YOUR TURN (active recall) — `11:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Sentence Similarity II (LC 737)". Word pairs linking transitively.]**

> Before you go, try **Sentence Similarity II**, LC 737. You're given pairs of similar words, and similarity is transitive — so two words are similar if a chain connects them. Same move: make each *word* a node, union the given pairs, then check if aligned words share a root. It's this problem's twin.
>
> Ten minutes of struggle first.

---

## 13. LOCK IT IN — `11:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Make the shared key the node** — emails, not accounts.
> 2. **Union within each record; transitivity fuses everything for free.**
> 3. **Group by root, attach the name, sort** — that's the output.
>
> Memory peg: **when records link through a shared thing, make that *thing* the node — union does the rest.**

---

## 14. CLIFFHANGER — `12:20`
*(open loop to next lesson)*

**[VISUAL: a montage — the trie tree, the Union-Find sets, then a blurred title for the next chapter.]**

> That closes the Tries and Union-Find chapter. You've got two power tools now: a trie that shares prefixes to make dictionary and prefix queries instant, and Union-Find that merges sets in near-constant time to answer "same group?" on the fly. Both show up constantly at Google — and both hinge on the same habit you've been building all along: *choose the right structure, and the hard problem gets easy.* On to the next chapter. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class UnionFind {
    int[] parent, rank;
    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }
    void union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
    }
}

public List<List<String>> accountsMerge(List<List<String>> accounts) {
    Map<String, Integer> emailId = new HashMap<>();
    Map<String, String> emailName = new HashMap<>();
    for (List<String> acc : accounts) {
        String name = acc.get(0);
        for (int i = 1; i < acc.size(); i++) {
            emailId.putIfAbsent(acc.get(i), emailId.size());
            emailName.put(acc.get(i), name);
        }
    }
    UnionFind uf = new UnionFind(emailId.size());
    for (List<String> acc : accounts) {
        int first = emailId.get(acc.get(1));
        for (int i = 2; i < acc.size(); i++)
            uf.union(first, emailId.get(acc.get(i)));
    }
    Map<Integer, List<String>> groups = new HashMap<>();
    for (Map.Entry<String, Integer> e : emailId.entrySet())
        groups.computeIfAbsent(uf.find(e.getValue()), k -> new ArrayList<>())
              .add(e.getKey());

    List<List<String>> result = new ArrayList<>();
    for (List<String> emails : groups.values()) {
        Collections.sort(emails);
        List<String> row = new ArrayList<>();
        row.add(emailName.get(emails.get(0)));
        row.addAll(emails);
        result.add(row);
    }
    return result;
}
```
