import { errorMessage } from './Login';

test('surfaces the DRF non_field_errors message', () => {
  const err = {
    message: 'Request failed with status code 400',
    response: { data: { non_field_errors: ['Unable to log in with provided credentials.'] } },
  };

  expect(errorMessage(err)).toBe('Unable to log in with provided credentials.');
});

test('surfaces a detail message', () => {
  const err = { message: 'Request failed with status code 401', response: { data: { detail: 'Invalid token.' } } };

  expect(errorMessage(err)).toBe('Invalid token.');
});

test('explains a network failure', () => {
  const err = { message: 'Network Error', code: 'ERR_NETWORK' };

  expect(errorMessage(err)).toMatch(/Cannot reach the API/);
});

test('falls back to the axios message', () => {
  expect(errorMessage({ message: 'Request failed with status code 500' })).toBe(
    'Request failed with status code 500'
  );
});
