import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    BartTokenizer,
    BartForConditionalGeneration
)
import pandas as pd
from tqdm import tqdm

tqdm.pandas()


class SentimentExtractor():
    def __init__(self):
        self._summarization_model_params()
        self._text_classification_params()
        self.summary_tokenizer = BartTokenizer.from_pretrained(self.summary_model_name)
        self.summary_model= BartForConditionalGeneration.from_pretrained(self.summary_model_name)
        self.classify_tokenizer = AutoTokenizer.from_pretrained(self.classify_tokenizer_name)
        self.classify_model = AutoModelForSequenceClassification.from_pretrained(self.classify_model_name)
        self.class_labels = [-1, 1]  # class labels are index 0:Negative 1:Positive
        self.sentiment_value_round = 4

    def _summarization_model_params(self):
        self.tokenizer_max_length = 1024
        self.summary_model_name = "facebook/bart-large-cnn"
        self.summary_max_length = 130
        self.summary_min_length = 30
        self.num_beams = 4

    def _text_classification_params(self):
        self.classify_tokenizer_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.classify_model_name = "distilbert-base-uncased-finetuned-sst-2-english"

    def summarization_model(self, text_article):
        inputs = self.summary_tokenizer(
            text_article,
            max_length=self.tokenizer_max_length,
            return_tensors="pt",
            truncation=True
        )
        summary_ids = self.summary_model.generate(
            inputs["input_ids"],
            num_beams=self.num_beams,
            min_length=self.summary_min_length,
            max_length=self.summary_max_length
        )

        return self.summary_tokenizer.batch_decode(
            summary_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]

    def text_classification_model(self, text_summary):
        inputs = self.classify_tokenizer(text_summary, return_tensors="pt")
        with torch.no_grad():
            logits = self.classify_model(**inputs).logits

        softmax_prob = torch.nn.Softmax(dim=0)
        # pred_class = self.classify_model.config.id2label[logits.argmax().item()]
        return [round(element, self.sentiment_value_round)
                for element in softmax_prob(logits[0]) \
                    .mul(torch.tensor(self.class_labels)) \
                    .tolist()
                ]

    def get_sentiment_values(self, news_df, process_desc=True):

        headline_sentiment = pd.DataFrame(
            news_df["headline"].progress_apply(
                lambda x: self.text_classification_model(x)
            ).tolist(), index=news_df.index) \
            .rename(columns={0: 'headline_negative', 1: 'headline_positive'})

        # TODO: It truncates the description, the max text(token) length is 1024
        if process_desc:
            description_sentiment = pd.DataFrame(
                news_df["description"].progress_apply(
                    lambda x: self.text_classification_model(
                        self.summarization_model(x))
                ).tolist(), index=news_df.index) \
                .rename(columns={0: 'description_negative', 1: 'description_positive'})

            return pd.concat([news_df, headline_sentiment, description_sentiment], axis=1)
        else:
            return pd.concat([news_df, headline_sentiment], axis=1)


if __name__ == "__main__":
    text = "Wall Street’s fast money has a new favorite bet. " \
           "Microsoft (MSFT) has replaced Amazon (AMZN) as the " \
           "most popular top 10 holding among hedge funds, strategists " \
           "at Goldman Sachs led by Ben Snider said in a recent note. " \
           "The investment bank’s Hedge Fund Trend Monitor, which " \
           "analyzes positions across 786 firms in the industry, " \
           "found 82 have Microsoft among their top 10 long positions; " \
           "Amazon appeared across the leading cohort of picks 79 times."

    sentiment_ext = SentimentExtractor()
    # summaries = sentiment_ext.summarization_model([text])
    summary = sentiment_ext.summarization_model(text)
    # sentiments = [sentiment_ext.text_classification_model(summary) for summary in summaries]
    sentiment = sentiment_ext.text_classification_model(summary)
    # print(sentiments)
    print(summary)
    print(sentiment)

