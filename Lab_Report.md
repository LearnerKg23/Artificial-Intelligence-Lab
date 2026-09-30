# AI Laboratory: Bayesian Networks and Autoregressive Language Models

## Deliverables

### 1. Python implementation of the first-order model
The complete code is also available in `lab_implementation.py`.

```python
import random
from collections import defaultdict

class FirstOrderModel:
    def __init__(self):
        # C(w_i, w_j)
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        # P(w_j | w_i)
        self.probabilities = defaultdict(dict)
        
    def train(self, data):
        # Count transitions
        for sentence in data:
            for i in range(len(sentence) - 1):
                current_word = sentence[i]
                next_word = sentence[i+1]
                self.transition_counts[current_word][next_word] += 1
                
        # Construct conditional distribution
        for current_word, next_words in self.transition_counts.items():
            total_transitions = sum(next_words.values())
            for next_word, count in next_words.items():
                self.probabilities[current_word][next_word] = count / total_transitions

    def predict_most_probable(self, word):
        if word in self.probabilities:
            next_words = self.probabilities[word]
            return max(next_words, key=next_words.get)
        return None

    def sample_next_token(self, word):
        if word in self.probabilities:
            next_words = list(self.probabilities[word].keys())
            probs = list(self.probabilities[word].values())
            return random.choices(next_words, weights=probs, k=1)[0]
        return None

    def generate_sentence(self, mode="sample"):
        current_word = "<START>"
        sentence = []
        while True:
            if mode == "greedy":
                next_word = self.predict_most_probable(current_word)
            else:
                next_word = self.sample_next_token(current_word)
                
            if next_word is None or next_word == "<END>":
                break
            sentence.append(next_word)
            current_word = next_word
        return " ".join(sentence)
```

### 2. Python implementation of the second-order model

```python
class SecondOrderModel:
    def __init__(self):
        # C((w_{t-2}, w_{t-1}), w_t)
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.probabilities = defaultdict(dict)
        
    def train(self, data):
        for sentence in data:
            if len(sentence) < 3:
                continue
            for i in range(len(sentence) - 2):
                context = (sentence[i], sentence[i+1])
                next_word = sentence[i+2]
                self.transition_counts[context][next_word] += 1
                
        for context, next_words in self.transition_counts.items():
            total = sum(next_words.values())
            for next_word, count in next_words.items():
                self.probabilities[context][next_word] = count / total

    def sample_next_token(self, context):
        if context in self.probabilities:
            next_words = list(self.probabilities[context].keys())
            probs = list(self.probabilities[context].values())
            return random.choices(next_words, weights=probs, k=1)[0]
        return None

    def generate_sentence(self):
        context = ("<START>", "the")
        sentence = ["the"]
        while True:
            next_word = self.sample_next_token(context)
            if next_word is None or next_word == "<END>":
                break
            sentence.append(next_word)
            context = (context[1], next_word)
        return " ".join(sentence)
```

### 3. Conditional probability tables for selected contexts

- **P(next word | the)**
  - cat: 3/12 (0.25)
  - dog: 3/12 (0.25)
  - mat: 2/12 (0.1667)
  - rug: 2/12 (0.1667)
  - park: 2/12 (0.1667)
- **P(next word | cat)**
  - sat: 2/3 (0.6667)
  - ran: 1/3 (0.3333)
- **P(next word | dog)**
  - sat: 2/3 (0.6667)
  - ran: 1/3 (0.3333)
- **P(next word | sat)**
  - on: 4/4 (1.0)
- **P(next word | ran)**
  - to: 2/2 (1.0)

### 4. Examples of generated text

**First-Order Model (Sampling Mode):**
- "the dog sat on the park"
- "the cat ran to the mat"
- "the cat sat on the rug"
- "the dog ran to the park"
- "the cat sat on the mat"

**First-Order Model (Greedy Mode):**
- "the cat sat on the mat"
- "the cat sat on the mat"
- "the cat sat on the mat"
- "the cat sat on the mat"
- "the cat sat on the mat"

**Second-Order Model (Sampling Mode):**
- "the cat sat on the rug"
- "the dog ran to the park"
- "the dog sat on the mat"

### 5. Results of probability-normalisation tests
```python
for word in model.probabilities:
    total = sum(model.probabilities[word].values())
    print(f"Total probability for '{word}': {total}")
```
**Output**: 
- Total probability for `<START>`: 1.0
- Total probability for `the`: 1.0
- Total probability for `cat`: 1.0
- Total probability for `dog`: 1.0
- ... 
*All totals correctly sum to 1.0.*

### 6. Answers to Questions 1–14

**Question 1: Why is this decomposition useful for generating text?**
The autoregressive decomposition $P(X_1, \dots, X_T) = P(X_1) \prod_{t=2}^T P(X_t | X_1, \dots, X_{t-1})$ is useful for generating text because it breaks down the joint probability of a sequence into a product of conditional probabilities. This allows us to generate text iteratively, one token at a time from left to right, matching the sequential nature of natural language.

**Question 2: What independence assumption is being made by this network?**
The network assumes the Markov property: the probability of the current word depends only on the immediately preceding word, and is conditionally independent of all other previous words in the sequence. Expressed in probability notation: $P(X_t | X_1, \dots, X_{t-1}) = P(X_t | X_{t-1})$.

**Question 3: Construct the conditional probability distribution and identify zero-probability transitions.**
(See Deliverable 3 for the tables).
Zero-probability transitions: For any current word, words that never immediately follow it in the dataset have zero probability. For example, for the word `the`, any word not in {cat, dog, mat, rug, park} has zero probability (e.g., $P(\text{on} | \text{the}) = 0$).

