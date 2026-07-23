In this exercise, you will compare the performance of common optimizers (SGD, Adam, and RMSprop) on a small Convolutional Neural Network (CNN) trained on the Fashion-MNIST dataset. You'll set up the data, define the model, implement the training loop, and configure each optimizer to see how they affect training dynamics.

Prerequisites
Familiarity with PyTorch nn.Module.
Understanding of data loading with torchvision.datasets and DataLoader.
Knowledge of the standard PyTorch training loop (forward pass, loss calculation, backpropagation, optimizer step).
Basic understanding of different optimizers like SGD, Adam, and RMSprop.
Instructions
In the cell under the ## Data transforms heading, define the train_tfms and test_tfms variables.
In the cell under ## Data loaders, initialize train_loader, val_loader, and test_loader using torch.utils.data.DataLoader.
Inside the accuracy_from_logits function, complete the logic for calculating accuracy.
Inside the train_one_epoch function, fill in the five standard steps of the training loop.
In the cell under ## Optimizers & hyperparameters, define the optim_cfgs dictionary.
Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-10-implementing-neural-networks-using-pytorch/exercises/starter/
Double-click the optimizer-bakeoff-starter.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To execute terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.



