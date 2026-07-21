# Summary: Training Neural Networks

Training a neural network (such as a Multilayer Perceptron) is a structured process of learning from data by adjusting parameters to minimize prediction error.

## Key Concepts

### 1. Labeled Datasets
- **Definition:** Input data paired with expected output data.
- **Scale:** Requires thousands or millions of samples to train effectively.
- **Examples:**
  - **Computer Vision:** Images paired with class labels (e.g., "Cat" or "Dog").
  - **Large Language Models (Transformers):** Partial sentences mapped to the next expected word (e.g., input "To be or..." mapped to output "not").

### 2. Loss Function
- **Purpose:** A mathematical function that evaluates model performance by penalizing incorrect predictions.
- **Goal:** Minimize the loss value to find optimal network parameters.

### 3. Gradient Descent & Learning Rate
- **Gradient Descent:** An optimization algorithm that iteratively moves network parameters toward lower loss (the direction of steepest descent).
- **Learning Rate:** Controls the step size during each iteration.
  - **Too Large:** Risks overshooting the minimum point.
  - **Too Small:** Leads to long convergence times.

### 4. Backpropagation
- **Mechanism:** The standard algorithm for implementing gradient descent efficiently in neural networks.
- **Process:**
  1. **Forward Pass:** Inputs traverse through layers to produce a prediction and calculate error.
  2. **Error Distribution:** Error is propagated backward through the network to assign "blame" to specific neurons.
  3. **Gradient Calculation:** Calculates how much each weight contributed to the total error.
  4. **Weight Update:** Adjusts weights using calculated gradients and the learning rate.

### 5. Model Evaluation (Test Dataset)
- **Holdout/Test Set:** A separate dataset unseen during training.
- **Purpose:** Evaluates generalization capability to ensure accuracy on real-world inputs.