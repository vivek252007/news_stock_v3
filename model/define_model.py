# import torch
import tensorflow as tf
from transformers import (
    AutoTokenizer,
    TFAutoModelForSequenceClassification,
    TFBartForConditionalGeneration
)

from model.config import *
import pandas as pd
from tqdm import tqdm

tqdm.pandas()


class SentimentExtractor():
    def __init__(self):
        self.classify_tokenizer = AutoTokenizer.from_pretrained(CLASSIFY_TOKENIZER_NAME)
        self.classify_model = TFAutoModelForSequenceClassification.from_pretrained(CLASSIFY_MODEL_NAME)
        self.class_labels = [-1.0, 1.0]  # class labels are index 0:Negative 1:Positive
        self.sentiment_value_round = 4

    def _init_summary_model(self):
        self.summary_tokenizer = AutoTokenizer.from_pretrained(SUMMARY_MODEL_NAME)
        self.summary_model = TFBartForConditionalGeneration.from_pretrained(SUMMARY_MODEL_NAME)

    def summarization_model(self, text_article):
        inputs = self.summary_tokenizer(
            text_article,
            max_length=TOKENIZER_MAX_LENGTH,
            return_tensors="tf",
            truncation=True
        )
        summary_ids = self.summary_model.generate(
            inputs["input_ids"],
            num_beams=NUM_BEAMS,
            min_length=SUMMARY_MIN_LENGTH,
            max_length=SUMMARY_MAX_LENGTH
        )

        return self.summary_tokenizer.batch_decode(
            summary_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]

    def text_classification_model(self, text_summary):
        inputs = self.classify_tokenizer(text_summary, return_tensors="tf")
        logits = self.classify_model(**inputs).logits
        softmax_prob = tf.math.multiply(
            tf.nn.softmax(logits, axis=-1),
            tf.constant(self.class_labels)).numpy().tolist()[0]

        return [round(element, self.sentiment_value_round)
                for element in softmax_prob
                ]

        # predicted_class_id = int(tf.math.argmax(logits, axis=-1)[0])
        # pred_class = self.classify_model.config.id2label[predicted_class_id]
        # with torch.no_grad():
        #     logits = self.classify_model(**inputs).logits
        #
        # softmax_prob = torch.nn.Softmax(dim=0)
        # # pred_class = self.classify_model.config.id2label[logits.argmax().item()]
        # return [round(element, self.sentiment_value_round)
        #         for element in softmax_prob(logits[0]) \
        #             .mul(torch.tensor(self.class_labels)) \
        #             .tolist()
        #         ]

    def get_sentiment_values(self, news_df, process_desc=True):

        headline_sentiment = pd.DataFrame(
            news_df["Title"].progress_apply(
                lambda x: self.text_classification_model(x)
            ).tolist(), index=news_df.index) \
            .rename(columns={0: 'title_negative', 1: 'title_positive'})

        # TODO: It truncates the description, the max text(token) length is 1024
        if process_desc:
            self._init_summary_model()
            description_sentiment = pd.DataFrame(
                news_df["Text"].progress_apply(
                    lambda x: self.text_classification_model(
                        self.summarization_model(x))
                ).tolist(), index=news_df.index) \
                .rename(columns={0: 'text_negative', 1: 'text_positive'})

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
    # print(summary)
    # print(sentiment)
