Choosing the right optimizer can significantly impact your model's training speed and final performance. This demo provides a practical framework for comparing two of the most common optimizers in PyTorch, Stochastic Gradient Descent (SGD) and Adam, by training a simple neural network on the classic MNIST dataset of handwritten digits.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-10-implementing-neural-networks-using-pytorch/demo-comparing-optimizers/
Double-click the demo.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To run terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

First, we'll import the necessary libraries, including torch for building the model, torchvision for the dataset, and matplotlib for plotting our results. We also define a special function, set_seed, to ensure our experiment is reproducible—meaning anyone who runs this code will get the exact same results.

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import random
import numpy as np
import matplotlib.pyplot as plt

# Set a seed for reproducibility
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(1234)
Next, we check if a GPU is available. Training is much faster on a GPU, but this code will fall back to the CPU if one isn't found.

# Select the appropriate device (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
Using device: cpu
Before feeding the images to our model, they need to be in the right format. We define a set of transforms to convert the images into PyTorch tensors and then normalize their pixel values. Normalization helps the model train more efficiently.

# Define the data transforms: convert images to tensors and normalize them
data_transforms = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),  # MNIST-specific mean and std
    ]
)
Now we download the MNIST dataset. We split the original training data into two parts: a larger set for training the model and a smaller validation set. The validation set is used to check the model's performance on data it hasn't been trained on, which helps us monitor for overfitting.

Finally, we create DataLoaders, which are helpers that feed the data to our model in manageable batches.

# Download and load the MNIST training and test datasets
train_ds_full = datasets.MNIST(
    root="./data", train=True, download=True, transform=data_transforms
)
test_ds = datasets.MNIST(
    root="./data", train=False, download=True, transform=data_transforms
)

# Create a validation split from the training set
val_ratio = 0.1
val_size = int(len(train_ds_full) * val_ratio)
train_size = len(train_ds_full) - val_size
train_ds, val_ds = torch.utils.data.random_split(train_ds_full, [train_size, val_size])

print(
    f"Train size: {len(train_ds)}, Val size: {len(val_ds)}, Test size: {len(test_ds)}"
)

# Create DataLoaders to handle batching
batch_size = 64
train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
Train size: 54000, Val size: 6000, Test size: 10000
It's always a good practice to look at your data. A helper function shows us a few sample images and their correct labels, confirming everything has loaded as expected.

A grid of handwritten digits showcasing the numbers 5, 2, 3, 9, 6 in the top row, and 8, 3, 7, 5, 4 in the bottom row, with each digit displayed on a black background and labeled with its corresponding numerical value.
With the data ready, we define our neural network architecture. It's a simple Multi-Layer Perceptron (MLP) with one input layer, one hidden layer with 128 neurons, and an output layer that produces scores (or logits) for each of the 10 possible digits.

# Define a simple Multi-Layer Perceptron (MLP)
class SimpleMLP(nn.Module):
    def __init__(self, input_size=28 * 28, hidden_size=128, num_classes=10):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # Flatten the image from 28x28 to a 784-element vector
        x = torch.flatten(x, 1)
        # Apply ReLU activation after the first layer
        x = F.relu(self.fc1(x))
        # The output of the second layer are the logits
        x = self.fc2(x)
        return x
This small helper function calculates accuracy. It takes the model's output logits, finds the digit with the highest score to get the prediction, and compares it to the true label.

# Function to compute accuracy from model outputs (logits)
@torch.no_grad()
def accuracy_from_logits(logits, y):
    # Get predicted class by finding the index with the highest logit value
    preds = logits.argmax(dim=1)
    # Check if predictions match the true labels
    correct = preds == y
    # Return the mean accuracy for the batch
    return correct.float().mean().item()
The train_one_epoch function contains the core logic for one epoch of training. For each batch of data, it performs five essential steps:

Zeros out old gradients.
Makes a prediction (forward pass).
Calculates the loss.
Computes new gradients with backpropagation (backward pass).
Updates the model's weights using the optimizer.
# Function for a single training epoch
def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()  # Set model to training mode
    running_loss, running_acc, n = 0.0, 0.0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)

        # 1. Zero the gradients
        optimizer.zero_grad()
        # 2. Get model predictions (forward pass)
        logits = model(x)
        # 3. Calculate the loss
        loss = criterion(logits, y)
        # 4. Compute gradients (backward pass)
        loss.backward()
        # 5. Update model weights
        optimizer.step()
        
        # ... update stats ...
        batch_size = x.size(0)
        running_loss += loss.item() * batch_size
        running_acc += accuracy_from_logits(logits, y) * batch_size
        n += batch_size
        
    return running_loss / n, running_acc / n
