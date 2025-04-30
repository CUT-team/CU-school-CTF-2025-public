import {useContext, useState} from 'react'
import {InputText} from 'primereact/inputtext'
import {Button} from 'primereact/button'
import {api} from '../services/axios.js'
import {MessengerContext} from '../context/MessengerContext.jsx'

export const SearchMessage = ({searchHandler}) => {
    const {currentChatId, setMessages, openChat} = useContext(MessengerContext)
    const [keyword, setKeyword] = useState('')

    const clickHandler = () => {
        searchHandler(keyword)
        if (!keyword.trim()) {
            openChat(currentChatId)
            return
        }
        api.post('/search_messages', {
            chat_id: currentChatId,
            keyword: keyword,
        }).then((r) => {
            setMessages(r.data)
        })
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            clickHandler()
        }
    }

    return (
        <div className="p-inputgroup flex-1">
            <InputText
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Поиск"
            />
            <Button icon="pi pi-search" onClick={clickHandler}/>
        </div>
    )
}