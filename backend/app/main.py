from fastapi import FastAPI
from app.user.routers import auth_router, profile_router, verification_router


# main app
app = FastAPI()


# add routers
app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(verification_router.router)
