# CipherMetrics | Cryptographic Algorithm Performance Analyzer

CipherMetrics is a collaborative academic project developed by [Resul-aliyev](https://github.com/Resul-aliyev) and [EgeTank](https://github.com/EgeTank) using Python.

It is an interactive cryptographic algorithm comparison and asymptotic analysis tool designed to evaluate how different encryption algorithms perform under varying input sizes.

Through a live, Matrix-themed dashboard, the project analyzes execution time, CPU workload, and computational complexity.

Beyond comparing encryption algorithms, CipherMetrics brings together cryptography, mathematical analysis, algorithm optimization, and performance visualization.

## Features

- **Live Dashboard:** Interactive dashboard built with Streamlit and Plotly.
- **Dummy Data Generation:** Generates random data payloads ranging from 1 MB to 10 MB for performance testing.
- **Algorithm Comparison:** Compares Affine Cipher, AES-256-CTR, and educational RSA implementations.
- **Performance Monitoring:** Measures execution time and monitors CPU usage using psutil.
- **Visual Analytics:** Displays encryption performance through interactive charts and result tables.
- **Modular Exponentiation:** Demonstrates the performance difference between standard modular exponentiation and optimized binary exponentiation.

## Cryptographic Algorithms

The project includes the following implementations:

- **Affine Cipher:** A classical encryption method based on modular arithmetic.
- **AES-256-CTR:** A modern symmetric encryption algorithm.
- **RSA:** An educational implementation demonstrating asymmetric encryption principles.

## Mathematical Analysis & Optimization

An important aspect of this project is understanding the relationship between mathematical operations and computational performance.

- **O(n) – Linear Complexity:** Examines how processing time increases with input size in operations such as Affine Cipher encryption.
- **O(n log e) – RSA:** Illustrates the computational cost of modular exponentiation across input elements.
- **O(log e) – Binary Exponentiation:** Demonstrates how repeated squaring and bitwise operations reduce the number of modular multiplication operations.

The project also explores Fermat's Little Theorem and its application in modular arithmetic under appropriate mathematical conditions.

## My Perspective & Contribution

My main interest in this project was exploring the mathematical foundations behind computational efficiency and understanding how theoretical concepts influence practical algorithm performance.

For me, comparing algorithms is not just about identifying which one runs faster. It is also about understanding **why an algorithm performs differently, how its mathematical structure affects execution time, and how optimization changes computational cost.**

My contributions focused on the mathematical and theoretical aspects of the project:

- Prepared a separate mathematical presentation for the project.
- Researched and explained algorithmic time complexity and asymptotic analysis.
- Explored modular exponentiation and Fermat's Little Theorem.
- Analyzed the relationship between mathematical operations and computational performance.
- Presented the theoretical differences between standard and optimized algorithms.

Working on this project strengthened my interest in cryptography, algorithm optimization, mathematical computing, and the connection between theoretical knowledge and practical software development.

## Built With

- Python
- Streamlit
- Plotly
- Pandas
- Cryptography
- psutil
- HTML, CSS & JavaScript

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Resul-aliyev/CipherMetrics.git
cd CipherMetrics
```

### 2. Install dependencies

```bash
pip install streamlit psutil pandas plotly cryptography
```

### 3. Run the application

```bash
python -m streamlit run CipherMetrics.py
```

## Project Collaboration

Developed collaboratively in 2025 with [EgeTank](https://github.com/EgeTank) as an academic project.

Both contributors participated in the development and presentation of the project, combining software development and mathematical analysis.

**Collaborator:** [EgeTank – GitHub Profile](https://github.com/EgeTank)

**Original Project Repository:** [EgeTank/CipherMetrics](https://github.com/EgeTank/CipherMetrics)

## Disclaimer

This project is intended for educational and performance comparison purposes.

The RSA implementation is a simplified textbook demonstration and is not suitable for real-world security applications.
