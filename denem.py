import argparse
import io
import json
import os
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

text = 'I just listened to the Jonas Brothers\' newly released song. Its straight up fire! Also, I like the fact that they debuted number 1 on Billboard Hot 100 just after returning from a hiatus of 6 years #YOLO #JonasBrothers.'

def classify_text(text2):
    """Classifies content categories of the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text2, six.binary_type):
        text = text2.decode('utf-8')

    document = types.Document(
        content=text2.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    categories = client.classify_text(document).categories

    for category in categories:
        print(u'=' * 20)
        print(u'{:<16}: {}'.format('name', category.name))
        print(u'{:<16}: {}'.format('confidence', category.confidence))
             

client = language.LanguageServiceClient()

if isinstance(text, six.binary_type):
    text = text.decode('utf-8')

# Instantiates a plain text document.
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

 #Detects entities in the document. You can also analyze HTML with:
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
    
classify_text(text)   
    
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
                categories = classify(text, verbose=False)

                result[filename] = categories
        except Exception:
            print('Failed to process {}'.format(file_path))

    with io.open(index_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))

    print('Texts indexed in file: {}'.format(index_file))
    return result
    
index('resources/texts', 'index.json')    