# Weekly Report 1

**Time spent:** ~10 hours 

## What did I do this week?
This week I started my project. I researched what topics I wanted to pursue. I couldn’t decide between rock, paper, scissors and a name generator, since they both involve Markov chains which I was interested in implementing. In the end, I settled for the name generator, as it seemed the simpler one to execute and it would be interesting to see the results. Overall, most of the week consisted of research and YouTube videos explaining the concepts (Markov chains, tries, machine learning, etc.)


## How has the program progressed?
So far, I have set up my Python development environment and created a GitHub repository. I have also drafted a project plan and have been researching the algorithms and data structures at the core of the project, such as tries, n-grams, and backoff generation. I haven’t begun writing the code as I would like to do more research on the algorithms and data structures and how to implement them.

## What did I learn this week/today?
I learned how a trie (prefix tree) works and why it is efficient for storing prefixes and supporting n-gram lookups. Furthermore, I learned about n-grams as sequences of tokens used in Markov chains, and how backoff generation makes sure that name generation always continues even if a specific context has not been seen before. 
From a wider perspective, I learned how this connects to computational creativity, where algorithms are used to generate new, human-like artifacts (in this case, names) rather than just analyze data. I also learned how this fits within machine learning, since the generator learns statistical patterns from a training set and uses them to produce unique outputs that resemble the style of the original data. Moreover, learning about the time and space complexities for training and generation helped me see that the project is possible and grounded theoretically.

## What remains unclear or has been challenging?
Since I’ve been mostly focused on the theory and haven’t started coding yet, at this point, the most unclear aspect is the practical execution of the program. I understand the theory behind tries, n-grams, backoff, and probability sampling, but I am not yet sure how smoothly these ideas will translate into an actual implementation. For example, I expect challenges in structuring the trie to handle arbitrary order n and making sure that probability normalization and sampling work as intended. Once I start coding, I will likely discover practical details that are harder than they appear on paper.

## What will I do next?
My next step will be to preprocess the data that will be used for training by removing duplicates and punctuation, counting frequencies, lowercasing, and then tokenizing them. After that I will begin implementing the core trie and n-gram model. I will start by inserting names into the trie and verifying that context-continuation counts are stored correctly. I will probably test the functionality by training the model using a few names only. 
