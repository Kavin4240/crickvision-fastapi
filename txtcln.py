
from collections import Counter
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.linear_model import LinearRegression
from collections import Counter
import warnings

warnings.filterwarnings("ignore","\nPyarrow",DeprecationWarning)

# Function to clean and preprocess user response
# For pre processing
def clean_and_preprocess(response):
    # Tokenization
    tokens = word_tokenize(response)
    
    # Lowercasing
    tokens = [token.lower() for token in tokens]
    
    # Removal of Punctuation
    tokens = [re.sub(r'[^\w\s]', '', token) for token in tokens]
    
    # Stopword Removal
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens




# Function to convert qualitative responses into structured data
def qualitative_to_structured(cleaned_response):
    structured_data = []
    for response in responses:
        words = response.split()
        structured_data.append({word: words.count(word) for word in words})
    return structured_data

# Function for sentiment analysis
def perform_sentiment_analysis(cleaned_response):
    sentiment_scores = []
    for response in cleaned_response:
        # If the response is a list of words, join them into a single string
        if isinstance(response, list):
            response = ' '.join(cleaned_response)
        
        positive_words = ['good', 'great', 'excellent', 'happy', 'satisfied']
        negative_words = ['bad', 'poor', 'terrible', 'unhappy', 'unsatisfied']
        
        # Ensure response is treated as a string from this point
        response_text = response.lower()  # This should not cause an error now
        num_positive = sum(1 for word in positive_words if word in response_text)
        num_negative = sum(1 for word in negative_words if word in response_text)
        
        sentiment_score = (num_positive - num_negative) / max(len(response_text.split()), 1)
        sentiment_scores.append(sentiment_score)
    
    return sentiment_scores


# Function for text clustering
def perform_text_clustering(cleaned_response):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(cleaned_response)
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    return cluster_labels

# Function for keyword extraction
def extract_keywords(cleaned_response):
    all_words = ' '.join(cleaned_response)
    words = all_words.split()
    keywords = [word for word, count in Counter(words).most_common(10)]
    return keywords

# Function for topic modeling
def perform_topic_modeling(cleaned_response):
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(cleaned_response)
    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    topic_matrix = lda.fit_transform(tfidf_matrix)
    return topic_matrix

# Function for frequency distribution analysis
def calculate_frequency_distribution(data):
    frequency_distribution = {}
    for item in data:
        if item in frequency_distribution:
            frequency_distribution[item] += 1
        else:
            frequency_distribution[item] = 1
    return frequency_distribution

# Function for correlation analysis
def perform_correlation_analysis(data1, data2):
    # Check if either data1 or data2 is constant
    if np.std(data1) == 0 or np.std(data2) == 0:
        # Handle the case of constant data; you might return None or some indicator value
        print("Warning: One of the input arrays is constant; the correlation coefficient is not defined.")
        return None, None
    else:
        correlation_coefficient, p_value = pearsonr(data1, data2)
        return correlation_coefficient, p_value

# Function for regression analysis
def perform_regression_analysis(X, y):
    regression_model = LinearRegression().fit(X, y)
    coefficients = regression_model.coef_
    return coefficients

# Define questions
questions = [
    "Imagine you're considering a career change. Describe the thought process you would go through to evaluate the decision. What factors would you consider, such as job satisfaction, salary, work-life balance, and growth opportunities?",
    "Think about a time when you had to resolve a conflict between two friends. Describe how you approached the situation and what steps you took to find a resolution. Did you listen to both sides, mediate the discussion, or suggest compromises?",
    "Reflect on a time when you had to make a significant life decision, ending a relationship. Describe the emotions you experienced and how they influenced your decision-making process. Did you seek advice from others, weigh the pros and cons, or follow your intuition?",
    "Consider a situation where you had to negotiate with a difficult person, such as a client or co-worker. Describe your approach to the negotiation and how you handle conflicts or disagreements. Do you use active listening, assertiveness, or compromise to reach a mutually beneficial outcome?",
    "Imagine you're faced with a moral dilemma, such as witnessing unethical behavior at work. Describe how you would respond to the situation and what factors would influence your decision. Do you consider ethical principles, company policies, or personal values when making moral choices?",
    "Picture yourself in a social setting where you don't know anyone. Describe how you would initiate conversations and build connections with new people. Do you use icebreakers, ask open-ended questions, or share personal anecdotes to engage others?"
]

