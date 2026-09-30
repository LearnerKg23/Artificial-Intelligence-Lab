import random
from collections import defaultdict

# Part III: Dataset
corpus = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]

def tokenize(corpus):
    tokenized = []
    for sentence in corpus:
        tokens = ["<START>"] + sentence.lower().split() + ["<END>"]
        tokenized.append(tokens)
    return tokenized

tokenized_data = tokenize(corpus)

# Part V & VI: First-order autoregressive model
class FirstOrderModel:
    def __init__(self):
        # Stores counts of transitions: C(w_i, w_j)
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        # Stores probabilities: P(w_j | w_i)
        self.probabilities = defaultdict(dict)
        
    def train(self, data):
        # 2. Count transitions
        for sentence in data:
            for i in range(len(sentence) - 1):
                current_word = sentence[i]
                next_word = sentence[i+1]
                self.transition_counts[current_word][next_word] += 1
                
        # 3. Construct conditional distribution
        for current_word, next_words in self.transition_counts.items():
            total_transitions = sum(next_words.values())
            for next_word, count in next_words.items():
                self.probabilities[current_word][next_word] = count / total_transitions

    def display_probabilities(self, word):
        if word in self.probabilities:
            print(f"P(next | '{word}'):")
            for next_word, prob in self.probabilities[word].items():
                print(f"  {next_word}: {prob:.4f}")
        else:
            print(f"No observed transitions for '{word}'")

    def predict_most_probable(self, word):
        if word in self.probabilities:
            next_words = self.probabilities[word]
            best_word = max(next_words, key=next_words.get)
            return best_word
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

model = FirstOrderModel()
model.train(tokenized_data)

print("--- Part VII: Test the Probability Model ---")
for word in model.probabilities:
    total = sum(model.probabilities[word].values())
    print(f"Total probability for '{word}': {total}")

print("\n--- Part VIII: Predicting the Next Word ---")
for w in ["the", "cat", "dog", "sat", "ran"]:
    model.display_probabilities(w)
    print(f"Most probable after '{w}': {model.predict_most_probable(w)}\n")

print("--- Part IX & X: Generate Text ---")
print("Sampling mode:")
for i in range(5):
    print(f"{i+1}: {model.generate_sentence(mode='sample')}")

print("\nGreedy mode:")
for i in range(5):
    print(f"{i+1}: {model.generate_sentence(mode='greedy')}")

# Part XI & XII: Second-order autoregressive model
class SecondOrderModel:
    def __init__(self):
        # Stores counts: C((w_{t-2}, w_{t-1}), w_t)
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
            total_transitions = sum(next_words.values())
            for next_word, count in next_words.items():
                self.probabilities[context][next_word] = count / total_transitions

    def sample_next_token(self, context):
        if context in self.probabilities:
            next_words = list(self.probabilities[context].keys())
            probs = list(self.probabilities[context].values())
            return random.choices(next_words, weights=probs, k=1)[0]
        return None

    def generate_sentence(self):
        # First word is sampled from P(X_2 | X_1 = <START>) using first order model logic
        # For simplicity in 2nd order, we can assume we always start with "<START> the"
        # since all our training sentences begin that way.
        context = ("<START>", "the")
        sentence = ["the"]
        while True:
            next_word = self.sample_next_token(context)
            if next_word is None or next_word == "<END>":
                break
            sentence.append(next_word)
            context = (context[1], next_word)
        return " ".join(sentence)

model2 = SecondOrderModel()
model2.train(tokenized_data)

print("\n--- Part XII & XIII: Second-order generation ---")
for i in range(5):
    print(f"{i+1}: {model2.generate_sentence()}")

