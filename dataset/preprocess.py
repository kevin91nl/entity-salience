"""The preprocess packages contains preprocessing methods."""


class Tokenize:
    """Class used for the tokenizing a text."""

    @staticmethod
    def default_tokenizer(text):
        """Tokenize a text.

        Parameters
        ----------
        text : str
            Text to tokenize.

        Returns
        -------
        list
            List of tokens.
        """
        return text.split()

    def __init__(self, text, tokenizer_method=None):
        """Tokenize a text.

        Parameters
        ----------
        text : str
            Text to tokenize
        tokenizer_method : function
            Method to use to convert a text into tokens.
        """
        self.tokenizer_method = tokenizer_method if tokenizer_method is not None else self.default_tokenizer
        self.tokens = list(self.tokenizer_method(text))

    def __str__(self):
        """Create the string representation of the tokens.

        Returns
        -------
        str
            The string representation of the tokens.
        """
        quotes_tokens = [f'"{token}"' for token in self.tokens]
        tokens_display = ', '.join(quotes_tokens) if len(quotes_tokens) < 10 else ', '.join(
            quotes_tokens[:3]) + ', ..., ' + ', '.join(quotes_tokens[-3:])
        return "Tokens ({}): [{}]".format(len(self.tokens), tokens_display)

    def __repr__(self):
        """Create the string representation of the tokens.

        Returns
        -------
        str
            The string representation of the tokens.
        """
        return self.__str__()

    def __getitem__(self, item):
        """Retrieve a token.

        Parameters
        ----------
        item : int
            Index of the token.

        Returns
        -------
        str
            The token at the given. index.
        """
        return self.tokens[item]

    def __setitem__(self, key, value):
        """Set a token.

        Parameters
        ----------
        key : int
            The index of the token.
        value : str
            The new value of the token.
        """
        self.tokens[key] = value
