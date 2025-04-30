import '../styles/Auth.css'
import {InputText} from 'primereact/inputtext'
import {Button} from 'primereact/button'
import {Toast} from 'primereact/toast'
import {useContext, useRef, useState} from 'react'

import {api} from '../services/axios.js'
import {useNavigate} from 'react-router-dom'
import {AuthContext} from '../context/AuthContext.jsx'

export const Login = () => {
    const navigate = useNavigate()
    const toast = useRef(null)
    const {login} = useContext(AuthContext)

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const loginHandler = (e) => {
        e.preventDefault()
        if (!username.trim() || !password.trim()) {
            toast.current.show({
                severity: 'error',
                summary: 'Ошибка',
                detail: 'Заполните все поля',
                life: 3000,
            })
            return
        }
        api.post('/login', {
            'username': username,
            'password': password,
        }).then(() => {
            login()
            navigate('/')
        }).catch((error) => {
            console.error(error)
            let detail = error.response.data.detail
            detail = typeof detail === 'string' ? detail : JSON.stringify(detail)
            toast.current.show({severity: 'error', summary: 'Ошибка', detail: detail, life: 3000})
        })
    }

    const registerHandler = (e) => {
        e.preventDefault()
        navigate('/register')
    }

    return (
        <section className="auth">
            <Toast ref={toast} position="top-center"/>
            <form>
                <h1>Вход</h1>
                <div className="flex flex-column gap-2 mb-3">
                    <label htmlFor="username">Логин</label>
                    <InputText id="username" value={username} onChange={(e) => setUsername(e.target.value)}/>
                    <label htmlFor="password">Пароль</label>
                    <InputText id="password" type="password" value={password}
                               onChange={(e) => setPassword(e.target.value)}/>
                </div>
                <Button onClick={loginHandler} className="mr-2">Вход</Button>
                <Button onClick={registerHandler} outlined>Регистрация</Button>
            </form>
        </section>
    )
}