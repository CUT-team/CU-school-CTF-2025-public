import {useContext} from 'react'
import {AuthContext} from '../context/AuthContext'
import {Navigate} from 'react-router-dom'

export const PrivateRoute = ({children}) => {
    const {isLoggedIn} = useContext(AuthContext)
    if (isLoggedIn === null) {
        return null
    }
    if (!isLoggedIn) {
        return <Navigate to="/login" replace/>
    }
    return children
}