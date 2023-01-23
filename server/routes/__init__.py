from fastapi import APIRouter

router=APIRouter()
from .auth import router as auth
router.include_router(auth, prefix="/auth")
from .user import router as user
router.include_router(user, prefix="/user")
from .organization import router as organization
router.include_router(organization, prefix="/organization")
from .project import router as project
router.include_router(project, prefix="/project")
from .task import router as task
router.include_router(task, prefix="/task")