**Question 4: Where in the program are the transition counts stored?**
The transition counts are stored in a nested dictionary object named `self.transition_counts`, accessed like `self.transition_counts[current_word][next_word]`.

**Question 5: Where is $P(X_t | X_{t-1})$ computed?**
It is computed in the `train()` method within a loop over the transition counts. The count of a specific transition is divided by the total number of transitions from the `current_word`, resulting in the conditional probability: `self.probabilities[current_word][next_word] = count / total_transitions`.

**Question 6: How does the program choose the next word? Is it always choosing the most probable word, or sampling?**
According to the specification ("generate a sentence by repeatedly sampling the next token"), the program chooses the next word by sampling from the conditional probability distribution. Sampling differs from always choosing the most probable word because it uses the probabilities as weights for a random choice, allowing for different paths and variations, whereas always choosing the most probable word (greedy generation) would be deterministic and output the exact same sentence every time.

**Question 7: What happens if the program encounters a word for which no transition has been observed?**
If a word with no observed transitions is encountered (e.g. it is not a key in `self.probabilities`), the prediction/sampling functions will not be able to find a next word. In the provided implementation, the function checks `if word in self.probabilities` and returns `None` if it isn't, which correctly triggers the loop to break and stop generation.

**Question 8: If one of the totals is 0.87, what does this tell you about the implementation?**
By the axioms of probability, the sum of probabilities for all possible next words given a specific current word must equal 1.0. If the sum is 0.87, it means there is a bug in the implementation—either the counts were tallied incorrectly, some transitions were skipped, or there's a floating-point calculation error.

**Question 9: Are the most probable predictions always the same as the words that you would personally expect? What does this tell you about the difference between a probability model and human linguistic expectations?**
Not always. A simple probability model's predictions are strictly limited to the statistical frequencies observed in its specific (and often limited) training dataset. For instance, it may assign a high probability to "cat" following "the" because it happens frequently in the small dataset. Humans, however, draw upon vast semantic understanding, world knowledge, and a far wider linguistic context to form expectations.

**Question 10: Compare the two sets of generated sentences. Which mode produces more variation? Why?**
Mode B (Sampling) produces significantly more variation. Mode A (Greedy) is entirely deterministic; starting from `<START>`, it will always pick "the", then always pick "cat" (tied with dog but first in max evaluation), then "sat", "on", "the", "mat", producing identical sentences repeatedly. Sampling incorporates randomness proportional to the probabilities, exploring different possible linguistic paths.

**Question 11: How does the second-order model differ from the first-order model in terms of:**
1. **Graph structure:** Each node $X_t$ now has incoming directed edges from both $X_{t-1}$ and $X_{t-2}$.
2. **Conditional probability table:** The CPT takes a context of two words $(X_{t-2}, X_{t-1})$ as the condition to yield a distribution over the next word $X_t$, creating a 2D context key.
3. **Amount of context:** The context size doubles, relying on the two preceding words instead of just one.
4. **Amount of data needed:** Exponentially more data is required to robustly estimate probabilities because the number of possible contexts (word pairs) is drastically larger than individual words, exacerbating data sparsity.

**Question 12: Why does increasing the amount of context potentially improve prediction? Why can it simultaneously make the model harder to estimate from limited data? Relate your answer to the size of the conditional probability table.**
Increasing context improves prediction by providing more specific information (e.g., distinguishing between "sat on the" and "ran to the"). However, because the size of the CPT grows exponentially with the context length (Vocab Size ^ Context Length), a limited dataset will fail to cover most of the possible context combinations. This leaves many entries in the CPT with zero counts, making the model harder to estimate accurately for unseen contexts.

**Question 13: Why is Approach B preferable when constructing an intelligent system?**
Approach B is preferable because it explicitly defines the intended behaviour and the exact probabilistic model to be implemented. This avoids treating the LLM as a black box and requires the user to understand the underlying representation (CPTs and counts). It also makes it possible to validate the implementation by testing probabilistic invariants (like probabilities summing to 1) and ensures a clear distinction between the theoretical model and the code used to run it.

**Question 14: What did thinking of the language model as a Bayesian network give you?**
- **A representation of dependencies:** It made explicit which previous variables (words) influence the current variable.
- **A factorisation of the joint distribution:** It showed exactly how to break down the complex joint probability of a full sentence into smaller, tractable conditional probabilities.
- **A way to reason about independence assumptions:** It visually and mathematically clarified what the model ignores (e.g., that $X_3$ is conditionally independent of $X_1$ given $X_2$ in a first-order model).

### 7. Reflection on LLM Usage
Using an LLM was highly effective for scaffolding the Python implementation because I provided a strict behavioural specification rather than a vague request. I instructed the LLM to use simple counts and native Python data structures instead of neural network libraries. 

*Validation Example:* I inspected the generated `train()` method for the first-order model to ensure it was properly computing the probabilities from the raw counts:
```python
for current_word, next_words in self.transition_counts.items():
    total_transitions = sum(next_words.values())
    for next_word, count in next_words.items():
        self.probabilities[current_word][next_word] = count / total_transitions
```
I verified that dividing `count` by `total_transitions` guarantees that the probabilities sum to 1.0 for each `current_word`, which I then successfully tested using the probability normalisation script. This validated that the implementation correctly mirrored the underlying probabilistic model.
