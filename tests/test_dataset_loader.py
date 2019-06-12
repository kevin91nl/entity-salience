import json
import unittest
import dataset.loader


class TestDatasetLoader(unittest.TestCase):
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

        def get(self, url):
            return self.fake_response

    def test_get_csv(self):
        # Fake a response (for any given URL)
        dataset.loader.requests = TestDatasetLoader.FakeRequests(TestDatasetLoader.FakeResponse(
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
        self.assertListEqual(result.columns.tolist(), ['header1', 'header2'])

    def test_get_json(self):
        # Fake a response (for any given URL)
        dataset.loader.requests = TestDatasetLoader.FakeRequests(TestDatasetLoader.FakeResponse(
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
        self.assertListEqual(result.columns.tolist(), ['hello'])

    def test_404_response(self):
        # Fake a 404 (file not found) response
        dataset.loader.requests = TestDatasetLoader.FakeRequests(TestDatasetLoader.FakeResponse(
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
