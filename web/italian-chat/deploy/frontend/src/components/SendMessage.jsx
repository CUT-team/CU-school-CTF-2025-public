import {useContext, useState} from 'react'
import {InputText} from 'primereact/inputtext'
import {Button} from 'primereact/button'
import {api} from '../services/axios.js'
import {MessengerContext} from '../context/MessengerContext.jsx'

export const SendMessage = () => {
    const {currentChatId, openChat} = useContext(MessengerContext)
    const [message, setMessage] = useState('')

    const sendHandler = () => {
        if (!message.trim()) return
        setMessage('')
        api.post('/send_message', {
            chat_id: currentChatId,
            text: message,
        }).then(() => {
            openChat(currentChatId)
        })
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            sendHandler()
        }
    }

    return (
        <div className="p-inputgroup flex-1 p-3">
            <InputText
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Сообщение..."
            />
            <Button icon="pi pi-send" onClick={sendHandler}/>
        </div>
    )
}