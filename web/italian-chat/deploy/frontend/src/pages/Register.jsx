import '../styles/Auth.css'
import {InputText} from 'primereact/inputtext'
import {Button} from 'primereact/button'
import {Toast} from 'primereact/toast'
import {useContext, useRef, useState} from 'react'

import {api} from '../services/axios.js'
import {useNavigate} from 'react-router-dom'
import {RadioButton} from 'primereact/radiobutton'
import {AuthContext} from '../context/AuthContext.jsx'

export const Register = () => {
    const navigate = useNavigate()
    const toast = useRef(null)

    const {login} = useContext(AuthContext)

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [avatar, setAvatar] = useState('')

    const avatars = [
        'https://i.imgur.com/HB50wXp.png',
        'https://i.imgur.com/VU2nGJ8.png',
        'https://i.imgur.com/eJw2sw1.png',
        'https://i.imgur.com/Gv1uke1.png',
        'https://i.imgur.com/UxP0C4S.png',
        'https://i.imgur.com/30KpDae.png',
    ]

    const loginHandler = (e) => {
        e.preventDefault()
        navigate('/login')
    }

    const registerHandler = (e) => {
        e.preventDefault()
        if (!username.trim() || !password.trim() || !avatar.trim()) {
            toast.current.show({
                severity: 'error',
                summary: 'Ошибка',
                detail: 'Заполните все поля',
                life: 3000,
            })
            return
        }
        api.post('/register', {
            'username': username,
            'password': password,
            'avatar_url': avatar,
        }).then(() => {
            login()
            navigate('/')
        }).catch((error) => {
            console.error(error)
            let detail = error.response.data.detail
            detail = typeof detail === 'string' ? detail : JSON.stringify(detail)
            toast.current.show({
                severity: 'error',
                summary: 'Ошибка',
                detail: detail,
                life: 3000,
            })
        })
    }

    return (
        <section className="auth">
            <Toast ref={toast} position="top-center"/>
            <form>
                <h1>Регистрация</h1>
                <div className="flex flex-column gap-2 mb-3">
                    <label htmlFor="username">Логин</label>
                    <InputText id="username" value={username} onChange={(e) => setUsername(e.target.value)}/>
                    <label htmlFor="password">Пароль</label>
                    <InputText id="password" type="password" value={password}
                               onChange={(e) => setPassword(e.target.value)}/>
                </div>

                <label>Аватар</label>

                <div className="flex flex-wrap gap-3 justify-content-center mb-3 mt-2">
                    {avatars.map((url, index) => (
                        <label
                            key={index}
                            htmlFor={`avatar${index}`}
                            className="flex align-items-center gap-2 cursor-pointer"
                            style={{width: '150px', justifyContent: 'start'}}
                        >
                            <RadioButton
                                inputId={`avatar${index}`}
                                name="avatar"
                                value={url}
                                onChange={(e) => setAvatar(e.value)}
                                checked={avatar === url}
                            />
                            <img
                                src={url}
                                alt={`Avatar ${index}`}
                                style={{width: '100px', height: '100px', objectFit: 'cover', borderRadius: '8px'}}
                            />
                        </label>
                    ))}
                </div>

                <Button onClick={registerHandler} className="mr-2">Регистрация</Button>
                <Button onClick={loginHandler} outlined>Вход</Button>
            </form>
        </section>
    )
}