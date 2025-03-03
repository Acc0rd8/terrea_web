import React from 'react';
import DarkModeToggle from './DarkModeToggle'; 
import './MainPage.css'

const MainPage = ({ onLogout, darkMode, toggleDarkMode }) => {
    return (
        <div className={`${darkMode ? 'bg-slate-800 text-white' : 'bg-white text-gray-900'} min-h-screen`}>
            <header className='header min-w-max '>
                <nav className="header__nav flex justify-center h-full items-center">
                    <a href="https://example.com/" className="header__logo text-purple-600">Terrea</a>
                    <ul className="header__nav_list flex justify-between gap-10">
                        <li className="header__nav_list-item cursor-pointer transition-all hover:text-purple-600">Продукты</li>
                        <li className="header__nav_list-item cursor-pointer transition-all hover:text-purple-600">Цены</li>
                        <li className="header__nav_list-item cursor-pointer transition-all hover:text-purple-600">Обучение</li>
                        <li className="header__nav_list-item cursor-pointer transition-all hover:text-purple-600">О нас</li>
                        <li className="header__nav_list-item cursor-pointer transition-all hover:text-purple-600">Q&A</li>
                    </ul>
                    <ul className='header__loggin flex justify-between'>
                        <button className='header__loggin_reg bg-purple-600 rounded-md'>Регистрация</button>
                        <button className={`header__loggin_auth ${darkMode ? 'border-white' : 'border-black'} bg-none border border-solid rounded-md`}>Войти</button>
                    </ul>
                </nav>
            </header>
            <div className="main-content">
                <h1 className="text-3xl">Добро пожаловать на главную страницу!</h1>
                <button onClick={onLogout} className="mt-4 bg-red-500 text-white px-4 py-2 rounded">Выйти</button>
            </div>
            <DarkModeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode} /> {/* Используем компонент */}
        </div>
    );
};

export default MainPage;