Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-10-implementing-neural-networks-using-pytorch/exercises/solution/
Double-click the optimizer-bakeoff-solution.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

First, we define a simple data transformation pipeline. This pipeline converts the Fashion-MNIST images into PyTorch tensors and then normalizes their pixel values to have a mean and standard deviation of 0.5, which helps the model train more effectively.

# <<< START SOLUTION SECTION
train_tfms = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)
test_tfms = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)
# >>> END SOLUTION SECTION
Next, we create DataLoader objects for the training, validation, and test datasets. These loaders will efficiently feed the data to our model in batches, with shuffling enabled for the training set to improve generalization.

# ... (Dataset loading and splitting code is omitted)

# <<< START SOLUTION SECTION
train_loader = DataLoader(
    train_ds, batch_size=128, shuffle=True, num_workers=2, pin_memory=True
)
val_loader = DataLoader(
    val_ds, batch_size=128, shuffle=False, num_workers=2, pin_memory=True
)
test_loader = DataLoader(
    test_ds, batch_size=128, shuffle=False, num_workers=2, pin_memory=True
)
# >>> END SOLUTION SECTION
To measure model performance, we implement the accuracy_from_logits function. It takes the model's raw outputs (logits), determines the predicted class by finding the index with the highest score using argmax, and then compares these predictions to the true labels to calculate the accuracy.

@torch.no_grad()
def accuracy_from_logits(logits, y):
    # ...
    # <<< START SOLUTION SECTION
    # Use argmax to get predicted class
    preds = logits.argmax(dim=1)

    # Get boolean tensor of correct predictions, hint: use ==
    correct = preds == y
    # >>> END SOLUTION SECTION

    # Return mean accuracy of the batch
    return correct.float().mean().item()
The core of the training logic is in the train_one_epoch function. Here, we implement the standard PyTorch training loop for a single epoch: zeroing the gradients, performing a forward pass, calculating the loss, running backpropagation, and updating the model's weights with the optimizer.

def train_one_epoch(model, loader, criterion, optimizer, device):
    # ...
    for x, y in loader:
        # ...
        # <<< START SOLUTION SECTION
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        # >>> END SOLUTION SECTION
        # ... (stats calculation is omitted)
To compare the different optimizers, we define their specific hyperparameters in a dictionary. This allows us to easily configure and instantiate SGD, Adam, and RMSprop with appropriate settings like learning rate, momentum, and weight decay.

# ... (helper functions are omitted)

# <<< START SOLUTION SECTION
optim_cfgs = {
    "sgd": {"lr": 1e-2, "momentum": 0.9, "weight_decay": 1e-4},
    "adam": {"lr": 1e-3, "betas": (0.9, 0.999), "weight_decay": 1e-4},
    "rmsprop": {"lr": 1e-3, "alpha": 0.99, "weight_decay": 1e-4},
}
# >>> END SOLUTION SECTION
After running the main training loop, which trains a fresh model with each optimizer for 3 epochs, we can see the performance metrics printed for each step.

=== Training with SGD ===
Epoch 01 | train loss 0.7335 acc 0.7402 | val loss 0.4451 acc 0.8365
Epoch 02 | train loss 0.4072 acc 0.8516 | val loss 0.3752 acc 0.8608
Epoch 03 | train loss 0.3572 acc 0.8695 | val loss 0.3579 acc 0.8647

=== Training with ADAM ===
Epoch 01 | train loss 0.5576 acc 0.8002 | val loss 0.3981 acc 0.8593
Epoch 02 | train loss 0.3652 acc 0.8684 | val loss 0.3469 acc 0.8733
Epoch 03 | train loss 0.3206 acc 0.8844 | val loss 0.3165 acc 0.8818

=== Training with RMSPROP ===
Epoch 01 | train loss 0.5412 acc 0.8004 | val loss 0.4018 acc 0.8527
Epoch 02 | train loss 0.3637 acc 0.8680 | val loss 0.3497 acc 0.8718
Epoch 03 | train loss 0.3158 acc 0.8840 | val loss 0.3050 acc 0.8838

Done training all optimizers.
The results are then visualized by plotting the validation accuracy over the epochs. This graph clearly shows that the adaptive optimizers, Adam and RMSprop, learn faster and achieve higher accuracy than standard SGD in this short training run.

Finally, we select the best-performing optimizer based on validation accuracy (RMSprop in this case), retrain a model with it from scratch, and report its performance on the unseen test set.

Best by val acc: rmsprop
Test accuracy with RMSPROP: 0.8889
Key Takeaway
This exercise demonstrates that adaptive optimizers like Adam and RMSprop often converge faster and achieve better performance than standard SGD, highlighting the significant impact of optimizer choice on model training dynamics.







