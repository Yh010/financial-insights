// src/main.tsx

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';

// Import your page components
import App from './App.tsx';
import { LandingPage } from './pages/LandingPage.tsx'; // Assuming LandingPage is in src/pages/

// 1. Define your application's routes
const router = createBrowserRouter([
  {
    path: '/', // The root path will show the landing page
    element: <LandingPage />,
  },
  {
    path: '/app', // The /app path will show the main chat application
    element: <App />,
  },
]);

// 2. Render the RouterProvider with your defined routes
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);