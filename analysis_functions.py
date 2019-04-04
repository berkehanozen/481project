import numpy
import argparse
import io
import json
import os
import six
import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import language_v1
from google.cloud.language_v1 import enums


class GoogleCloud(object):
    @staticmethod
    def classify_text(text):
        try:
            """Classifies content categories of the provided text."""
            client = language.LanguageServiceClient()

            if isinstance(text, six.binary_type):
                text = text.decode('utf-8')

            document = types.Document(
                content=text.encode('utf-8'),
                type=enums.Document.Type.PLAIN_TEXT)

            categories = client.classify_text(document).categories

            for category in categories:
                print(u'=' * 20)
                print(u'{:<16}: {}'.format('name', category.name))
                print(u'{:<16}: {}'.format('confidence', category.confidence))
        except:
            print('Too few words.')

        client = language.LanguageServiceClient()

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Instantiates a plain text document.
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects entities in the document. You can also analyze HTML with:
        document.type == enums.Document.Type.HTML
        entities = client.analyze_entities(document).entities

        for entity in entities:
            entity_type = enums.Entity.Type(entity.type)
            print('=' * 20)
            print(u'{:<16}: {}'.format('name', entity.name))
            print(u'{:<16}: {}'.format('type', entity_type.name))
            print(u'{:<16}: {}'.format('salience', entity.salience))
            print(u'{:<16}: {}'.format('wikipedia_url',
                                       entity.metadata.get('wikipedia_url', '-')))
            print(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')))
    @staticmethod
    def classify(text, verbose=True):
        """Classify the input text into categories. """

        language_client = language.LanguageServiceClient()

        document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)
        response = language_client.classify_text(document)
        categories = response.categories

        result = {}

        for category in categories:
            # Turn the categories into a dictionary of the form:
            # {category.name: category.confidence}, so that they can
            # be treated as a sparse vector.
            result[category.name] = category.confidence

        if verbose:
            print(text)
            for category in categories:
                print(u'=' * 20)
                print(u'{:<16}: {}'.format('category', category.name))
                print(u'{:<16}: {}'.format('confidence', category.confidence))

        return result
    # [END language_classify_text_tutorial_classify]


    # [START language_classify_text_tutorial_index]
    @staticmethod
    def index(path, index_file):
        """Classify each text file in a directory and write
        the results to the index_file.
        """

        result = {}
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if not os.path.isfile(file_path):
                continue

            try:
                with io.open(file_path, 'r') as f:
                    text = f.read()
                    categories = GoogleCloud.classify(text, verbose=False)

                    result[filename] = categories
            except Exception:
                print('Failed to process {}'.format(file_path))

        with io.open(index_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))

        print('Texts indexed in file: {}'.format(index_file))
        return result
    # [END language_classify_text_tutorial_index]


    # [START language_classify_text_tutorial_split_labels]
    @staticmethod
    def split_labels(categories):
        """The category labels are of the form "/a/b/c" up to three levels,
        for example "/Computers & Electronics/Software", and these labels
        are used as keys in the categories dictionary, whose values are
        confidence scores.
        The split_labels function splits the keys into individual levels
        while duplicating the confidence score, which allows a natural
        boost in how we calculate similarity when more levels are in common.
        Example:
        If we have
        x = {"/a/b/c": 0.5}
        y = {"/a/b": 0.5}
        z = {"/a": 0.5}
        Then x and y are considered more similar than y and z.
        """
        _categories = {}
        for name, confidence in six.iteritems(categories):
            labels = [label for label in name.split('/') if label]
            for label in labels:
                _categories[label] = confidence

        return _categories
    # [END language_classify_text_tutorial_split_labels]


    # [START language_classify_text_tutorial_similarity]
    @staticmethod
    def similarity(categories1, categories2):
        """Cosine similarity of the categories treated as sparse vectors."""
        categories1 = GoogleCloud.split_labels(categories1)
        categories2 = GoogleCloud.split_labels(categories2)

        norm1 = numpy.linalg.norm(list(categories1.values()))
        norm2 = numpy.linalg.norm(list(categories2.values()))

        # Return the smallest possible similarity if either categories is empty.
        if norm1 == 0 or norm2 == 0:
            return 0.0

        # Compute the cosine similarity.
        dot = 0.0
        for label, confidence in six.iteritems(categories1):
            dot += confidence * categories2.get(label, 0.0)

        return dot / (norm1 * norm2)
    # [END language_classify_text_tutorial_similarity]

    @staticmethod
    def query_category(index_file, category_string, n_top=3):
        """Find the indexed files that are the most similar to
        the query label.
        The list of all available labels:
        https://cloud.google.com/natural-language/docs/categories
        """

        with io.open(index_file, 'r') as f:
            index = json.load(f)

        # Make the category_string into a dictionary so that it is
        # of the same format as what we get by calling classify.
        query_categories = {category_string: 1.0}

        similarities = []
        for filename, categories in six.iteritems(index):
            similarities.append(
                (filename, GoogleCloud.similarity(query_categories, categories)))

        similarities = sorted(similarities, key=lambda p: p[1], reverse=True)

        print('=' * 20)
        print('Query: {}\n'.format(category_string))
        print('\nMost similar {} indexed texts:'.format(n_top))
        for filename, sim in similarities[:n_top]:
            print('\tFilename: {}'.format(filename))
            print('\tSimilarity: {}'.format(sim))
            print('\n')

        return similarities
    # [END language_classify_text_tutorial_query_category]
    @staticmethod
    def text_sentiment_analysis(content):

        client = language_v1.LanguageServiceClient()

        # content = 'Your text to analyze, e.g. Hello, world!'

        if isinstance(content, six.binary_type):
            content = content.decode('utf-8')

        type_ = enums.Document.Type.PLAIN_TEXT
        document = {'type': type_, 'content': content}

        response = client.analyze_sentiment(document)
        sentiment = response.document_sentiment
        print('Overall sentiment of the text:')
        print('Score: {}'.format(sentiment.score))
        print('Magnitude: {}'.format(sentiment.magnitude))

    @staticmethod
    def entity_sentiment_analysis(text):
        """Detects entity sentiment in the provided text."""
        client = language.LanguageServiceClient()

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)

        # Detect and send native Python encoding to receive correct word offsets.
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16

        result = client.analyze_entity_sentiment(document, encoding)

        for entity in result.entities:
            print('Mentions: ')
            print(u'Name: "{}"'.format(entity.name))
            for mention in entity.mentions:
                print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
                print(u'  Content : {}'.format(mention.text.content))
                print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
                print(u'  Sentiment : {}'.format(mention.sentiment.score))
                print(u'  Type : {}'.format(mention.type))
            print(u'Salience: {}'.format(entity.salience))
            print(u'Sentiment: {}\n'.format(entity.sentiment))
