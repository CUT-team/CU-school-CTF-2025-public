import {createContext, useState} from 'react'
import {api} from '../services/axios.js'

export const MessengerContext = createContext(null)

export const MessengerProvider = ({children}) => {
    const [currentChatId, setCurrentChatId] = useState(null)
    const [messages, setMessages] = useState(null)
    const [chats, setChats] = useState(null)

    const updateChats = () => {
        api.get('/chats').then((r) => {
            setChats(r.data.filter((chat) => !chat.forbidden))
        })
    }

    const openChat = (chatId) => {
        setCurrentChatId(chatId)
        return new Promise((resolve, reject) => {
            api.get(`/messages/${chatId}`)
                .then((r) => {
                    setMessages(r.data)
                    resolve()
                })
                .catch(reject)
        })
    }

    return (
        <MessengerContext.Provider value={{chats, messages, openChat, updateChats, currentChatId, setMessages}}>
            {children}
        </MessengerContext.Provider>
    )
}