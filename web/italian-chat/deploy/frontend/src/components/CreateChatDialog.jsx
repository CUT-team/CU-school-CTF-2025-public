import {useContext, useRef, useState} from 'react'
import {Dialog} from 'primereact/dialog'
import {InputText} from 'primereact/inputtext'
import {Button} from 'primereact/button'
import {Toast} from 'primereact/toast'
import {api} from '../services/axios.js'
import {MessengerContext} from '../context/MessengerContext.jsx'

export const CreateChatDialog = ({visible, setVisible}) => {
    const toast = useRef(null)
    const [chatName, setChatName] = useState('')
    const {updateChats} = useContext(MessengerContext)

    const createHandler = () => {
        if (!chatName.trim()) {
            toast.current.show({
                severity: 'error',
                summary: 'Ошибка',
                detail: 'Заполните все поля',
                life: 3000,
            })
            return
        }

        api.post('/create_chat', {
            'name': chatName,
        }).then(() => {
            updateChats()
        }).catch((error) => {
            let detail = error.response.data.detail
            detail = typeof detail === 'string' ? detail : JSON.stringify(detail)
            toast.current.show({severity: 'error', summary: 'Ошибка', detail: detail, life: 3000})
        })

        setChatName('')
        setVisible(false)
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            createHandler()
        }
    }

    return (
        <>
            <Toast ref={toast} position="top-center"/>
            <Dialog
                header="Создать чат"
                visible={visible}
                draggable={false}
                resizable={false}
                onHide={() => setVisible(false)}
                style={{width: '100%', maxWidth: '370px'}}
            >
                <div className="flex flex-column gap-3">
                    <label htmlFor="chatname">
                        Название чата
                    </label>
                    <InputText
                        id="chatname"
                        value={chatName}
                        onKeyDown={handleKeyDown}
                        onChange={(e) => setChatName(e.target.value)}
                        className="w-full"
                    />

                    <Button
                        label="Создать"
                        onClick={createHandler}
                        className="w-full"
                    />
                </div>
            </Dialog>
        </>
    )
}