from types import SimpleNamespace


class EasyNamespace(SimpleNamespace):
    """
    acts as a dot accessed "dictionary"
    some methods are "missing" but are added as needed

    the diference between EasyNamespace and SimpleNamespace is that
    EeasyNameSpace goes creates EasyNamespacesof every dictionary in the
    given dictionary
    """

    def __init__(self, dictionary) -> None:
        if isinstance(dictionary, dict):
            super(EasyNamespace, self).__init__(**dictionary)
            for key in self.keys():
                if isinstance(self[key], dict):
                    setattr(self, key, EasyNamespace(self[key]), )
        else:
            raise AttributeError(
                f"got '{type(dictionary).__name__}' expected a 'dict'")

    def update(self, dictionary: dict) -> None:
        """
        acts as a dictionarys update() method

        setts the attributes to the EeasyNamespace object
        adds another EasyNamespace object if the value is a dictionary
        :param dictionary: dict
        :return: None
        """
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    setattr(self, key, EasyNamespace(value))
                else:
                    setattr(self, key, value)
        else:
            raise AttributeError(
                f"got '{type(dictionary).__name__}' expected a 'dict'")

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def __len__(self):
        return self.__dict__.__len__()

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__.__repr__()

    def __iter__(self):
        return self.__dict__.__iter__()
