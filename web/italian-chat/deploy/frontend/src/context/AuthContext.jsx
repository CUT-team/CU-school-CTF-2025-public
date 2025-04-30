import {createContext, useState, useEffect} from 'react'
import {api} from '../services/axios.js'

export const AuthContext = createContext(null)

export const AuthProvider = ({children}) => {
    const [isLoggedIn, setIsLoggedIn] = useState(null)
    const [profile, setProfile] = useState(null)

    useEffect(() => {
        setIsLoggedIn(localStorage.getItem('isLoggedIn') === 'true')
        setProfile(JSON.parse(localStorage.getItem('profile')))
    }, [])

    const login = () => {
        setIsLoggedIn(true)
        localStorage.setItem('isLoggedIn', 'true')
        api.get('/profile').then((r) => {
            setProfile(r.data)
            localStorage.setItem('profile', JSON.stringify(r.data))
        })
    }

    const logout = () => {
        api.post('/logout')
        setIsLoggedIn(false)
        localStorage.setItem('isLoggedIn', 'false')
    }

    return (
        <AuthContext.Provider value={{isLoggedIn, login, logout, profile}}>
            {children}
        </AuthContext.Provider>
    )
}
