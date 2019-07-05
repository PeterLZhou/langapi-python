{import json
import re
import itertools
from typing import Union


class LangTranslateClient:
    translations: dict = {}
    public_key: str
    target_language: str

    def __init__(self, public_key: str, target_language: str, translations_file_path: str):
        self.public_key = public_key
        self.translations = json.loads(open(translations_file_path).read())
        self.targetLanguage = target_language

        print(self.translations)

    def tr(self, phrase: Union[str, None], variables: dict = None, options: dict = None) -> Union[str, None]:
        variables = variables if variables is not None else {}
        options = options if options is not None else {}
        force_language = options["forceLanguage"] if "forceLanguage" in options else None
        original_language = self.translations["originalLanguage"] if "originalLanguage" in options else None

        # fallback to original phrase if info doesn't exist
        if (phrase is None
                or not self.translations
                or not original_language
                or (not self.target_language and not force_language)):
            return (self.replace_placeholders_with_parameters(phrase, variables)
                    if phrase is not None
                    else None)

        # phrase stripped of placeholders to index into resource file
        phrase_key: str = self.replace_parameters_with_placeholders(phrase, variables)

        # phrase-specific forced language takes precedence over global target language
        target_language: str = force_language if force_language is not None else self.target_language

        # lookup key in prod resource file and fallback to test
        try:
            return self.replace_placeholders_with_parameters(
                self.translations["prod"][original_language][target_language][phrase_key], variables
            )
        except KeyError:
            try:
                return self.replace_placeholders_with_parameters(
                    self.translations["test"][original_language][target_language][phrase_key], variables
                )
            except KeyError:
                return self.replace_placeholders_with_parameters(phrase, variables)

    @staticmethod
    def replace_parameters_with_placeholders(phrase, variables):
        index = itertools.count(0)
        for name in variables:
            phrase = re.sub(r'{' + name + '}', '{' + str(next(index)) + '}', phrase)

        return phrase

    @staticmethod
    def replace_placeholders_with_parameters(phrase: str, variables: dict):
        for name, value in variables.items():
            # replace parameters of the form {name} w/ parameter's value
            dynamic_regex = '\\{' + name + '\\}'
            phrase = re.sub(dynamic_regex, value, phrase)

        return phrase
