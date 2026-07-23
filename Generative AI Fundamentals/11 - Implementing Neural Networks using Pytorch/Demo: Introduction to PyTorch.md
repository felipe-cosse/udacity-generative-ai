PyTorch is a foundational tool for machine learning, acting like a mechanic's toolbox for building and training models. This lesson provides a hands-on tour of PyTorch's core components, giving you a solid foundation to construct everything from simple regressions to complex neural networks.

Accessing the Workspace
Follow these steps to access and run the notebook.

Access the Vocareum workspace from the cloud resources tab.
In the file explorer on the left, navigate to the following directory: cd13303-genai-c1-classroom/module-10-implementing-neural-networks-using-pytorch/demo-intro-pytorch/
Double-click the pytorch_demo.ipynb file to open it.
Click "Select Kernel" in the top-right corner.
Select Jupyter Kernel from the dropdown menu options.
Select Python (venv1) from the list.
If the kernel is not listed, click the refresh icon at the top of the kernel menu.
You are now ready to run the code!

To run terminal commands, activate the pre-configured virtual environment:

source /voc/data/venv1/bin/activate
You can also access this notebook on GitHub here(opens in a new tab).

Important: When you are done, click on "End Lab" to avoid wasting your limited GPU resources.

This walkthrough covers the fundamental building blocks of PyTorch: Tensors, Neural Networks, Loss Functions, Optimizers, Data Handlers, and the Training Loop.

First, let's explore PyTorch Tensors, the core data structure in PyTorch. Think of them as multi-dimensional arrays, similar to vectors or matrices. We'll start by creating a 3D tensor to represent four 28x28 grayscale images filled with random noise and then access the second image.

import torch
import matplotlib.pyplot as plt

images = torch.rand(4, 28, 28)
# To access the second image
second_image = images[1]
print(second_image)
To visualize one of these images, we can use the matplotlib library. The imshow function is perfect for displaying a 2D tensor as an image. Since we generated the tensor with random numbers, the resulting image is just noise, as expected.

plt.imshow(second_image, cmap='gray')
plt.show()
[IMAGE_PLACEHOLDER: Screengrab of the grayscale random noise image plot]

PyTorch tensors support all the standard operations you might know from linear algebra. For example, let's take a 2x2 matrix A and calculate its first four powers using matrix multiplication.

A = torch.tensor([[1, 1], [1, 0]], dtype=torch.float32)
print("A^1:\\n", torch.matrix_power(A, 1))
print("A^2:\\n", torch.matrix_power(A, 2))
print("A^3:\\n", torch.matrix_power(A, 3))
print("A^4:\\n", torch.matrix_power(A, 4))
Next, we'll build a simple neural network using PyTorch's torch.nn module. The simplest form is a Multi-Layer Perceptron (MLP), which consists of an input layer, an output layer, and one or more hidden layers. Here, we define an MLP with one hidden layer.

import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_size):
        super(MLP, self).__init__()
        self.hidden_layer = nn.Linear(input_size, 64)
        self.activation = nn.ReLU()
        self.output_layer = nn.Linear(64, 2)

    def forward(self, x):
        x = self.hidden_layer(x)
        x = self.activation(x)
        x = self.output_layer(x)
        return x
We can instantiate this model with an input size of 10 and print its structure.

model = MLP(input_size=10)
print(model)
To test the model's forward method, we pass it a random vector of length 10. As defined in our output layer, the model returns a vector of length 2.

input_vector = torch.randn(10)
output = model(input_vector)
print(output)
Loss functions are crucial for training, as they measure the difference between a model's prediction and the actual target. Let's look at two common types. First, Cross-Entropy Loss, which is used for classification tasks. A lower loss indicates a more confident and correct prediction.

cross_entropy_loss = nn.CrossEntropyLoss()
target = torch.tensor([1]) # 0 for cats, 1 for dogs. Label is for dog.

# Case 1: Prediction is more likely a dog (correct)
predicted1 = torch.tensor([[2.0, 5.0]])
loss1 = cross_entropy_loss(predicted1, target)
print(f"Loss when prediction is more likely a dog: {loss1.item():.4f}")

# Case 2: Prediction is more likely a cat (incorrect)
predicted2 = torch.tensor([[1.5, 1.1]])
loss2 = cross_entropy_loss(predicted2, target)
print(f"Loss when prediction is more likely a cat: {loss2.item():.4f}")
Second, Mean Squared Error (MSE) Loss is used for regression problems, where the goal is to predict a continuous value like a house price.

