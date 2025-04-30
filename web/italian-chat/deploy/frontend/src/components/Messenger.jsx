import '../styles/Messenger.css'
import {ChatsList} from './ChatsList.jsx'
import {useContext, useEffect, useRef, useState} from 'react'
import {MessengerContext} from '../context/MessengerContext.jsx'
import {MessagesList} from './MessagesList.jsx'
import {SendMessage} from './SendMessage.jsx'
import {SearchMessage} from './SearchMessage.jsx'
import {Invite} from './Invite.jsx'

export const Messenger = () => {
    const {currentChatId, messages, updateChats} = useContext(MessengerContext)
    const messagesListRef = useRef(null)
    const [keyword, setKeyword] = useState('')

    useEffect(() => {
        updateChats()
    }, [])

    const scrollDown = () => {
        if (messagesListRef.current) {
            messagesListRef.current.scrollTop = messagesListRef.current.scrollHeight
        }
    }

    return (
        <section className="messenger">
            <div className="messenger-wrapper">
                <ChatsList scrollDown={scrollDown}/>
                {currentChatId ? <div className="chat-wrapper">
                    <div className="flex justify-content-between align-items-center p-3">
                        <Invite/>
                        {(messages && messages.length > 0) || keyword ?
                            <SearchMessage searchHandler={(keyword) => setKeyword(keyword)}/> : ''}
                    </div>
                    <MessagesList ref={messagesListRef}/>
                    <SendMessage/>
                </div> : ''}
            </div>
        </section>
    )
}