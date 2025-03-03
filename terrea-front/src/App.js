import React, { useState } from 'react';
import LoginPage from './components/LoginPage';
import MainPage from './components/MainPage';

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [darkMode, setDarkMode] = useState(true);

    const toggleDarkMode = () => {
        setDarkMode(prevMode => !prevMode);
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
    };

    return (
        <div>
            {isAuthenticated ? (
                <MainPage onLogout={handleLogout} darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
            ) : (
                <LoginPage 
                    setIsAuthenticated={setIsAuthenticated} 
                    darkMode={darkMode} 
                    toggleDarkMode={toggleDarkMode} 
                />
            )}
        </div>
    );
};

export default App;