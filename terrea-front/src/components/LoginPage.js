import React, { useState } from 'react';
import axios from 'axios';
import DarkModeToggle from './DarkModeToggle'; // Импортируем компонент

const LoginPage = ({ setIsAuthenticated, darkMode, toggleDarkMode }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:8000/profile/login', {
                email,
                password
            });
            console.log(response.data);
            setIsAuthenticated(true);
        } catch (err) {
            if (err.response) {
                setError(err.response.data.detail || 'Ошибка при входе');
                console.error(err.response.data);
            } else {
                setError('Неизвестная ошибка');
                console.error(err);
            }
        }
    };

    const handleLoginWithoutAuth = () => {
        setIsAuthenticated(true);
    };

    return (
        <div className={`flex h-screen flex-col justify-center px-6 py-12 lg:px-8 ${darkMode ? 'bg-slate-800 text-white' : 'bg-white text-gray-900'}`}>
            <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                <img className="mx-auto h-10 w-auto" src="#" alt="Terrea-Web" />
                <h2 className="mt-10 text-center text-2xl font-bold tracking-tight">Авторизируйтесь в ваш аккаунт</h2>
            </div>
            <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-start">Email адрес</label>
                        <div className="mt-2">
                            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} name="email" id="email" autoComplete="email" required className={`block w-full rounded-md px-3 py-1.5 text-base outline outline-1 -outline-offset-1 placeholder:text-gray-400 ${darkMode ? 'bg-slate-700 text-white outline-gray-600' : 'bg-white text-gray-900 outline-gray-300'} focus:outline focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600 sm:text-sm`} />
                        </div>
                    </div>

                    <div>
                        <div className="flex items-center justify-between">
                            <label htmlFor="password" className="block text-sm font-medium">Пароль</label>
                            <div className="text-sm">
                                <a href="https://example.com" className="font-semibold text-indigo-600 hover:text-indigo-500">Забыли пароль?</a>
                            </div>
                        </div>
                        <div className="mt-2">
                            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} name="password" id="password" autoComplete="current-password" required className={`block w-full rounded-md px-3 py-1.5 text-base outline outline-1 -outline-offset-1 placeholder:text-gray-400 ${darkMode ? 'bg-slate-700 text-white outline-gray-600' : 'bg-white text-gray-900 outline-gray-300'} focus:outline focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600 sm:text-sm`} />
                        </div>
                    </div>

                    <div>
                        <button type="submit" className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Войти</button>
                    </div>

                    <div>
                        <button type="button" onClick={handleLoginWithoutAuth} className="flex w-full justify-center rounded-md bg-green-600 px-3 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-green-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-600">Войти без авторизации</button>
                    </div>

                    {error && <p className="text-red-500">{error}</p>}
                </form>
                <p className='text-sm text-gray-500 pt-5'>
                    Не пользователь?
                    <a href="https://example.com" className="font-semibold text-indigo-600 hover:text-indigo-500"> Начните бесплатную пробную подписку 14 дней</a>
                </p>
            </div>
            <DarkModeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode} /> {/* Используем компонент */}
        </div>
    );
};

export default LoginPage;