The evaluate function is similar but runs without calculating gradients or updating weights. Its only job is to measure the model's loss and accuracy on a given dataset, like our validation set.

# Function to evaluate the model on validation or test data
@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()  # Set model to evaluation mode
    total_loss, total_acc, n = 0.0, 0.0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = criterion(logits, y)
        
        # ... update stats ...
        batch_size = x.size(0)
        total_loss += loss.item() * batch_size
        total_acc += accuracy_from_logits(logits, y) * batch_size
        n += batch_size

    return total_loss / n, total_acc / n
Now we get to the main event: the "Optimizer Bake-Off." We set up the experiment by defining our loss function (CrossEntropyLoss), creating a dictionary with configurations for our two contenders (SGD and Adam), and writing helper functions to create a fresh model and the correct optimizer for each run.

# Loss function for classification
criterion = nn.CrossEntropyLoss()

# Function to create a new model instance for each experiment
def make_fresh_model():
    return SimpleMLP().to(device)

# Define the optimizer configurations we want to compare
optim_configs = {"sgd": {"lr": 1e-2, "momentum": 0.9}, "adam": {"lr": 1e-3}}

# Helper function to create an optimizer for a given model
def make_optimizer(name, params):
    if name == "sgd":
        return optim.SGD(params, **optim_configs["sgd"])
    if name == "adam":
        return optim.Adam(params, **optim_configs["adam"])
    raise ValueError("Unknown optimizer")
This is our main training loop. We iterate through our two optimizers, SGD and Adam. For each one, we reset the random seed for a fair comparison, create a new model, and train it for three epochs. After each epoch, we record the training and validation loss and accuracy.

# Main training loop to compare optimizers
EPOCHS = 3
histories = {}

for opt_name in ["sgd", "adam"]:
    print(f"\n=== Training with {opt_name.upper()} ===")
    set_seed(1234)  # Reset seed for a fair comparison
    model = make_fresh_model()
    optimizer = make_optimizer(opt_name, model.parameters())

    # Store metrics for this run
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, EPOCHS + 1):
        # Train for one epoch
        tl, ta = train_one_epoch(model, train_loader, criterion, optimizer, device)
        # Evaluate on the validation set
        vl, va = evaluate(model, val_loader, criterion, device)

        # Save metrics
        history["train_loss"].append(tl)
        history["train_acc"].append(ta)
        history["val_loss"].append(vl)
        history["val_acc"].append(va)

        print(
            f"Epoch {epoch:02d} | train loss {tl:.4f} acc {ta:.4f} | val loss {vl:.4f} acc {va:.4f}"
        )

    histories[opt_name] = history

print("\nDone training all optimizers.")
=== Training with SGD ===
Epoch 01 | train loss 0.2941 acc 0.9137 | val loss 0.1680 acc 0.9495
Epoch 02 | train loss 0.1245 acc 0.9626 | val loss 0.1247 acc 0.9652
Epoch 03 | train loss 0.0869 acc 0.9747 | val loss 0.1030 acc 0.9682

=== Training with ADAM ===
Epoch 01 | train loss 0.2706 acc 0.9212 | val loss 0.1612 acc 0.9520
Epoch 02 | train loss 0.1207 acc 0.9641 | val loss 0.1271 acc 0.9625
Epoch 03 | train loss 0.0832 acc 0.9751 | val loss 0.1059 acc 0.9675

Done training all optimizers.
With training complete, we plot the validation accuracy for both optimizers. This chart gives us a clear visual comparison of how effectively each optimizer helped the model learn.

Line graph comparing validation accuracy over epochs for two optimizers: SGD (blue line) and Adam (orange line). The x-axis represents epochs, ranging from 1 to 3, while the y-axis represents validation accuracy, ranging from 0.950 to 0.968. The graph shows that Adam consistently outperforms SGD in validation accuracy throughout the epochs.
Finally, we identify the best-performing optimizer based on the validation accuracy we just plotted. We then retrain a final model from scratch using only that winning optimizer and evaluate its performance on the completely unseen test set. This gives our final, unbiased measure of how well our model can generalize to new data.

