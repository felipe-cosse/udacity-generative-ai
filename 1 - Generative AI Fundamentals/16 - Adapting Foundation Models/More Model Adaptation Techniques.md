Large language models can often be too big or slow to run efficiently on specific hardware. To solve this, we can use techniques to adapt and optimize them for deployment. This involves either making the model itself smaller and faster through compression or extending its capabilities by equipping it with external tools.

Model compression includes various techniques designed to reduce a model's size, making it more efficient, faster, and cheaper for deployment and inference while retaining much of its original utility.

Overview of techniques for optimizing language learning models: Distillation involves training a student model from a teacher model; Quantization converts model weights to lower numerical precision (e.g., from 32-bit to 4-bit); Pruning removes less important parameters or sets them to zero. An illustration features a large robot interacting with a smaller robot, indicating a teaching dynamic.
Model compression.

Key approaches to model compression include:

Distillation: Also known as knowledge distillation, this process involves training a smaller "student" model to mimic the behavior of a larger, more complex "teacher" model. The core idea is to distill the knowledge from the powerful teacher into a more compact student, resulting in a smaller, faster model with comparable performance.

Quantization: This is a compression technique that converts a model's weights and activations to a lower numerical precision. For example, converting parameters from 32-bit floating-point numbers to 8-bit integers can drastically reduce the model's memory footprint and increase its throughput.

Pruning: This technique involves removing less important parameters within a neural network or setting their values to zero. While this doesn't necessarily reduce the total parameter count, it reduces the number of non-zero parameters, leading to sparser models. Pruned models require less storage and can potentially speed up computation. However, pruning is currently less common in practice than other methods due to implementation complexity and varying performance boosts.

Another approach to model adaptation involves extending a model's capabilities using agentic AI and tools. A core characteristic of agentic AI is tool use, where AI agents are equipped with an inventory of tools that vastly extend what an LLM can do on its own.

A cartoon robot with a friendly expression typing on a calculator, accompanied by bullet points highlighting its capabilities: knowledge augmentation including vector and web search, capability extension for tools like calculators and time zone converters, and writing actions such as sending emails and placing orders.
Tools for Model Adaptation

These tools can be categorized as follows:

Knowledge augmentation: These tools provide the model with access to external data. Examples include retrievers for vector databases in RAG systems, web search capabilities, or APIs for internal company systems. A simple RAG system can be seen as a basic agent with a retrieval tool.

Capability extension: These tools overcome the inherent limitations of LLMs. For instance, since LLMs often struggle with complex math, a calculator can be provided as a tool. Other examples include time zone converters or code interpreters.

Write actions: These are tools that allow the agent to make changes to an external environment. This could include sending emails, placing orders, or updating databases. Using these tools requires careful consideration of security, reliability, and ethics, especially when agents have access to write actions or sensitive data.

Models can be adapted for specific applications by using compression techniques like distillation and quantization to make them smaller, or by using agentic tools to extend their knowledge and capabilities.







Now, let's consider another use case. Say the model is too big to run on our target hardware, or it simply is too slow. We can go through a process called model compression, which makes a model smaller while retaining much of its original utility. Model compression encompasses techniques designed to reduce a model size, making it more efficient, faster and cheaper for deployment and inference. Key approaches include model distillation, also known as knowledge distillation. This involves training a smaller student model to mimic the behavior of a larger teacher model. The core idea is to distill the knowledge from the powerful, often complex teacher into a more compact student. This results in smaller, faster and more efficient models that can retain performance comparable to the teacher. Quantization is a compression technique that converts models weights and activations to a lower numerical precision. For example, converting from 32-bit floating point to 8-bit integers can drastically reduce the model's memory footprint and increase its throughput. Pruning involves removing less important parameters or setting them to zero within a neural network. This doesn't necessarily reduce a total parameter count, but it can reduce the number of non zero parameters leading to sparser models. Prune models require less storage and can potentially speed up computation. While promising in research, pruning is currently less common in practice than other compression methods, partly due to implementation complexity and varying performance boosts. Last, we look at one of the newer developments in model adaptation. That is the use of Agentic AI. A core characteristic of Agentic AI is tool use. Agents are equipped with a tool inventory that vastly extends their capabilities beyond what a large language model can do alone. These tools can include knowledge augmentation. This means retrievers for external data like vector databases and RAG systems, web search or APIs for internal systems. Note that RAG itself can be seen as a simple agent with retrieval tools. Capability extension. Here we have calculators as LLMs often struggle with complex math, time zone converters or code interpreters. Write actions, tools that allow the agent to make changes to an environment, such as sending emails, placing orders, or updating databases, while powerful, careful consideration of security, reliability, and ethical use is critical, especially when agents have access to write actions or sensitive data.