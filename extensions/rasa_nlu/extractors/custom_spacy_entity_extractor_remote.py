from rasa_nlu.extractors import EntityExtractor
from typing import Any, Dict, List, Text, Optional, Type


class RemoteSpacyCustomNER(EntityExtractor):
    """A custom sentiment analysis component"""
    name = "custom_entities"
    provides = ["custom_entities"]
    language_list = ["en"]
    print('initialised the class')

    defaults = {
        "host": 'custom-ner',
        "port": 9501,
        "arch": None,
        "dropout": 0.1,
        "accumulate_gradient": 1,
        "patience": 500,
        "max_epochs": 0,
        "max_steps": 5000,
        "eval_frequency": 200,
        # by default all dimensions recognized by spacy are returned
        # dimensions can be configured to contain an array of strings
        # with the names of the dimensions to filter for
        "dimensions": None
    }

    def __init__(
            self, component_config: Dict[Text, Any] = None, nlp: "Language" = None
    ) -> None:
        self.nlp = nlp
        self.component_config = component_config
        super(RemoteSpacyCustomNER, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Load the sentiment polarity labels from the text
           file, retrieve training tokens and after formatting
           data train the classifier."""
        entities = []
        texts = []
        for example in training_data.entity_examples:
            texts.append(example.text)
            entities.append(example.get('entities'))
        import requests
        url = 'http://{0}:{1}/train'.format(self.component_config.get('host'),
                                            self.component_config.get('port'))
        data = {"text": texts, "entities": entities, "params": [self.component_config]}
        print(requests.put(url, json=data).text)

    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""
        import requests
        url = 'http://{0}:{1}/predict'.format(self.component_config.get('host'),
                                              self.component_config.get('port'))
        data = {"text": [message.text]}
        response = requests.get(url, json=data)
        json_response = response.json()
        extracted = self.add_extractor_name(json_response['entities'][0])
        message.set("entities", message.get("entities", []) + extracted, add_to_output=True)
