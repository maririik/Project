# Weekly Report 5

**Time spent:** ~ 7 hours 

## What did I do this week?
This week I finished the peer review. I also continued drafting both the Implementation document and the Testing document. Additionally, I expanded the testing. I added deterministic tests using seeded RNG and a tiny FakeRNG to remove flaky retries and used pytest’s monkeypatch to control sample_weighted choices and early-stop behavior. I also added a PPokémon data set.

## How has the program progressed?
The test coverage has increased from ~62% to ~86% (terminal shows namegen.py ~78%, trie.py ~97%). The generator and trie behavior are now covered for both normal flow and edge cases (invalid order, empty names, missing successors).

## What did I learn this week/today?
This week I learned how to use pytest’s monkeypatch to replace functions/attributes during tests and restore them automatically.

## What remains unclear or has been challenging?
Balancing “meaningful” tests with “branch-hitting” tests. Some coverage lines are fallbacks that require contrived inputs (weird mappings) to reach
 
## What will I do next?
I will continue working on the Implementation and Testing documents. I will push coverage toward 90%+ and try to finalise the tests. 

