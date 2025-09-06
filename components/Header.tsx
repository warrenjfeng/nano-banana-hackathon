
import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="text-center">
      <h1 className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
        Virtual Style Try-On
      </h1>
      <p className="mt-4 text-lg text-gray-300 max-w-2xl mx-auto">
        See yourself in a new look. Upload your photo and a style inspiration to let our AI create a virtual try-on for you.
      </p>
    </header>
  );
};
