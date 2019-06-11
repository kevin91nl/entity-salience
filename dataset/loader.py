"""The loader package contains data loaders for the entity salience project."""
import io
from urllib.parse import urljoin

import requests
import pandas as pd


class ExternalDataLoader:
    """A class for loading external data."""

    def __init__(self):
        """Initialize the external data loader."""
        self.base_url = 'https://raw.githubusercontent.com/kevin91nl/entity-salience-data/master/data/wikiphrase/'
        self.files = {
            'annotations': {'path': 'annotations.csv', 'parser': self.parse_csv},
            'wikinews-docs': {'path': 'wikinews-docs.json', 'parser': self.parse_json},
            'wikinews-entities': {'path': 'wikinews-entities.json', 'parser': self.parse_json},
            'wikipedia-entities': {'path': 'wikipedia-entities.json', 'parser': self.parse_json},
        }

    @staticmethod
    def parse_csv(content):
        """Create a DataFrame from CSV data.

        Parameters
        ----------
        content : bytes
            The CSV content (bytes) to convert into a DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame.
        """
        return pd.read_csv(io.StringIO(content.decode('utf-8')))

    @staticmethod
    def parse_json(content):
        """Create a DataFrame from JSON data.

        Parameters
        ----------
        content : bytes
            The JSON content (bytes) to convert into a DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame.
        """
        return pd.read_json(io.StringIO(content.decode('utf-8')))

    def get(self, file, ignore_cache=False):
        """Retrieve the DataFrame for a given file by fetching the data from an external data source.

        Parameters
        ----------
        file : str
            The file to retrieve (see self.files for the possible files).
        ignore_cache : bool
            When set to true, any cache is ignored and a new cache is created for the given file.

        Returns
        -------
        pd.DataFrame
            The found DataFrame.

        Raises
        ------
        ValueError
            When the file is not found or when an error occurred during the lookup.
        """
        if file not in self.files:
            raise ValueError(f'File "{file}" not found. Choose one of: [{", ".join(self.files.keys())}]')
        file_metadata = self.files.get(file)
        if 'cache' in file_metadata and not ignore_cache:
            return file_metadata['cache']
        path = file_metadata['path']
        parser = file_metadata['parser']
        url = urljoin(self.base_url, path)
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f'Could not retrieve file "{file}" on URL "{url}".')
        result = parser(response.content)
        self.files[file]['cache'] = result
        return result