mse_loss = nn.MSELoss()
predicted_price = torch.tensor([320000.0])
actual_price = torch.tensor([300000.0])
loss = mse_loss(predicted_price, actual_price)
print(f"MSE Loss: {loss.item()}")
After calculating the loss, an optimizer adjusts the model's parameters to minimize it. Stochastic Gradient Descent (SGD) and Adam are two popular optimizers in PyTorch.

from torch.optim import SGD, Adam

# Assuming 'model' is our MLP defined earlier
optimizer_sgd = SGD(model.parameters(), lr=0.01, momentum=0.9)
print("SGD Optimizer instantiated.")

optimizer_adam = Adam(model.parameters(), lr=0.01)
print("Adam Optimizer instantiated.")
To manage data efficiently, PyTorch uses Dataset and DataLoader classes. A Dataset class provides a standard way to access data, while a DataLoader wraps the dataset to provide batched, shuffled, and parallelized data loading. Let's create a custom dataset that returns pairs of numbers and their products.

from torch.utils.data import Dataset, DataLoader

class NumberProductDataset(Dataset):
    def __init__(self, data_range):
        self.data = [(i, i + 1, i * (i + 1)) for i in range(data_range)]

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

dataset = NumberProductDataset(data_range=11)
sample = dataset[3] # pick the 4th element (index 3)
print(f"Input: {sample[0]}, {sample[1]}, Output: {sample[2]}")
Now, we can use a DataLoader to iterate over this dataset in shuffled batches of a specified size.

dataloader = DataLoader(dataset, batch_size=3, shuffle=True)
for i, (input1, input2, output) in enumerate(dataloader):
    print(f"Batch {i+1}:")
    print(f"  Inputs 1: {input1}")
    print(f"  Inputs 2: {input2}")
    print(f"  Outputs: {output}")
Finally, let's bring all these components together in a complete training loop. Our goal is to train a model to add two numbers. First, we define a dataset for this task.

class NumberSumDataset(Dataset):
    def __init__(self, data_range):
        self.data = []
        for i in range(data_range):
            for j in range(data_range):
                self.data.append(([i, j], i + j))

    def __getitem__(self, idx):
        return torch.tensor(self.data[idx][0], dtype=torch.float32), torch.tensor(self.data[idx][1], dtype=torch.float32)

    def __len__(self):
        return len(self.data)
Next, we define an MLP architecture suited for this addition task, with an input layer for two numbers and an output layer for their sum.

class SumMLP(nn.Module):
    def __init__(self):
        super(SumMLP, self).__init__()
        self.hidden_layer = nn.Linear(2, 128)
        self.activation = nn.ReLU()
        self.output_layer = nn.Linear(128, 1)

    def forward(self, x):
        x = self.hidden_layer(x)
        x = self.activation(x)
        x = self.output_layer(x)
        return x
We instantiate all the necessary components for our training loop.

sum_dataset = NumberSumDataset(data_range=10)
sum_dataloader = DataLoader(sum_dataset, batch_size=10, shuffle=True)
sum_model = SumMLP()
loss_function = nn.MSELoss()
optimizer = Adam(sum_model.parameters(), lr=0.01)
Now we execute the training loop for 20 epochs. In each epoch, we iterate through batches of data, make predictions, calculate the loss, perform backpropagation, and update the model's weights. Notice how the loss decreases over time, indicating that the model is learning.

num_epochs = 20
for epoch in range(num_epochs):
    epoch_loss = 0.0
    for inputs, targets in sum_dataloader:
        optimizer.zero_grad()
        predictions = sum_model(inputs)
        loss = loss_function(predictions.squeeze(), targets)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss/len(sum_dataloader):.4f}")
With the model trained, let's test it on new numbers it hasn't seen before, like 3 and 7.

test_input = torch.tensor([3.0, 7.0])
prediction = sum_model(test_input)
print(f"Prediction for 3 + 7: {prediction.item():.1f}")
The model correctly predicts the sum, demonstrating that by combining PyTorch's core components, we can successfully build and train a functional machine learning model from scratch.






