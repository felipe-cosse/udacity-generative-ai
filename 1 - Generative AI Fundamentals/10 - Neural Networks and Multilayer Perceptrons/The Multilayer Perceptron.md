# Neural Networks and Multilayer Perceptrons - The Multilayer Perceptron

> **Course Context:** Generative AI Fundamentals  
> **Source Module:** Module 10: Neural Networks and Multilayer Perceptrons  
> **Lesson Title:** The Multilayer Perceptron  

---

## Overview

A single perceptron can make a simple decision, but by itself it cannot tell the difference between a cat and a dog from a photo. However, by combining many perceptrons together in layers, we can build a powerful model known as a Multi-Layer Perceptron (MLP) capable of learning intricate patterns from data.

---

## Video Transcript

Let's take a look at what happens when you combine many perceptrons together in layers. 

The multi-layer perceptron is a type of artificial neural network composed of multiple layers of nodes and neurons. Each of these nodes is a perceptron, each performing a simple computation and passing the result to the next layer. 

* The first layer, known as the **input layer**, receives raw data. 
* The final layer or **output layer** produces a network's predictions or decisions. 
* Between these, one or more **hidden layers** perform complex transformations on the data. 

The multi-layer perceptron's power comes from its ability to learn from experience. Each perceptron in the hidden layer is connected to each of the inputs. Each of these connections is associated with a weight, which during training adjusts itself to reduce the number of errors the model makes overall. Each of the neurons in the subsequent layers are connected to each of the neurons in the preceding layer. Each of these weights are also adjusted during training. 

At the end, we often have a number of neurons equal to the number of classes in our problem. One neuron will have the highest value, and that's the one whose class we choose—here, the neuron corresponding to "cat." Through training, which involves updating the many weights in the model to make better guesses on the training dataset, the multi-layer perceptron can learn to make accurate predictions. 

In fact, for large language models, this last layer has a perceptron for each of the tokens a model uses. Running a forward pass of the model will let us know what token it thinks should go next in the completion.

---

## Key Takeaways & Architecture Breakdown

A Multi-Layer Perceptron (MLP) is a type of artificial neural network composed of multiple layers of nodes, also known as neurons. In an MLP, each of these nodes is a perceptron, performing a simple computation and passing its result to the next layer.

The basic structure of an MLP consists of three main types of layers:

### 1. Input Layer
The **Input Layer** is the first layer, which receives the raw input data. For an image classification task, this could be the pixel values of the image.

### 2. Hidden Layers
Between the input and output layers are one or more **Hidden Layers**. These layers are responsible for performing complex transformations on the data, allowing the network to learn increasingly abstract features.

### 3. Output Layer
The **Output Layer** is the final layer, which produces the network's predictions or decisions. In a classification problem like "Cat or Dog?", this layer would output the final prediction.

---

## Training and Inference

The power of an MLP comes from its ability to learn from experience through a process called **training**. 

* Each neuron in a layer is connected to every neuron in the preceding layer. Each of these connections has an associated **weight**, a numerical value that the model adjusts during training.
* By systematically updating these weights, the model learns to minimize the number of errors it makes. This process allows the MLP to learn the complex relationships within the training data.
* At the end of the network, the output layer often has a number of neurons equal to the number of classes in the problem. For example, a "Cat or Dog" classifier has two output neurons. The neuron that produces the highest value "wins," and its corresponding class is chosen as the model's prediction.

### Connection to Large Language Models (LLMs)
This fundamental architecture is a key component in more advanced models. In Large Language Models (LLMs), for instance, the final layer has a neuron for every possible token in the model's vocabulary. When the model generates text, it performs a "forward pass" to determine which token (word or sub-word) has the highest probability of coming next.

---

## Summary Statement
The Multi-Layer Perceptron is a foundational neural network that learns complex patterns by processing data through an input layer, one or more hidden layers, and an output layer, adjusting connection weights during training to make accurate predictions.




Let's take a look at what happens when you combine many perceptrons together in layers. The multi-layer perceptron is a type of artificial neural network composed of multiple layers of nodes and neurons. Each of these nodes is a perceptron, each performing a simple computation and passing the result to the next layer. The first layer, known as the input layer, receives a raw data. The final layer or output layer produces a network's predictions or decisions. Between these, one or more hidden layers perform complex transformations on the data. The multi-layer perceptron's power comes from its ability to learn from experience. Each perceptron in the hidden layer is connected to each of the inputs. Each of these connections is associated with a weight, which during training adjusts itself to reduce the number of errors the model makes overall. Each of the neurons in the subsequent layers are connected to each of the neurons in the preceding layer. Each of these weights are also adjusted during training. At the end, we often have a number of neurons equal to the number of classes in our problem. One neuron will have the highest value, and that's the one whose class we choose. Here, the neuron corresponding to cut one. Through training, which involves updating the many weights in the model to make better guesses on the training dataset, the multi-layer perceptron can learn to make accurate predictions. In fact, for large language models, this last layer has a perceptron for each of the tokens a model uses. Running a forward pass of the model will let us know what token it thinks should go next in the completion.