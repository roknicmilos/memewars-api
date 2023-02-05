import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('Renders title', () => {
  render(<App/>);
  const title = screen.getByText(/Welcome to the Meme Wars/i);
  expect(title).toBeInTheDocument();
});

test('Renders google login button', () => {
  render(<App/>);
  const buttonText = screen.getByText(/Login with google/i);
  expect(buttonText).toBeInTheDocument();
});
