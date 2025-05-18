import sys
sys.path.append('./')

from nlu.tokenizers.lm_tokenizer import LanguageModelTokenizer
from nlu.featurizers.lm_featurizer import LanguageModelFeaturizer
from nlu.message import Message

text = "今天天气不错,我想出去一趟"
message = Message(
    text = text,
    time = "2023-11-17"
)
message.set("text",text)

component_config = {
    "model_name_or_path": "/rainbow/model/pytorch/ernie"
}

lm_tokenizer = LanguageModelTokenizer(component_config=component_config)

lm_model = LanguageModelFeaturizer(component_config=component_config)

tokenized_dict = lm_tokenizer.tokenize(message.text)
# print(tokenized_dict)
lm_tokenizer.process(message=message)
print(message.as_dict())

lm_model.process(message=message)
print(message.get("language_dense_features"))