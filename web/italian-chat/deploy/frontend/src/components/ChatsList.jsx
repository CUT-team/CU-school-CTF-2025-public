import {useContext, useEffect} from 'react'
import {MessengerContext} from '../context/MessengerContext.jsx'

export const ChatsList = ({scrollDown}) => {
    const {chats, openChat, messages} = useContext(MessengerContext)

    const handler = (chatId) => {
        openChat(chatId)
    }

    useEffect(() => {
        if (messages !== null) {
            scrollDown()
        }
    }, [messages])

    return (
        <div className="chats-list">
            {chats !== null ? chats.map((chat, index) => (
                <div key={index} className="chat-item" onClick={() => handler(chat.chat_id)}>{chat.name}</div>
            )) : <></>}
        </div>
    )
}