Let's talk about PyTorch. PyTorch is a key tool for machine learning, providing all the components you need to build and train models. In this lesson, we'll walk through the core concepts to give you a solid foundation. We'll start with PyTorch tensors, which are the fundamental data structures. It will cover how to build neural nets, define loss functions, and optimizers, and manage data with data sets and data loaders. Finally, we'll combine everything into a complete training loop. Let's begin with tensors. Think of them as multidimensional arrays, like vectors or matrices. Here, we're using torch.rand to create a 3D tensor, representing(4, 28, 28) pixel gray-scale images. We then access a second image in the tensor and print its values. To visualize one of these images, we can use a library called Matplotlib. The imshow function is perfect for displaying a 2D tensor as and image. Here, we use imshow to display the second image tensor. Since we created the tensor with random numbers, the resulting image is just random noise as we'd expect. PyTorch tensors support all the standard operations you might be familiar with from linear algebra. For example, let's take a 2 by 2 matrix and calculate its powers using matrix multiplication. We define a 2x2 tensor named A. Then we use a torch.matrix_power function to compute and print the first, second, third and fourth powers of A. Now let's move on to building neural nets using PyTorch's nn.Module. A neural network is a system of interconnected nodes. We'll build a simple one called a Multi-Layer Perceptron or MLP with one hidden layer. Here, we define our MLP architecture as a Python class. It has a hidden layer, a ReLU activation function, and an output layer. The forward method defines the path that it takes as it flows through the network. Now that we have our models blueprint, we can create an instance of it. We'll specify that our model should accept an input of size 10. We create the model and print it. This shows us a summary of the layers we defined, including the number of input and output features for each linear layer. We create a random vector of length 10 and pass to our model. As you can see, the model returns a vector of length two, which matches the size of the output layer we defined. Next, let's discuss loss functions. A loss function measures a difference between our models prediction and the correct answer. This measurement guides the model's training. We'll look at two common types, Cross-Entropy for classification and Mean Squared Error for regression. This is an example of cross-entropy loss and a classification task. Notice that when the models prediction is confident and correct, the loss is low. When the prediction is wrong, the loss is much higher. Mean Squared Error or MSE is used for regression tasks, where the goal is to predict a continuous value, like the price of a house. Here, we calculate the MSE loss for a house price prediction. The model predicts 320,000 units, but the actual price is 300,000 units. The MSE loss is a square of this difference. After calculating the loss, we need an optimizer to adjust the model's internal parameters to minimize that loss. Stochastic Gradient Descent or SGD is a popular optimization algorithm. Here, we instantiate two common optimizers, SGD and Adam. We provide them with the models parameters and a learning rate, which controls the size of the adjustments made during training. To manage our data effectively, PyTorches provides a dataset and data loader classes. Data set provides a standard way to access data, while data loader helps organize that data into shuffled batches for efficient training. In this cell, we create a custom data set that generates pairs of numbers in their products. We define how to get the length of the dataset and how to retrieve a specific item bytes index. Now we'll use a data loader to manage our custom dataset. We can tell the data loader to group our data into batches of a specific size and to shuffle the data before each training epic. We create a data loader with a batch size of three. When we loop through it, it gives us shuffled batches of data. You can see the inputs and outputs for four different batches here. We've now covered all the individual components. It's time to bring them all together in a complete training loop to train a model from scratch. First, we'll create a simple dataset for a new task, teaching a model how to add two numbers. This NumberSumDataset will provide a model with pairs of numbers and their corresponding sums. Next, we'll define a new MLP that is suitable for addition task. It will need to accept two numbers as input and produce a single number as output. Here is an architecture for our sum MLP. It has an input layer for two numbers, a hidden layer with 128 nodes, and an output layer that produces a single value representing the predicted sum. We're almost ready to train. This next cell just gathers all the components we built into one place. Here, we instantiate everything we need. Our NumberSumDataset and DataLoader, our SumMLP model, the MSE loss function, and the Adam optimizer. And now for the main event, the training loop. We run the training process for 20 epochs, and then each epic, we loop through our data in batches. For each batch, we make predictions, calculate the loss, and use a optimizer to update the model. As you can see from the output, the loss decreases significantly over time, which means our model is learning. Now that the model is trained, let's test it with some new numbers it hasn't seen before, like three and seven. We pass a tensor containing three and seven to our train model, and the prediction is 10.0, which is a correct sum. Success. You now have a foundational understanding of the core concepts of PyTorch. This knowledge equips you to start building and training your own powerful machine learning models.