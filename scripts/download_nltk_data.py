import nltk
import os

def download_nltk_data():
    """Download required NLTK data."""
    # Create data directory if it doesn't exist
    nltk_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Set the download directory
    nltk.data.path.append(nltk_data_dir)
    
    # Download required NLTK resources
    resources = [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger'
    ]
    
    for resource in resources:
        try:
            nltk.download(resource, download_dir=nltk_data_dir)
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")

if __name__ == "__main__":
    download_nltk_data()
