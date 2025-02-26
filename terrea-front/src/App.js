import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
    const [darkMode, setDarkMode] = useState(true); // Состояние для тёмного режима

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const toggleDarkMode = () => {
        setDarkMode(!darkMode); // Переключение состояния
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:8000/profile/login', {
                email,
                password
            }, {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json'
                },
            });
            console.log(response.data);
        } catch (err) {
            if (err.response) {
                setError(err.response.data.detail || 'Ошибка при входе');
                console.error(err.response.data); // Логируем ошибку для отладки
            } else {
                setError('Неизвестная ошибка');
                console.error(err); // Логируем ошибку для отладки
            }
        }
    };

    return (
        <div className={`App min-h-screen flex items-center justify-center ${darkMode ? 'bg-slate-800 text-white' : 'bg-white text-gray-900'}`}>
            <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 align-middle">
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <img className="mx-auto h-10 w-auto" src="#" alt="Terrea-Web"/>
                    <h2 className="mt-10 text-center text-2xl font-bold tracking-tight">{darkMode ? 'Авторизируйтесь в ваш аккаунт' : 'Авторизируйтесь в ваш аккаунт'}</h2>
                </div>
                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-start">{darkMode ? 'Email адрес' : 'Email адрес'}</label>
                            <div className="mt-2">
                                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} name="email" id="email" autoComplete="email" required className={`block w-full rounded-md px-3 py-1.5 text-base outline outline-1 -outline-offset-1 placeholder:text-gray-400 ${darkMode ? 'bg-slate-700 text-white outline-gray-600' : 'bg-white text-gray-900 outline-gray-300'} focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm`} />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm font-medium">{darkMode ? 'Пароль' : 'Пароль'}</label>
                                <div className="text-sm">
                                    <a href="https://example.com" className="font-semibold text-indigo-600 hover:text-indigo-500">Забыли пароль?</a>
                                </div>
                            </div>
                            <div className="mt-2">
                                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} name="password" id="password" autoComplete="current-password" required className={`block w-full rounded-md px-3 py-1.5 text-base outline outline-1 -outline-offset-1 placeholder:text-gray-400 ${darkMode ? 'bg-slate-700 text-white outline-gray-600' : 'bg-white text-gray-900 outline-gray-300'} focus:outline focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm`} />
                            </div>
                        </div>

                        <div>
                            <button type="submit" className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Войти</button>
                        </div>

                        {error && <p>{error}</p>}
                    </form>

                    <p className="mt-10 text-center text-sm text-gray-500">
                        Не пользователь?
                        <a href="https://example.com" className="font-semibold text-indigo-600 hover:text-indigo-500"> Начните бесплатную пробную подписку 14 дней</a>
                    </p>
                </div>
            </div>
            <button 
                onClick={toggleDarkMode} 
                className={`absolute top-4 right-4 p-2 rounded-md ${darkMode ? 'bg-gray-700 text-white' : 'bg-gray-200 text-gray-900'}`}>
                {darkMode ? 'Светлый режим' : 'Тёмный режим'}
            </button>
        </div>
    );
}

export default App;