# Accounts Merge

> **LeetCode:** 721. Accounts Merge · **Difficulty:** 🟡 Medium · **Pattern:** Tries & Union-Find · **Google frequency:** medium

---

## Problem

Each account is `[name, email1, email2, ...]`. Two accounts belong to the **same person** if they share **any** email (names can repeat across different people, so the name alone doesn't identify a person). Merge accounts: return, for each person, `[name, ...sorted emails]` with duplicates removed.

**Example:**
```
accounts = [
  ["John","johnsmith@mail.com","john_newyork@mail.com"],
  ["John","johnsmith@mail.com","john00@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","johnnybravo@mail.com"]
]
→ [
  ["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","johnnybravo@mail.com"]
]
```
*(The first two Johns share `johnsmith@mail.com`, so they merge; the third John and Mary stay separate.)*

**Constraints that matter:** up to ~1000 accounts, total emails up to ~10⁴. Two accounts merge transitively through shared emails — if A shares an email with B and B with C, all three are one person. That **transitive grouping over shared keys** is the signature of **Union-Find**.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Compare every pair of accounts; if they share an email, merge their email sets." That's O(accounts² × emails) and the merging is transitive, so you'd have to keep re-merging until nothing changes — messy and slow.
- **The leap — union the emails, not the accounts.** Treat every distinct **email** as a node. Within a single account, union all its emails together (they clearly belong to one person). Because unioning is transitive, any two accounts sharing an email automatically end up in the same set. After processing all accounts, group emails by their **root**: each root is one person. Attach the owner's name (remembered per email) and sort each group's emails.
- **Why emails as nodes (not accounts)?** The connection *is* the shared email. Making emails the nodes means "share an email" becomes "these two emails are literally the same node," so union naturally fuses everything transitively — no pairwise account comparison, no re-merge loop.
- **Pattern trigger:** **"merge records that are linked through shared keys, transitively"** → **Union-Find keyed by the shared entity** (here, the email). DFS/BFS over an email-graph works too, but Union-Find is the cleanest expression.

---

## ① Brute Force

Repeatedly compare account email-sets; merge any two that intersect; loop until a full pass merges nothing.

```python
def accountsMerge_brute(accounts):
    groups = [(a[0], set(a[1:])) for a in accounts]
    changed = True
    while changed:
        changed = False
        merged = []
        used = [False] * len(groups)
        for i in range(len(groups)):
            if used[i]:
                continue
            name, emails = groups[i][0], set(groups[i][1])
            for j in range(i + 1, len(groups)):
                if used[j]:
                    continue
                if emails & groups[j][1]:          # share an email
                    emails |= groups[j][1]
                    used[j] = True
                    changed = True
            merged.append((name, emails))
        groups = merged
    return [[name] + sorted(emails) for name, emails in groups]
```

**Why it's the natural first attempt:** "merge any two accounts that overlap" is the literal task, done set-intersection at a time.

**Why it's not enough:** each pass is O(accounts² × emails), and transitivity forces multiple passes (a merge can create a new overlap), so it's O(accounts³ × emails) worst case. Way too slow and awkward.

**Complexity:** Time `O(accounts³ × emails)` worst case, Space `O(total emails)`.

---

## ② Optimised Solution (Union-Find over emails)

Union all emails within each account; group by root; sort.

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


def accountsMerge(accounts):
    email_id = {}                       # email -> integer id
    email_name = {}                     # email -> owner name
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_id:
                email_id[email] = len(email_id)
            email_name[email] = name

    uf = UnionFind(len(email_id))
    for account in accounts:
        first = email_id[account[1]]
        for email in account[2:]:       # union each email to the account's first
            uf.union(first, email_id[email])

    # group emails by their set root
    from collections import defaultdict
    groups = defaultdict(list)
    for email, idx in email_id.items():
        groups[uf.find(idx)].append(email)

    result = []
    for root, emails in groups.items():
        name = email_name[emails[0]]
        result.append([name] + sorted(emails))
    return result
```

**Walk the example:** assign ids — `johnsmith=0, john_newyork=1, john00=2, mary=3, johnnybravo=4`.
- Account 1 `[John, 0, 1]`: union(0,1) → set {0,1}.
- Account 2 `[John, 0, 2]`: union(0,2) → set {0,1,2} (because 0's root already covers 1).
- Account 3 `[Mary, 3]`: nothing to union → {3}.
- Account 4 `[John, 4]`: nothing to union → {4}.

Group by root: `{0,1,2}` → John with `johnsmith, john_newyork, john00`; `{3}` → Mary; `{4}` → John (johnnybravo). Sort each group's emails →
`["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"]`, `["Mary","mary@mail.com"]`, `["John","johnnybravo@mail.com"]`. ✅

**Why it's correct:** unioning every email inside an account to that account's first email guarantees all of an account's emails share a root; transitivity of union then fuses any two accounts sharing an email into one set automatically. Grouping by root yields exactly the per-person email sets. The name is consistent within a set because every email in it traces back to accounts of the same person.

**Complexity:** Let `E` = total emails. Time `O(E · α(E) + E log E)` — the union pass is near-linear, the `sort` per group totals `O(E log E)`. Space `O(E)`.

---

## ③ Space Optimization

The `O(E)` maps (`email_id`, `email_name`) and the Union-Find arrays are inherent — you must remember every email, its owner, and its set. You can't beat `O(E)` because the output alone lists all `E` emails.

> Minor levers: `email_name` can be avoided by storing the name once per root when you first see it, but that's a constant-factor tweak. The `E log E` sort time is unavoidable given the required sorted output. So space is already optimal at `O(E)`; the interesting part was *choosing emails (not accounts) as the union nodes*, which is what makes the merge transitive and linear instead of a repeated pairwise scan.

**Complexity:** Time `O(E log E)`, Space `O(E)`.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute (repeated pairwise set merges) | O(accounts³ × emails) | O(E) |
| Union-Find over emails | O(E log E) | O(E) |

*(E = total number of emails across all accounts.)*

---

## Say it out loud (interview narration)

> *"Accounts merge transitively through shared emails, which screams Union-Find. The key move is to make each distinct email a node — not each account. I union all emails within an account together, so any two accounts sharing an email land in the same set automatically, transitively, with no pairwise comparison. I keep a map from email to owner name and email to id. After unioning, I group emails by their set root — each root is one person — attach the name, and sort each group's emails. find uses path compression, union uses union by rank, so the merging is near-linear; the only log factor is the required sorted output. That's O(E log E), versus the ugly repeated-pairwise-merge brute force."*

## Related / follow-ups
- **Number of Provinces** (LC 547 — union-find components)
- **Redundant Connection** (LC 684 — union-find cycle detection)
- **Similar String Groups** (LC 839 — union strings that are one swap apart)
- **Sentence Similarity II** (LC 737 — transitive word-pair grouping via union-find)
