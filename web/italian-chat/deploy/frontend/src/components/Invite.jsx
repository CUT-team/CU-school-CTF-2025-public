import {Button} from 'primereact/button'
import {InputText} from 'primereact/inputtext'
import {Dialog} from 'primereact/dialog'
import {useContext, useRef, useState} from 'react'
import {api} from '../services/axios.js'
import {MessengerContext} from '../context/MessengerContext.jsx'
import {Toast} from 'primereact/toast'
import {AuthContext} from '../context/AuthContext.jsx'

export const Invite = () => {
    const toast = useRef(null)
    const [dialogVisible, setDialogVisible] = useState(false)
    const [username, setUsername] = useState('')
    const {currentChatId, chats} = useContext(MessengerContext)
    const {profile} = useContext(AuthContext)

    const inviteHandler = () => {
        if (!username.trim()) {
            toast.current.show({
                severity: 'error',
                summary: 'Ошибка',
                detail: 'Заполните все поля',
                life: 3000,
            })
            return
        }

        api.post('/invite', {
            chat_id: currentChatId,
            username: username,
        }).then(() => {
            toast.current.show({
                severity: 'success',
                summary: 'Пользователь добавлен',
                life: 3000,
            })
            setUsername('')
            setDialogVisible(false)
        }).catch((error) => {
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

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            inviteHandler()
        }
    }

    return (
        <>
            <Toast ref={toast} position="top-center"/>

            {chats.find((chat) => chat.chat_id === currentChatId && chat.owner === profile.username) ?
                <Button className="mr-3" label="Пригласить пользователя" icon="pi pi-plus"
                        onClick={() => setDialogVisible(true)}/> : ''}

            <Dialog
                header="Пригласить пользователя"
                visible={dialogVisible}
                draggable={false}
                resizable={false}
                onHide={() => setDialogVisible(false)}
                style={{width: '100%', maxWidth: '370px'}}
            >
                <div className="flex flex-column gap-3">
                    <label htmlFor="username">
                        Логин
                    </label>
                    <InputText
                        id="username"
                        value={username}
                        onKeyDown={handleKeyDown}
                        onChange={(e) => setUsername(e.target.value)}
                        className="w-full"
                    />

                    <Button
                        label="Пригласить"
                        onClick={inviteHandler}
                        className="w-full"
                    />
                </div>
            </Dialog>
        </>
    )
}