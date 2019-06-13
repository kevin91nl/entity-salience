"""The preprocess packages contains preprocessing methods."""


class Token:
    """A class for representing a token."""

    def __init__(self, text):
        """Initialize a token.

        Parameters
        ----------
        text : str
            The label of the token.
        """
        self.text = text

    def __str__(self):
        """Create the string representation of a token.

        Returns
        -------
        str
            The string representation of a tokens.
        """
        return self.text

    def __repr__(self):
        """Create the string representation of a token.

        Returns
        -------
        str
            The string representation of a tokens.
        """
        return self.__str__()


class Tokens(list):
    """A class holding the tokens of a text."""

    def __init__(self, raw_tokens):
        """Initialize the list of tokens with raw tokens (strings).

        Parameters
        ----------
        raw_tokens : list
            A list of tokens (strings).
        """
        super().__init__()
        for raw_token in raw_tokens:
            self.append(Token(text=raw_token))

    def __str__(self):
        """Create the string representation of the tokens.

        Returns
        -------
        str
            The string representation of the tokens.
        """
        quotes_tokens = [f'"{token}"' for token in self]
        tokens_display = ', '.join(quotes_tokens) if len(quotes_tokens) < 10 else ', '.join(
            quotes_tokens[:3]) + ', ..., ' + ', '.join(quotes_tokens[-3:])
        return "Tokens ({}): [{}]".format(len(self), tokens_display)

    def __repr__(self):
        """Create the string representation of the tokens.

        Returns
        -------
        str
            The string representation of the tokens.
        """
        return self.__str__()


class Tokenizer:
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

    def __init__(self, tokenizer_method=None):
        """Initialize the tokenizer.

        Parameters
        ----------
        tokenizer_method : function
            A function which tokenizes the given input and returns a list of tokens.
        """
        self.tokenizer_method = tokenizer_method if tokenizer_method is not None else self.default_tokenizer

    def __call__(self, text):
        """Tokenize a text.

        Parameters
        ----------
        text : str
            Text to tokenize

        Returns
        -------
        Tokens
            A class holding the tokens.
        """
        return Tokens(self.tokenizer_method(text))
