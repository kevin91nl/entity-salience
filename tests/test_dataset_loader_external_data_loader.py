import json
import unittest
import dataset.loader
import pandas as pd


class TestDatasetLoaderExternalDataLoader(unittest.TestCase):
    """Tests for the ExternalDataLoader class."""

    class FakeResponse:
        """The FakeResponse class makes a fake response by a self-specified status code and content."""

        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content.encode('utf-8')

    class FakeRequests:
        """The FakeRequests class fakes the requests library and has a custom get() method which always delivers the
        given FakeResponse."""

        def __init__(self, fake_response):
            self.fake_response = fake_response
            self.call_count = 0

        def get(self, url):
            self.call_count += 1
            return self.fake_response

    def test_get_csv(self):
        # Fake a response (for any given URL)
        dataset.loader.requests = self.FakeRequests(self.FakeResponse(
            status_code=200,
            content='header1,header2' + "\n" + 'cell1,cell2'
        ))

        # Setup the external dataloader
        loader = dataset.loader.ExternalDataLoader()
        loader.files['test-csv'] = {
            'path': 'test.csv',
            'parser': dataset.loader.ExternalDataLoader.parse_csv
        }

        # Try to fetch the file
        result = loader.get('test-csv', ignore_cache=True)

        # Check whether the content is correct
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 1)
        self.assertListEqual(result.columns.tolist(), ['header1', 'header2'])
        self.assertDictEqual(result.iloc[0].to_dict(), {'header1': 'cell1', 'header2': 'cell2'})

    def test_get_json(self):
        # Fake a response (for any given URL)
        dataset.loader.requests = self.FakeRequests(self.FakeResponse(
            status_code=200,
            content=json.dumps({'hello': {0: 'world'}})
        ))

        # Setup the external dataloader
        loader = dataset.loader.ExternalDataLoader()
        loader.files['test-json'] = {
            'path': 'test.json',
            'parser': dataset.loader.ExternalDataLoader.parse_json
        }

        # Try to fetch the file
        result = loader.get('test-json', ignore_cache=True)

        # Check whether the content is correct
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[0], 1)
        self.assertListEqual(result.columns.tolist(), ['hello'])
        self.assertDictEqual(result.iloc[0].to_dict(), {'hello': 'world'})

    def test_404_response(self):
        # Fake a 404 (file not found) response
        dataset.loader.requests = self.FakeRequests(self.FakeResponse(
            status_code=404,
            content=""
        ))

        # Setup the external dataloader
        loader = dataset.loader.ExternalDataLoader()

        # Try to fetch any file (which will encounter a 404 by the fake request)
        first_file = list(loader.files.keys())[0]

        # Trying to fetch the file should raise a ValueError
        with self.assertRaises(ValueError):
            loader.get(first_file, ignore_cache=True)

    def test_get_unknown_file(self):
        # Setup the external dataloader
        loader = dataset.loader.ExternalDataLoader()

        # Trying to fetch an unknown file should raise a ValueError
        unknown_file = '$unknown_file'
        with self.assertRaises(ValueError):
            loader.get(unknown_file, ignore_cache=True)

    def test_cache_mechanism(self):
        # Fake a response (for any given URL)
        dataset.loader.requests = self.FakeRequests(self.FakeResponse(
            status_code=200,
            content=json.dumps({'hello': {0: 'world'}})
        ))

        # Setup the external dataloader
        loader = dataset.loader.ExternalDataLoader()
        loader.files['test-json'] = {
            'path': 'test.json',
            'parser': dataset.loader.ExternalDataLoader.parse_json
        }

        # Try to fetch the file
        first_result = loader.get('test-json')

        # Now try to fetch the file for the second time
        second_result = loader.get('test-json')

        # Check whether the URL is called only once and whether the results are equal
        self.assertDictEqual(first_result.to_dict(), second_result.to_dict())
        self.assertEqual(1, dataset.loader.requests.call_count)

    def test_ignore_cache(self):
        # Fake a response (for any given URL)
        dataset.loader.requests = self.FakeRequests(self.FakeResponse(
            status_code=200,
            content=json.dumps({'hello': {0: 'world'}})
        ))

        # Setup the external dataloader
        loader = dataset.loader.ExternalDataLoader()
        loader.files['test-json'] = {
            'path': 'test.json',
            'parser': dataset.loader.ExternalDataLoader.parse_json
        }

        # Try to fetch the file
        first_result = loader.get('test-json', ignore_cache=True)

        # Now try to fetch the file for the second time
        second_result = loader.get('test-json', ignore_cache=True)

        # Check whether the URL is called every time (since the ignore_cache flag is true) and whether the results are
        # equal
        self.assertDictEqual(first_result.to_dict(), second_result.to_dict())
        self.assertEqual(2, dataset.loader.requests.call_count)
