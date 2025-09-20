# Weekly Report 3

**Time spent:** ~ 20 hours 

## What did I do this week?
This week I redid and refined the core of my trie-backed n-gram name generator. I also wrote unit tests to validate the main functionalities, such as successor counts, generation behavior, and length constraints. I have started writing the Testing Documentation. In addition, I started working on a small user interface using Gradio to make the generator easier to test interactively. The project is now at the point where names can be generated from a dataset.

## How has the program progressed?
The program has progressed from a basic prototype into a more complete and testable package. It can now consistently generate new names that are distinct from the training data, while respecting constraints like maximum or fixed length. With the Gradio UI, I can quickly experiment with parameters and datasets which makes testing more user-friendly. Overall, the project is transitioning from the core implementation stage towards refinement and user friendliness.

## What did I learn this week/today?
I learned how to make a simple user interface using Gradio which is a Python package I haven't used before. I experimented with differ UI to see what would be most user friendly.  Writing unit tests taught me how important it is to cover edge cases, since many of the uncovered scenarios (like high-order n-grams or long target lengths) can cause unexpected failures.

## What remains unclear or has been challenging?
I realized that splitting code into separate modules (e.g., one for trie-building and one for generation) could improve clarity, but I am still unsure whether it’s necessary for my project right now. I’ve also found it unclear whether to not include generated names that are too similar to real names. For example, generating Ann from Anne would be disqualified as it is too similar to the real. For now, my generator only disqualifies names that are exact copies of the names in the dataset.

There are also some edge cases to handle, such as when selecting a very large order (e.g., 10) or a long target name length (e.g., 20). In these cases, the generator often fails to produce results and returns None. Handling these scenarios more gracefully is something I might try to explore further.
 
## What will I do next?
I plan on polishing the user interface more as well as doing some more testing with different types of data. I plan on adding a functionality where users can select the dataset to use for the trie from different options. I would like to see what names would be generated when combining different datasets. I will continue to polish the generator to handle special cases, such as when generated names are identical.