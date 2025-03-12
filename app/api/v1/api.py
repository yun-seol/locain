from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, campaigns, social_channels, reviews,
    payments, categories, coupons, points
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(social_channels.router, prefix="/social-channels", tags=["social-channels"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(coupons.router, prefix="/coupons", tags=["coupons"])
api_router.include_router(points.router, prefix="/points", tags=["points"]) 