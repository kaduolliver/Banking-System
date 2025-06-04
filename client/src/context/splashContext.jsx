import React, { createContext, useState, useContext } from 'react';

const SplashContext = createContext();

export function SplashProvider({ children }) {
  const [showSplash, setShowSplash] = useState(false);

  return (
    <SplashContext.Provider value={{ showSplash, setShowSplash }}>
      {children}
    </SplashContext.Provider>
  );
}

export function useSplash() {
  return useContext(SplashContext);
}
