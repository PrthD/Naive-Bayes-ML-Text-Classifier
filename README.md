
# Naive Bayes ML Text Classifier

A Python-based machine learning text classifier that uses the **Naive Bayes** algorithm to classify input text based on predefined target words. The project demonstrates the application of object-oriented programming principles in building a flexible and reusable text classification system. It processes text from input files and classifies it based on environmental themes such as weather and seasons, making it an excellent tool for natural language processing (NLP) tasks.

## Features

- **Naive Bayes Classifier**: Implements a Naive Bayes algorithm for text classification based on word occurrences in the input text.
- **Object-Oriented Design**: Utilizes object-oriented programming principles, ensuring flexibility, readability, and maintainability of the code.
- **File Input Processing**: Reads text from files or standard input and performs classification.
- **Target Word Matching**: Analyzes input text to classify it based on predefined target words, with a focus on weather, seasons, and environmental-related themes.
- **Error Handling**: Includes robust error handling for file input errors (e.g., missing files, OS-related issues).

## Installation

Ensure that **Python 3** is installed on your system. No additional external dependencies are required for this project.

### Steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Naive-Bayes-ML-Text-Classifier.git
   ```

2. **Navigate to the `src/` directory**:
   ```bash
   cd Naive-Bayes-ML-Text-Classifier/src
   ```

## Usage

1. Place the input file in the `src/` directory, or specify the path to the file.

2. Run the script with the following command:
   ```bash
   python ooclassifier.py < input_file.txt
   ```

   - The classifier will process the file and use Naive Bayes techniques to classify the text based on predefined target words related to weather and environmental themes.

### Example:

```bash
python ooclassifier.py < example_input.txt
```

This will classify the input based on occurrences of target words.

## Customization

You can easily modify the predefined list of target words within the script to suit your specific classification needs. These words are used for matching and classification during the Naive Bayes analysis.

```python
TargetWords = [
    'outside', 'today', 'weather', 'raining', 'nice', 'rain', 'snow',
    'day', 'winter', 'cold', 'warm', 'snowing', 'out', 'hope', 'boots',
    'sunny', 'windy', 'coming', 'perfect', 'need', 'sun', 'on', 'was',
    '-40', 'jackets', 'wish', 'fog', 'pretty', 'summer'
]
```

## Repository File Structure

- **src/ooclassifier.py**: The main Python script containing the Naive Bayes classifier implementation.
- **src/example_input.txt**: A sample input text file that demonstrates how the classifier works.
- **requirements.txt** (Optional): Placeholder for listing external dependencies (currently not required).
- **README.md**: Documentation that explains the project's usage, features, and installation.

## License

This project is open for educational and non-commercial use.
