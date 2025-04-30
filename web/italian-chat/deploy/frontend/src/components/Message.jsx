import {useContext, useEffect, useState} from 'react'
import {AuthContext} from '../context/AuthContext.jsx'
import {AvatarContext} from '../context/AvatarContext.jsx'

export const Message = ({data}) => {
    const {profile} = useContext(AuthContext)
    const {getAvatarUrl} = useContext(AvatarContext)
    const [avatarUrl, setAvatarUrl] = useState(null)

    useEffect(() => {
        getAvatarUrl(data.sender).then((data) => {
            setAvatarUrl(data)
        })
    }, [])

    return (
        <div className={`message ${profile.username === data.sender ? 'out' : ''}`}>
            <img className="avatar" src={avatarUrl}/>
            <div>
                <p className="sender">{data.sender}</p>
                <p className="text">{data.text}</p>
            </div>
        </div>
    )
}