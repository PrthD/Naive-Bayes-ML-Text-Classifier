
# Naive Bayes ML Text Classifier

A Python-based machine learning classifier designed to analyze input text files using a Naive Bayes approach. The project applies object-oriented programming principles to build a flexible and reusable text classification system. It processes text from input files and classifies it based on predefined target words, making it ideal for natural language processing (NLP) tasks.

## Features

- **Naive Bayes Classifier**: Implements a Naive Bayes approach for classifying text based on word occurrences.
- **Object-Oriented Design**: Uses object-oriented principles for flexibility, readability, and easy maintenance.
- **File Input Processing**: Reads text from a file or standard input to perform classification.
- **Target Word Matching**: Analyzes text to identify and classify based on target words related to weather, seasons, and other environmental themes.
- **Error Handling**: Handles file input errors, such as missing files or OS-related issues, gracefully.

## Installation

Ensure that Python 3 is installed on your system. No additional external dependencies are required for this project.

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/naive-bayes-ml-text-classifier.git
    ```

2. Navigate to the project directory:
    ```bash
    cd naive-bayes-ml-text-classifier
    ```

## Usage

1. Ensure your input file is in the same directory as the script or specify the path to the file.

2. Run the Python script:
    ```bash
    python ooclassifier.py < input_file.txt
    ```

3. The script will process the file, using Naive Bayes classification techniques on predefined target words related to weather and environment.

## Customization

You can modify the list of `TargetWords` in the script to fit your specific needs. These words are used for classification within the input text.

```python
TargetWords = [
    'outside', 'today', 'weather', 'raining', 'nice', 'rain', 'snow',
    'day', 'winter', 'cold', 'warm', 'snowing', 'out', 'hope', 'boots',
    'sunny', 'windy', 'coming', 'perfect', 'need', 'sun', 'on', 'was',
    '-40', 'jackets', 'wish', 'fog', 'pretty', 'summer'
]
```
