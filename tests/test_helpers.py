import unittest
from slave import view, dump
from slave.response import Response, ResponseFormatter, ResponseValidator

class TestHelpersAndFacades(unittest.TestCase):
    def test_dump_basic(self):
        data = {'foo': 'bar'}
        result = dump(data)
        self.assertIn('<pre>', result)
        self.assertIn('foo', result)
        self.assertIn('bar', result)

    def test_dump_handles_datetime(self):
        from datetime import datetime
        data = {'now': datetime(2020, 1, 1, 12, 0)}
        result = dump(data)
        self.assertIn('2020-01-01T12:00:00', result)

    def test_response_success(self):
        data = {'foo': 'bar'}
        resp = Response.success('cmd1', data)
        d = resp.to_dict()
        self.assertEqual(d['status'], 'success')
        self.assertEqual(d['command_id'], 'cmd1')
        self.assertEqual(d['data'], data)
        self.assertIn('timestamp', d)

    def test_response_error(self):
        resp = Response.error('cmd2', 'fail')
        d = resp.to_dict()
        self.assertEqual(d['status'], 'error')
        self.assertEqual(d['command_id'], 'cmd2')
        self.assertEqual(d['error'], 'fail')

    def test_response_to_json(self):
        data = {'foo': 'bar'}
        resp = Response.success('cmd3', data)
        json_str = resp.to_json()
        self.assertIn('foo', json_str)
        self.assertIn('cmd3', json_str)

    def test_response_validator(self):
        d = {'command_id': 'cmd4', 'status': 'success', 'data': {'foo': 'bar'}}
        resp = ResponseValidator.validate(d)
        self.assertEqual(resp.command_id, 'cmd4')
        self.assertEqual(resp.status, 'success')
        self.assertEqual(resp.data, {'foo': 'bar'})

    def test_response_formatter_success(self):
        json_str = ResponseFormatter.format_success('cmd5', {'foo': 'bar'})
        self.assertIn('foo', json_str)
        self.assertIn('cmd5', json_str)

    def test_response_formatter_error(self):
        json_str = ResponseFormatter.format_error('cmd6', 'fail')
        self.assertIn('fail', json_str)
        self.assertIn('cmd6', json_str)

if __name__ == '__main__':
    unittest.main() 