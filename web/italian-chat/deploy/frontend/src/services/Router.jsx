import {BrowserRouter, Route, Routes} from 'react-router-dom'
import {Main} from '../pages/Main.jsx'
import {Login} from '../pages/Login.jsx'
import {Register} from '../pages/Register.jsx'
import {PrivateRoute} from './PrivateRoute.jsx'

export const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<PrivateRoute><Main/></PrivateRoute>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/register" element={<Register/>}/>
            </Routes>
        </BrowserRouter>
    )
}