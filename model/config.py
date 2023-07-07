# Summary model config
TOKENIZER_MAX_LENGTH = 1024
SUMMARY_MODEL_NAME = "facebook/bart-large-cnn"
SUMMARY_MAX_LENGTH = 130
SUMMARY_MIN_LENGTH = 30
NUM_BEAMS = 4

# Classification model config
CLASSIFY_TOKENIZER_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
CLASSIFY_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

# model config
CLASS_LABELS = [-1.0, 1.0]  # class labels are index 0:Negative 1:Positive
SENTIMENT_VALUE_ROUND = 4