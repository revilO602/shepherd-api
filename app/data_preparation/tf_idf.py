import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models.poi import Poi
from app.database import SessionLocal

# Download NLTK resources (only required once)
nltk.download("punkt")
nltk.download("stopwords")

# Initialize NLTK components for text preprocessing
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


# Function for text preprocessing (tokenization, stopwords removal, and stemming)
def preprocess_text(text):
    if text is None:
        text = ""  # Default to empty string if text is None

    # Remove punctuation using regular expression
    text = re.sub(r"[^\w\s]", "", text)

    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Remove stopwords and apply stemming to each word
    filtered_words = [stemmer.stem(word) for word in words if word not in stop_words]

    # Join the filtered words back into a single string
    preprocessed_text = " ".join(filtered_words)

    return preprocessed_text


# Function to fetch POI descriptions and related data from the database using SQLAlchemy
def fetch_poi_data_from_db():
    # Initialize SQLAlchemy session and preprocess POI data
    session = SessionLocal()
    poi_descriptions = []
    poi_ids = []
    try:
        pois = session.query(Poi).all()  # Query all POIs

        for poi in pois:
            poi_ids.append(poi.id)
            # Preprocess description, name, tags, and reviews
            description = preprocess_text(poi.description)
            name = preprocess_text(poi.name)
            tags = " ".join([preprocess_text(tag) for tag in poi.tags])

            reviews_text = []
            for review in poi.reviews:
                review_title = preprocess_text(review["title"])
                review_text = preprocess_text(review["text"])
                review_trip_type = preprocess_text(review["trip_type"])
                reviews_text.append(f"{review_title} {review_text} {review_trip_type}")

            # Combine all text data for TF-IDF analysis
            combined_text = f"{name} {description} {tags} {' '.join(reviews_text)}"
            poi_descriptions.append(combined_text)
    except Exception as e:
        # Rollback changes if an error occurs
        session.rollback()
        print(f"Error inserting additional data: {e}")

    finally:
        # Close the session to release resources
        session.close()

    return poi_ids, poi_descriptions


def add_tf_idf_relevances_to_pois(all_tf_ids):
    session = SessionLocal()
    try:
        # pois = session.query(Poi).filter(Poi.name.is_(None)).all()
        pois = session.query(Poi).all()
        for poi in pois:
            print(poi.id)
            poi.tf_idf_relevances = all_tf_ids[poi.id]

        # Commit the session to persist changes
        session.flush()
        session.commit()
        print("Additional data inserted successfully.")
    except Exception as e:
        # Rollback changes if an error occurs
        session.rollback()
        print(f"Error inserting additional data: {e}")

    finally:
        # Close the session to release resources
        session.close()


poi_ids, poi_descriptions = fetch_poi_data_from_db()

# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the preprocessed descriptions to compute TF-IDF scores
tfidf_matrix = tfidf_vectorizer.fit_transform(poi_descriptions)

# Get feature names (words) from the vectorizer
feature_names = tfidf_vectorizer.get_feature_names_out()

# Calculate TF-IDF scores for each word in the vocabulary
all_tf_ids = {}
for i, description in enumerate(poi_descriptions):
    poi_tf_idf_dict = {}
    scores = []
    feature_index = tfidf_matrix[i, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])

    for word_index, score in tfidf_scores:
        scores.append((feature_names[word_index], score))

    for word, score in scores:
        poi_tf_idf_dict[word] = round(score, 4)
    all_tf_ids[poi_ids[i]] = poi_tf_idf_dict
    add_tf_idf_relevances_to_pois(all_tf_ids)
