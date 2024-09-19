import fastapi as fa

# Define root api router
router = fa.APIRouter(prefix="/api")

# Versioned routers
v1_router = fa.APIRouter(prefix="/v1")

router.include_router(v1_router)