# Define thinking patterns and their keywords
thinking_patterns = {
     "Confirmation Bias": ["validate", "confirm", "evidence", "bias", "support", "assumption", "belief", "information", "interpretation"],
    "Availability Heuristic": ["remember", "recollection", "recent", "memory", "instance", "common", "familiar", "easy", "accessible"],
    "Anchoring Bias": ["anchor", "initial", "reference", "comparison", "influence", "persuade", "starting", "fixation", "focus", "adjustment"],
    "Overconfidence Bias": ["excessive", "confident", "overestimate", "accuracy", "certainty", "judgment", "confidence", "sureness", "conviction", "self-assured"],
    "Gambler's Fallacy": ["probability", "chance", "luck", "random", "outcome", "past", "event", "previous", "expectation"],
    "Hindsight Bias": ["outcome", "knew-it-all-along", "predict", "realize", "past", "memory", "judgement", "history", "after-the-fact", "foresight"],
    "Recency Bias": ["recent", "last", "recent", "memory", "event", "instance", "recent", "fresh", "recent", "present"],
    "Self-Serving Bias": ["own", "personal", "ego", "selfish", "serve", "benefit", "advantage", "credit", "responsibility", "excuse"],
    "Halo Effect": ["overall", "initial", "positive", "impression", "perception", "good", "favorable", "attribute", "characteristic", "glow"],
    "Framing Effect": ["perspective", "viewpoint", "interpretation", "presentation", "context", "bias", "perception", "framing", "angle", "representation"],
    "Negativity Bias": ["negative", "focus", "attention", "pessimistic", "bad", "downbeat", "gloomy", "unfavorable", "adverse", "critical"],
    "Bandwagon Effect": ["popular", "trend", "follower", "join", "influence", "conformity", "majority", "groupthink", "hype", "craze"],
    "Sunk Cost Fallacy": ["investment", "commitment", "irrecoverable", "loss", "expense", "spent", "past", "investment", "rationalize", "persistent"],
    "False Consensus Effect": ["overestimate", "assumption", "common", "belief", "misjudgment", "consensus", "overgeneralization", "shared", "agreement", "majority"],
    "Illusory Correlation": ["perceive", "association", "imaginary", "false", "relationship", "correlation", "misconception", "inaccuracy", "misinterpretation", "illusion"],
    "In-group Bias": ["group", "favoritism", "in-group", "loyalty", "bias", "preference", "discrimination", "favor", "discrimination", "in-group"],
    "Anchoring-and-Adjustment Heuristic": ["initial", "starting", "reference", "adjust", "adapt", "modify", "change", "alter", "shift", "correct"],
    "Dunning-Kruger Effect": ["ignorance", "incompetence", "unawareness", "overestimate", "overconfidence", "misjudgment", "unskilled", "inept", "illusion", "illusion"],
    "Conformity": ["compliance", "consensus", "majority", "social", "group", "peer", "influence", "pressure", "norm", "uniformity"],
    "Loss Aversion": ["fear", "loss", "risk", "avoidance", "prevention", "reluctance", "anticipation", "anxiety", "concern", "aversion"]

    


}

# Get user responses for each question
user_responses = []
for question in questions:
    response = input(f"{question}\n")
    cleaned_response = clean_and_preprocess(response)
    user_responses.append(cleaned_response)


# Perform text classification for each question
sentiments_by_question = perform_sentiment_analysis(cleaned_response)
clusters_by_question = perform_text_clustering(cleaned_response)
keywords_by_question = extract_keywords(cleaned_response)
topics_by_question = perform_topic_modeling(cleaned_response)

# Convert qualitative data into structured data
def qualitative_to_structured(user_responses):
    structured_data = []
    for response in user_responses:  # Corrected variable name here
        words = response.split()
        structured_data.append({word: words.count(word) for word in words})
    return structured_data


# Perform frequency distribution analysis
# Assuming user_responses is a list of lists where each inner list contains strings
all_words = [word for response_list in user_responses for response in response_list for word in response.split()]
frequency_distribution = calculate_frequency_distribution(all_words)


# Perform correlation analysis between sentiment scores and anticipation scores
anticipation_scores = [score for score in sentiments_by_question]
sentiment_scores = [score for score in sentiments_by_question]
correlation_coefficient, p_value = perform_correlation_analysis(anticipation_scores, sentiment_scores)

# Perform regression analysis between anticipation scores and sentiment scores
X = np.array(anticipation_scores).reshape(-1, 1)
y = np.array(sentiment_scores)
regression_coefficients = perform_regression_analysis(X, y)

# Analyze the most accurate thinking pattern across all questions
thinking_patterns_matched = {}
for pattern, keywords in thinking_patterns.items():
    matched_questions = []
    for i, response in enumerate(user_responses):
        if all(keyword in response for keyword in keywords):
            matched_questions.append(questions[i])
    thinking_patterns_matched[pattern] = matched_questions

# Find the most accurate thinking pattern
accurate_pattern = max(thinking_patterns_matched, key=lambda x: len(thinking_patterns_matched[x]))

# Print results

# Assuming `user_responses` is a list of cleaned and tokenized responses

def identify_thinking_patterns(user_responses, thinking_patterns):
    pattern_scores = {pattern: 0 for pattern in thinking_patterns}
    
    for response in user_responses:
        for word in response:
            for pattern, keywords in thinking_patterns.items():
                if word in keywords:
                    pattern_scores[pattern] += 1
    
    # Optionally, normalize scores or apply different logic to select best match
    # For simplicity, here we just return the pattern scores
    return pattern_scores

# Calculate pattern scores
pattern_scores = identify_thinking_patterns(user_responses, thinking_patterns)

# Find the most accurate thinking pattern
# This can be based on highest score or other criteria depending on your needs
accurate_pattern = max(pattern_scores, key=pattern_scores.get)

print("Thinking Pattern Scores:", pattern_scores)
print("Most Accurate Thinking Pattern:", accurate_pattern)
