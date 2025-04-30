import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import {PrimeReactProvider} from 'primereact/api'

import 'primereact/resources/themes/lara-light-indigo/theme.css'
import 'primereact/resources/primereact.min.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css'

import './styles/style.css'
import {Router} from './services/Router.jsx'
import {Providers} from './services/Providers.jsx'

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <PrimeReactProvider>
            <Providers>
                <Router/>
            </Providers>
        </PrimeReactProvider>
    </StrictMode>,
)
