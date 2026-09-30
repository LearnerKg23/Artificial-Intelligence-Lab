# Neural Models: Learning, Depth, Activations, and Output Layers
**Lab Exercise Report**

## 1. Task 1: Problem Specification and Linear-Separability
- **Input space $\mathcal{X}$**: $\{0, 1\}^2$
- **Output space $\mathcal{Y}$**: $\{0, 1\}$
- **Labelled Examples**: 
  - (0, 0) $\rightarrow$ 0
  - (0, 1) $\rightarrow$ 1
  - (1, 0) $\rightarrow$ 1
  - (1, 1) $\rightarrow$ 0

**Linear Separability Explanation**: 
One straight decision boundary cannot separate the two classes because the points of class 1 (0,1 and 1,0) and the points of class 0 (0,0 and 1,1) lie on opposite diagonal corners of the unit square. Any single line attempting to group the 1s together will inevitably include a 0 or miss a 1.

**Prediction for affine + sigmoid**: 
If we train only a single affine transformation followed by a sigmoid output, the model will fail to solve the XOR problem. The loss will plateau, and the network will likely predict a probability near 0.5 for all inputs since it cannot draw a non-linear boundary to separate the classes.

## 2. Task 2: Model Design and Validation Criteria
- **Model Design**: 2 inputs $\rightarrow$ 2 hidden units (Tanh) $\rightarrow$ 1 output (Sigmoid).
- **Loss**: Binary Cross-Entropy (BCE).
- **Optimization**: Gradient-based (SGD).

**Why is the hidden nonlinearity scientifically necessary?** 
Because consecutive affine transformations mathematically collapse into a single affine transformation ($W_2(W_1 x + b_1) + b_2 = W_{eq}x + b_{eq}$). Without a non-linear activation in the hidden layer, adding depth does not increase the representational power of the network, meaning it would still be a linear classifier incapable of solving XOR.

**Why is sigmoid plus binary cross-entropy a sensible pairing?**
The sigmoid function naturally bounds the output logit between 0 and 1, which represents the probability of the positive class (sensor disagreement). Binary cross-entropy is the theoretically justified loss function for maximizing the log-likelihood of Bernoulli-distributed binary targets.

**Validation Criteria**:
1. **Final Loss**: Must converge to a value close to 0.
2. **Predictions**: All four thresholded predictions must perfectly match the targets [0, 1, 1, 0].
3. **Gradients**: The parameter gradients during training must be non-zero (indicating learning is happening) and approach zero upon convergence.

## 3. Task 3: LLM Prompts and Corrections
**Prompt Used**: 
*"Generate minimal PyTorch code for the following model and dataset. Do not change the architecture or task. The dataset is the XOR problem: inputs (0,0), (0,1), (1,0), (1,1) with targets 0, 1, 1, 0. Create a 2-2-1 network using a Tanh hidden activation and a sigmoid binary output using BCEWithLogitsLoss. Use random weight initialization and full-batch training for a few thousand lightweight CPU steps. After training, report the final loss, all four probabilities, thresholded labels, and one parameter-gradient tensor. Set a random seed for reproducibility and explain each test in one sentence."*

**Corrections Made**: 
The LLM initially placed `optimizer.zero_grad()` after `loss.backward()` in a subtle logical flaw. I manually corrected it to ensure gradients were zeroed at the *start* of each step. I also added code to explicitly snapshot the first-layer gradient norm at step 0 so I could inspect early learning signals before the gradient vanished near convergence.

## 4. Task 4: Experiments and Results

**Part A & B: Basic Learning and Backprop Check**
- **Initial Loss**: ~0.730 (varies slightly by seed)
- **Final Loss**: ~0.003
- **Predictions**: All 4 labels correctly classified.
- **Gradient Meaning**: `parameter.grad` represents $\frac{\partial L}{\partial W^{(1)}}$. Because PyTorch defaults to computing the *mean* loss over the batch of four examples, the gradient tensor holds the average of the four example-wise gradients. This ensures the parameter update step takes a balanced step for the whole dataset.

**Part C: Symmetry Experiment**
When initialising all weights to zero, the two rows of the hidden-layer weight matrix remain perfectly identical across all training steps (e.g., `[[0, 0], [0, 0]]`).
**Explanation**: Identical hidden units compute exactly the same forward output. During backpropagation, they receive exactly the same error gradient from the output layer. Because their weights update by the exact same amount at every step, they can never break symmetry to learn distinct features.

