from .profile_handler import router as profile_router
from .register_handler import router as register_router
from .survey_handler import router as survey_router
from .view_handler import router as view_router
from .menu_handler import router as menu_router
from .admin_handler import router as admin_router
from .clear_handler import router as clear_router
handlers = [
    clear_router,
    profile_router,
    register_router,
    survey_router,
    view_router,
    menu_router,
    admin_router,
    
]