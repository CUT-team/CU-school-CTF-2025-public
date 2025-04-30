import {createContext, useRef, useState} from 'react'
import {api} from '../services/axios.js'

export const AvatarContext = createContext(null)

export const AvatarProvider = ({children}) => {
    const [cache, setCache] = useState({})
    const pendingRequests = useRef({})

    const getAvatarUrl = (username) => {
        if (cache[username]) {
            return Promise.resolve(cache[username])
        }

        if (pendingRequests.current[username]) {
            return pendingRequests.current[username]
        }

        const request = api.get(`/avatar/${username}`).then((r) => {
            const avatarUrl = r.data.avatar_url
            setCache((prevCache) => ({
                ...prevCache,
                [username]: avatarUrl,
            }))
            return avatarUrl
        }).finally(() => {
            delete pendingRequests.current[username]
        })

        pendingRequests.current[username] = request
        return request
    }

    return (
        <AvatarContext.Provider value={{getAvatarUrl}}>
            {children}
        </AvatarContext.Provider>
    )
}
