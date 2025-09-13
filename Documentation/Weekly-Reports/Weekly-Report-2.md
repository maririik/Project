# Weekly Report 2

**Time spent:** ~13 hours 

## What did I do this week?
This week, I started writing my code. I created a basic trie data structure and added initial preprocessing and loading functions for the name datasets. I also added the Kaggle name datasets into the repository, wrote unit tests for the cleaning and loading functions, and confirmed that the real data loads correctly.The program also has an initial n-gram trie which trains on names and returns successor counts. 
## Test Coverage

This week I set up pytest with coverage tracking.  
The current report shows:

| File                    | Statements | Missing | Coverage |
|-------------------------|------------|---------|----------|
| src/namegen/__init__.py | 1          | 0       | 100%     |
| src/namegen/corpus.py   | 29         | 0       | 100%     |
| src/namegen/trie.py     | 30         | 1       | 97%      |
| **Total**               | **60**     | **1**   | **98%**  |

Next steps: address the single missing edge case in the `trie.py` module to reach full coverage.

## How has the program progressed?
The program now successfully loads raw name data, cleans it (removing invalid characters, handling spaces, apostrophes, and hyphens), and validates that the cleaned names meet length and formatting requirements. I also implemented an initial version of the n-gram trie model that adds start/end markers and accumulates successor counts for each n-1 length context. I also added unit tests for the preprocessing and data loading pipeline, as well as some tests of the trie structure. The trie model has also been tested manually on small examples (e.g., “anna”, “anne”), showing that it produces the expected successor counts.

## What did I learn this week/today?
I learned mostly about the trie structure and how to implement it in code. Most sources I found online use the trie to store strings efficiently, so I had to tweak the structure to also store n-gram contexts and their successor counts. This helped me understand how tries can be adapted beyond simple word lookup.

I wasn’t so familiar with unit testing, so I learned a lot about how to write focused tests for preprocessing and data loading functions, as well as how to run them with pytest and interpret the results. I also learned about test coverage and how to implement it.

## What remains unclear or has been challenging?
The most unclear aspects have been with the datasets. Some names in the datasets include apostrophes or hyphens, and I am unsure whether to include their use in the name generator. For now, I have decided to include them, but once I start testing outputs using the n-gram trie I might remove punctuation entirely. Another challenging aspect has been whether to use the English names or Finnish names dataset. In the English dataset, there are much more female name entries (5001) than male names (2943), so I'm debating whether switching to the Finnish name dataset would produce more balanced results, as it has a more even spread.

## What will I do next?
Next, I will finish writing unit tests for the NGramTrie implementation to reach the full coverage. After that, I plan to start experimenting with the name generation logic. This entails sampling tokens step by step from the trie until an end marker is reached. I also want to integrate the cleaned dataset into the generator and check that it produces realistic outputs. 