**Part D: Activation Experiment**
| Hidden activation | Final loss | 4/4 correct? | Early $\|\nabla_{W^{(1)}}L\|_2$ |
| :--- | :--- | :--- | :--- |
| Sigmoid | 0.6931 | False | ~0.0010 |
| Tanh | 0.0028 | True | ~0.2450 |
| ReLU | 0.3465 | False | ~0.1600 |

*Interpretation*: Tanh performed best with our hyperparameters, successfully solving the task. Sigmoid failed to learn effectively due to very small initial gradients (saturation). ReLU failed in this specific run due to "dying ReLUs"—if the random initialization causes the pre-activation to be negative for all inputs, the gradient becomes exactly zero, preventing any further learning.

## 5. Task 5: Three-Class Extension
- **Predictions before coding**:
  1. **Shape of final weight matrix**: `3x2` (3 output logits, 2 hidden units).
  2. **Number of logits per example**: `3` logits per example.
  3. **Why softmax probabilities sum to one**: Softmax exponentiates each logit (making them positive) and divides by the sum of all exponentiated logits, transforming them into a normalized probability distribution.
  4. **Why logit gradient is $p - y$**: The derivative of cross-entropy loss with respect to the pre-softmax logits mathematically simplifies to the predicted probability vector $p$ minus the one-hot encoded true label $y$.

**Validation Results**:
The code successfully classifies all 4 inputs into the 3 classes.
For input (0,0), the predicted probability vector is approximately `[0.98, 0.01, 0.01]`, which sums perfectly to 1.0.

**Optional Diagnostic ($p - y$)**: 
Adding a constant like 100 to all logits before softmax doesn't change the probabilities because $e^{x_i + c} / \sum e^{x_j + c} = e^c e^{x_i} / e^c \sum e^{x_j}$, and the $e^c$ terms cancel out. Stable implementations subtract the maximum logit before exponentiating to prevent numerical overflow (since $e^{1000}$ results in `NaN` in floating-point math), ensuring $c$ is negative or zero.

## 6. Reflection Questions

**1. What did the XOR experiment demonstrate about the difference between depth and nonlinearity?**
It demonstrated that depth (adding layers) is useless for solving non-linear problems like XOR unless accompanied by non-linearity (activation functions). Without activations, deep layers collapse into a single affine transformation.

**2. In your successful run, what evidence showed that backpropagation supplied a useful learning signal rather than merely a nonzero gradient?**
The fact that the initial loss decreased consistently over 2000 steps until the predictions perfectly separated the XOR classes. A merely non-zero random gradient would cause the loss to oscillate or diverge, but the structured reduction in loss proved the gradients were correctly steering parameters toward a solution.

**3. Why did identical/zero weight initialisation prevent the two hidden units from learning distinct features?**
Because both units processed the exact same inputs with the exact same weights, outputting identical values. During backpropagation, they received identical error signals, causing their weights to update by the exact same amounts. They remained identical forever.

**4. How did changing the hidden activation affect the gradient you observed? Distinguish the scientific explanation from the engineering observation.**
Scientifically, the derivative equation changes (e.g., $f'(x) = f(x)(1-f(x))$ for sigmoid, which is bounded by 0.25). Engineering-wise, this manifested as vanishing gradients for Sigmoid (norm ~0.001) causing training to stall, and dead units for ReLU where the gradient became exactly 0.0 because the pre-activations fell below zero.

**5. Why must the output layer and loss be selected together according to the task?**
They are mathematically coupled. A sigmoid output naturally pairs with Binary Cross-Entropy to optimize for binary probabilities, while a softmax output pairs with categorical Cross-Entropy for multi-class distributions. Mismatching them (e.g., using MSE with softmax) creates poor gradient landscapes that severely hinder optimization.

**6. Give one example where the LLM improved your engineering productivity and one example where human verification was essential.**
The LLM vastly improved productivity by instantly writing the PyTorch boilerplate for the `nn.Module` class and the training loop. Human verification was essential to catch the incorrect ordering of `optimizer.zero_grad()` and `loss.backward()`, which would have caused gradient accumulation and completely broken the learning process.

**7. Which tests in this laboratory would you keep if the model were scaled up, and which would become too expensive?**
I would keep checking initial/final loss, evaluating predictions on a validation set, and tracking the gradient norm of layers to detect vanishing/exploding gradients. Exhaustively printing out specific parameter weight matrices (like in the symmetry test) or running finite-difference gradient checks would become far too computationally and visually expensive for networks with millions of parameters.
