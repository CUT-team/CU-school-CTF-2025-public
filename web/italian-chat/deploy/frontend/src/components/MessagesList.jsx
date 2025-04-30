import {useContext, forwardRef} from 'react'
import {MessengerContext} from '../context/MessengerContext.jsx'
import {Message} from './Message.jsx'

export const MessagesList = forwardRef((props, ref) => {
    const {messages} = useContext(MessengerContext)

    return (
        <div ref={ref} className="messages-list">
            {messages === null ? '' : messages.length > 0 ? messages.map((message, index) => (
                <Message key={index} data={message}/>
            )) : <span>Сообщений нет</span>}
        </div>
    )
})