"""
Script to create a sample PDF for testing AI Study Buddy.
Run once: python create_sample_pdf.py
"""

from fpdf import FPDF

def create_sample_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Page 1: Introduction to Machine Learning
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, "Introduction to Machine Learning", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, """
Machine Learning is a subset of artificial intelligence (AI) that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves.

The process begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future based on the examples that we provide.

Key Concepts:

1. Supervised Learning: The algorithm learns from labeled training data and makes predictions. Example algorithms include Linear Regression, Decision Trees, and Neural Networks.

2. Unsupervised Learning: The algorithm finds patterns in unlabeled data. Example algorithms include K-Means Clustering and Principal Component Analysis (PCA).

3. Reinforcement Learning: The algorithm learns by interacting with an environment and receiving rewards or penalties. This is how AlphaGo learned to play Go.
""")
    
    # Page 2: Neural Networks
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "Chapter 2: Neural Networks", ln=True)
    
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, """
Neural Networks are computing systems inspired by the biological neural networks in the human brain. They consist of layers of interconnected nodes or "neurons" that process information.

Structure of a Neural Network:

- Input Layer: Receives the initial data
- Hidden Layers: Process the data through weighted connections  
- Output Layer: Produces the final result

Each connection has a weight that adjusts during training. The network learns by:
1. Making predictions (forward propagation)
2. Calculating error (loss function)
3. Adjusting weights (backpropagation)

Types of Neural Networks:

- Feedforward Neural Networks (FNN): Data flows in one direction
- Convolutional Neural Networks (CNN): Excellent for image processing
- Recurrent Neural Networks (RNN): Good for sequential data like text
- Transformers: The architecture behind GPT and modern language models

Training Tips:
- Use dropout to prevent overfitting
- Normalize your input data
- Start with a small learning rate
- Monitor validation loss to detect overfitting
""")
    
    # Page 3: Practical Applications
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "Chapter 3: Real-World Applications", ln=True)
    
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, """
Machine Learning is transforming many industries:

Healthcare:
- Disease diagnosis from medical images
- Drug discovery and development
- Personalized treatment recommendations

Finance:
- Fraud detection in transactions
- Algorithmic trading
- Credit risk assessment

Transportation:
- Self-driving vehicles
- Route optimization
- Predictive maintenance

Natural Language Processing:
- Machine translation
- Sentiment analysis
- Chatbots and virtual assistants

Getting Started with ML:

1. Learn Python programming
2. Study statistics and linear algebra
3. Practice with datasets from Kaggle
4. Start with scikit-learn library
5. Progress to deep learning with PyTorch or TensorFlow

Remember: Machine learning is about finding patterns in data. The more quality data you have, the better your models will perform!
""")
    
    pdf.output("sample.pdf")
    print("Created sample.pdf successfully!")

if __name__ == "__main__":
    create_sample_pdf()
