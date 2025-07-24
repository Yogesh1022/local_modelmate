import React, { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AppContext } from '../context/AppContext';

/**
 * A component that protects routes from unauthenticated access.
 * If the user is not logged in, it redirects them to the login page.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The child components to render if authenticated.
 */
const ProtectedRoute = ({ children }) => {
  // Get the authentication status from the global context.
  const { isLoggedIn } = useContext(AppContext);
  const location = useLocation();

  // If the user is not logged in, redirect them to the /login page.
  // We save the location they were trying to access in the state,
  // so we can redirect them back there after they successfully log in.
  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If the user is logged in, render the child components (the protected page).
  return children;
};

export default ProtectedRoute;
