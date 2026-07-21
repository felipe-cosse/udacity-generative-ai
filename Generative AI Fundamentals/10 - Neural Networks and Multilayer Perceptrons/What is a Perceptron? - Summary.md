# Summary: What is a Perceptron?

**Source Page:** [Neural Networks and Multilayer Perceptrons - What is a Perceptron?](https://learn.udacity.com/nd608?version=3.2.31&partKey=cd13303&lessonKey=41665816-e0df-4725-9349-0fb6c898ac4a&conceptKey=de63bc57-fa57-4191-80be-e4a3e1aaa99c)

## High-Level Overview
A **Perceptron** is the most basic building block of artificial neural networks. Functionally, it operates as a single-neuron binary classifier that maps an input vector to a binary output (e.g., 0 or 1, or classifying an image as a "Cat" vs. "Dog").

---

## Architecture & Mathematical Flow
The perceptron processes data through three key computational steps:

1. **Weighted Inputs:** Receives $N$ numerical inputs $\mathbf{x} = [x_1, x_2, \dots, x_n]^T$ and multiplies each input by a corresponding learnable weight $w_i$.
2. **Summation:** Computes the linear dot product sum of inputs and weights:
   $$\text{Sum} = \sum_{i=1}^{n} w_i x_i + b$$
3. **Activation Function:** Passes the sum through a binary step function $f(z)$:
   $$f(z) = \begin{cases} 1 & \text{if } z > 0 \\ 0 & \text{if } z \le 0 \end{cases}$$

---

## Learning Mechanism
* **Iterative Weight Adjustments:** Starts with initial weight values and processes labeled training samples.
* **Error Correction ("Nudging"):** If the prediction matches the ground truth label, weights remain unchanged. If incorrect, the parameters are incrementally nudged based on prediction error.
* **Scalability:** A single perceptron is limited to linearly separable decision boundaries. Combining multiple perceptrons into a Multi-Layer Perceptron (MLP) enables deep networks to solve complex, non-linear tasks (such as full image classification).