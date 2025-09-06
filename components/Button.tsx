
import React from 'react';
import { Spinner } from './Spinner';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ children, isLoading = false, disabled, ...props }) => {
  return (
    <button
      {...props}
      disabled={disabled || isLoading}
      className="inline-flex items-center justify-center px-8 py-4 font-semibold text-white transition-all duration-200 bg-purple-600 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {isLoading && <Spinner className="-ml-1 mr-3" />}
      {children}
    </button>
  );
};
