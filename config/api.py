from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from users.api import router as users_router
from courses.api import router as courses_router

api = NinjaExtraAPI(title="Simple LMS API", version="1.0.0", urls_namespace="api")

# Register JWT Controller
api.register_controllers(NinjaJWTDefaultController)

# Register routers
api.add_router("/auth", users_router, tags=["Authentication"])
api.add_router("/courses", courses_router, tags=["Courses & Enrollments"])

