from fastapi import FastAPI
from app.user.routers import auth_router, profile_router, verification_router
from app.tenant.routers import tenant_router
from app.project.routers import project_router


# main app
app = FastAPI()


# add routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(verification_router)
app.include_router(tenant_router)
app.include_router(project_router)
