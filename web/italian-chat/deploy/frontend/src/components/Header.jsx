import {useContext, useState} from 'react'
import {AuthContext} from '../context/AuthContext'
import {useNavigate} from 'react-router-dom'
import {Button} from 'primereact/button'
import {CreateChatDialog} from './CreateChatDialog.jsx'

export const Header = () => {
    const {logout} = useContext(AuthContext)
    const navigate = useNavigate()

    const [dialogVisible, setDialogVisible] = useState(false)

    const logoutHandler = () => {
        logout()
        navigate('/login')
    }

    return (
        <>
            <header className="flex justify-content-between align-items-center p-3 pl-4 pr-4 shadow-2">
                <div className="text-2xl font-bold">Italian Chat</div>
                <div>
                    <Button className="mr-3" label="Создать чат" icon="pi pi-plus"
                            onClick={() => setDialogVisible(true)}/>
                    <Button className="p-button-danger" outlined label="Выйти" icon="pi pi-sign-out"
                            onClick={logoutHandler}/>
                </div>
            </header>
            <CreateChatDialog visible={dialogVisible} setVisible={setDialogVisible}/>
        </>
    )
}
