# Specification Document

**Study program:** Bachelor's Programme in Science (BSc)  

---

## Project Plan
For my project I will use the programming language **Python**.  
This is the only language I am proficient in to the extent that I could peer-review projects written in it.  

My project plan is to design a **name generator** under the topic of computational creativity and machine learning.  

---

## Algorithms I plan to use
- For the algorithm, I will use an n-gram Markov chain. My model will learn P(next token ∣ last n tokens) from a dataset of either Finnish or English names. The n will be chosen by the user. 
- In addition to this, I will use a backoff generation, in case the data set does not contain statistics for every possible n-length context. At generation time, if the full n-length context isn’t found, the algorithm will back off to n−1,n−2,…,1 to ensure a next token can be sampled. Backoff generation would make sure the generator would not get stuck and prevents the model from memorizing only long n-gram. 
- I will also use a Maximum-likelihood estimation to record how often each token follows a given context when I train the model. 
- I would also like to explore the addition of temperature sampling which can be used to define how creative the names can be.
- Post-generation constraints and filters will be implemented to ensure that the output stays between a certain character length, has the correct vowel and consonant ratio, and rejects duplicates 


## The data structures I plan to use
- I will build a trie of all observed n-grams up to order n. At each node, I will also store a record of which tokens followed that prefix and how many times.
- I will use counters/frequency tables to get the statistics needed for the maximum-likelihood estimation. It will map {token → count} and remember how often each next token followed a context.
- I will use sets and hash maps to support fast checks for uniqueness and allowed characters. Sets will store unique items and check membership fast (O(1) average time). The hash table will make sure the lookups are quick

---

## Problem addressed
The problem my project addresses is automatic name generation. My model will create new names that resemble the style of an existing dataset while avoiding duplicates and nonsense names. Simple ransom mashup methods usually ignore sequence structure and naive Markov models are at risk of just memorizing the training data. My solution is to create an arbitrary order n-gram Markov chain stored in a trie, alongside probability sampling and filters, to generate names that are both stylistically consistent without being copies of the training data.

---

## The inputs my program will receive
- The model will use a dataset of names. This will be tokenized into characters or syllables and inserted into the trie as n-grams. The dataset will also be used to compute frequency counts for the probabilities for the Markov chain. The program will generate new names that resemble the style of the training corpus but are not direct copies.
- The program will also have user parameters such as the chain order n, temperature, and length limits.The chain order will determine how many tokens of context the model uses when predicting the next token. The temperature controls the creativity by either sharpening or flattening probabilities when sampling. Min/max name length will prevent outputs that are too short or too long. 

--- 

## Expected time and space complexities
- Training phase: Insert all tokens into the trie for all n-grams → O(N×n) 
    - where N = total tokens in the data and n = Markov order
    - Source from [wikipedia](https://en.wikipedia.org/wiki/Trie)
- Generation phase: Backoff lookups in the trie + probability sampling → O(T)
    - T = length of generated name 
    - To generate a name of length T, the algorithm repeats T steps of context lookup and token sampling. Each lookup may back off through up to n contexts (cost ≤ O(n^2)) and sample from a small set of candidates (≤ vocabulary size b). Since both n and b are small constants, the total cost per name is O(T) i.e. linear in the output length.
- Filters/constraints: Exact duplicate check → O(1) with hash set

---

## Sources I intend to use
- [Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie)  
- [Wikipedia: Markov chains](https://en.wikipedia.org/wiki/Markov_chain)  
- [Markov decision process](https://en.wikipedia.org/wiki/Markov_decision_process)  
- [Finnish name database](https://www.opendata.fi/data/en_GB/dataset/none/resource/08c89936-a230-42e9-a9fc-288632e234f5)  
- [Kaggle English name corpus](https://www.kaggle.com/datasets/nltkdata/names)  

---

## Core of the project
The core of my project is computational creativity through machine learning. An arbitrary order n-gram Markov chain will be implemented with a trie to model and generate names. The algorithm learns statistical patterns of character sequences from a training dataset of names, stores these sequences in the trie, and then generates new names by sampling continuations from the learned probabilities. Key components of the model include maximum-likelihood estimation of n-gram probabilities, backoff generation for unseen contexts, and controlled sampling to have balance between realism and creativity. 