# Find the best optimizer based on the highest validation accuracy
best_name = max(histories.keys(), key=lambda n: max(histories[n]["val_acc"]))
print(f"Best optimizer by validation accuracy: {best_name.upper()}")

# Retrain the model with the best optimizer and evaluate on the test set
print("\nTraining final model...")
set_seed(1234)
best_model = make_fresh_model()
best_opt = make_optimizer(best_name, best_model.parameters())

for epoch in range(EPOCHS):
    train_one_epoch(best_model, train_loader, criterion, best_opt, device)

# Final evaluation on the unseen test set
test_loss, test_acc = evaluate(best_model, test_loader, criterion, device)
print(f"\nFinal Test Accuracy with {best_name.upper()}: {test_acc:.4f}")
Best optimizer by validation accuracy: SGD

Training final model...

Final Test Accuracy with SGD: 0.9717
This demo shows how to systematically compare training optimizers in PyTorch to determine which one yields better performance for a given model and dataset.







This demo, we're going to run a simple experiment to compare two different training optimizers in PyTorch. We will build a basic neural network, train it on the classic MNIST handwritten digit dataset, and see whether the SGD or Adam optimizer gives us better results. First things first, we'll begin with our imports and setup. Here, we import all the necessary libraries, including torch for building the model, torch vision for the dataset, and matplot.lib for plotting our results. We also define and call a special function, set_seed. This is important because it ensures that anyone who runs his code gets the exact same results, making our experiment reproducible. Next, we check if a GPU is available for use. Training a neural network is much faster on a GPU. Now we move on to preparing our data. Before we can feed the images to our model, they need to be in the right format. We define a set of transforms to first convert the images into PyTorch tensors and then normalizer pixel values. Normalization helps the model train more efficiently. In this cell, we download the MNIST data set. We then split the original training data into two parts, a larger set for training the model and a smaller validation set. The validation set is used to check the model's performance on data it hasn't been trained on during the training process. Finally, we create data loaders, which are helpers that feed the data to our model in manageable batches. It's always a good practice to look at your data. This helper function shows us a few sample images from our training set along with their correct labels, just to confirmed that everything has loaded as expected. With our data ready, it's time to build the components for training the model itself in some utility functions for calculating metrics and running the training process. Here, we define our neural network architecture. It's a simple multi-layer perceptron or MLP. It has one input layer that takes a flat in 28 by 28 pixel image, one hidden layer with 120 neurons and an output layer that produces scores or logits for each of the 10 possible digits. This is a small helper function to calculate accuracy. It takes a models output logits, finds a digit with the highest score to get the prediction, and then compares it to the true label to see if the model was correct. This cell contains a core logic for one epic of training. For each batch of data, it performs five essential steps of training a model. It zeros out old gradients, makes a prediction, calculates a loss, computes new gradients with back propagation, and finally, updates some models weights using the optimizer. The evaluate function is very similar to the training function. The key difference is that it runs without calculating gradients or updating the models weights. Its only job is to measure the model's loss and accuracy on a given dataset, like a validation or test set. Now we get to the main event of this notebook, the optimizer bake off. Here, we set up the experiment. We define our loss function, which is cross entropy loss. Since this is a multi class classification problem, we also create a dictionary that holds the configurations for our two contenders, SGD with a specific learning rate and momentum, and Adam with its own learning rate. The helper functions make it easy to create a fresh model and the correct optimizer for each run. This is our main training loop. We iterate through our two optimizers, SGD, and Adam. For each one, we reset the random C to ensure reproducibility. We create a new model and train it for three epics. In each epic, we record the training and validation loss and accuracy. With a training complete for both optimizers, let's look at the results and perform a final evaluation. A picture is worth 1,000 words. Here, we plot to validation accuracy for both SGD and Adam across the three training epics. This chart gives us a clear visual comparison of how quickly and effectively each optimizer helped the model learn. Finally, we identify the best performing optimizer based on the validation accuracy we just plotted. We then create one last model, train it from scratch using only that winning optimizer and evaluate its performance on the completely unseen test set. This gives our final unbiased measure of how well our model can generalize to new data.