import {AuthProvider} from '../context/AuthContext.jsx'
import {MessengerProvider} from '../context/MessengerContext.jsx'
import {AvatarProvider} from '../context/AvatarContext.jsx'

export const Providers = ({children}) => {
    return (
        <AuthProvider>
            <MessengerProvider>
                <AvatarProvider>
                    {children}
                </AvatarProvider>
            </MessengerProvider>
        </AuthProvider>
    )
}