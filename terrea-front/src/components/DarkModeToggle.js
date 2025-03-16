import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faMoon } from '@fortawesome/free-solid-svg-icons';

const DarkModeToggle = ({ darkMode, toggleDarkMode }) => {
    return (
        <button 
            onClick={toggleDarkMode} 
            className={`absolute top-4 right-4 p-2 rounded-md transition-transform duration-300 ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-200 text-gray-900'} wave`}>
            <FontAwesomeIcon icon={darkMode ? faSun : faMoon} className={`transition-transform duration-300`} />
        </button>
    );
};

export default DarkModeToggle;