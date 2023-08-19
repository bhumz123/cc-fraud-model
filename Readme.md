## Credit Card Fraud Detection
Credit card fraud detection is a critical task in maintaining the security and integrity of financial transactions. This repository provides an overview of a comprehensive credit card fraud detection system that incorporates various techniques and models to detect fraudulent activities.

#### Disclaimer: Due to the substantial size of certain model files, Git LFS (Large File Storage) was utilized to compress and store these large files. To ensure the smooth running of the project, please Clone the repository and use "git lfs fetch" in order fetch the large files actual contents.

# Index

1. [Credit Card Fraud Detection](#credit-card-fraud-detection)
2. [Exploratoy Data Analysis](#exploratory-data-analysis)
3. [Data Preprocessing](#data-preprocessing)
4. [Balancing the Dataset](#Balancing-the-Dataset)
5. [Feature Selection](#feature-selection)
6. [Train the LSTM model](#train-the-lstm-model)
7. [Generate LSTM predictions](#generate-lstm-predictions)
8. [Combine LSTM predictions with original features](#combine-lstm-predictions-with-original-features)
9. [Train the ARF model](#train-the-arf-model)
10. [Generating LSTM predictions for new Data](#generating-lstm-predictions-for-new-data)
11. [Make predictions using ensemble](#make-predictions-using-ensemble)
12. [Real-time Fraud Detection Enviornment](#REAL-TIME-FRAUD-DETECTION-ENVIORNMENT)


## Exploratory Data Analysis
Exploratory Data Analysis (EDA) is a crucial step to have the understanding and gaining insights from credit card fraud datasets. By examining and visualizing the data, we have uncovered patterns, identified anomalies, and  have better understand the characteristics of fraudulent transactions.
## Data Preprocessing:
Pre-processing is an essential step in credit card fraud detection to gain a better understanding of the data and uncover patterns, anomalies, or trends that may indicate fraudulent activities. Sensitive information like credit card numbers, merchant details, and coordinates are encrypted using encryption techniques to ensure data security and privacy. Two techniques used for encryption are:

FF3: FF3 is a format-preserving encryption scheme that encrypts credit card numbers while preserving their original format and length. It ensures that the encrypted output maintains the same format as the original credit card number, allowing for reversible encryption without compromising data integrity.

GeoHashing: GeoHashing is used to encode and index geographical coordinates, such as latitude and longitude, into a string format. This technique enables efficient indexing and searching of geographical data based on proximity.

RFM: RFM (Recency, Frequency, Monetary) is performed to derive meaningful features from the transaction data. RFM metrics capture the recency of transactions, the frequency of transactions, and the monetary value of transactions, along with the risk and credit score of merchants and categories.We have used this to gain a better understanding of customer behaviour and identify segments with different characteristics. It provides insights into customer value and engagement by analysing three key dimensions: recency, frequency, and monetary value.

## Balancing the Dataset
Credit card fraud detection involves dealing with imbalanced datasets where fraudulent transactions are significantly less common than legitimate transactions. To address this class imbalance issue, the Adaptive Synthetic Sampling (ADASYN) technique is used. ADASYN generates synthetic instances of the minority class (fraudulent transactions) based on their feature distributions. This approach helps in creating a more representative dataset for training the model and improves the performance in detecting credit card fraud instances.

## Feature Selection

Weighted feature selection techniques are implemented to determine the importance or relevance of features in the dataset. Two feature selection techniques used in this system are:

Genetic Algorithm (GA): Genetic algorithms are well-suited for feature selection in credit card fraud detection. They automatically search through a large feature space and identify the most informative subset of features for fraud detection. GA can capture feature interactions, handle multicollinearity, and optimize model hyperparameters.

Particle Swarm Optimization (PSO): PSO is a metaheuristic optimization algorithm that iteratively searches the solution space to find the optimal feature subset. PSO is efficient, parallelizable, and capable of balancing accuracy and complexity in feature selection.

## Train the LSTM model:
1. Set up the LSTM architecture, including the number of layers, hidden units, and activation functions.
2. Prepare the training data by formatting it into appropriate input-output sequences.
3. Initialize the LSTM model with the defined architecture.
4. Train the LSTM model using the training data.
5. Monitor the training process and adjust hyperparameters if needed.
6. Save the trained LSTM model for future use.

## Train the ARF model:
1. Set up the ARF (Adaptive Random Forest) model architecture.
2. Prepare the training data by formatting it into appropriate input-output sequences.
3. Initialize the ARF model with the defined architecture.
4. Train the ARF model using the training data.
5. Save the trained ARF model for future use.

## Generating LSTM & ARF predictions for Incoming Data:
1. Load the saved LSTM and ARF models.
3. Generate predictions for the new incoming data using both the models.

## Make Final predictions using Weighted Voting:
1. Weighted Voting is used as an ensemble method.
2. LSTM is given weightage of 0.6 and ARF is given a weightage of 0.4
3. Generate final predictions using the ensemble method.
4. Evaluate the performance of the ensemble predictions using appropriate metrics.


## Real-Time Fraud Detection Enviornment
A robust Architecture is built to enable real-time fraud detection. By leveraging a Flask API, Kafka producer, Kafka consumer, and machine learning predictions, the system aims to quickly identify fraudulent patterns and anomalies as they occur. The immediate storage of event data and corresponding predictions in the PostgreSQL database allows for comprehensive record-keeping and retrospective analysis. This helps in refining the fraud detection system and taking timely actions to mitigate fraud.


