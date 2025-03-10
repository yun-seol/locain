from typing import Optional, Dict, Any, List
import requests
import json
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.payment import Payment, PaymentStatus
from sqlalchemy.orm import Session
import logging
import asyncio
import httpx
from app.schemas.payment import PaymentWebhook, PaymentStats, PaymentCreate, PaymentUpdate
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class IamportPayment:
    def __init__(self):
        self.api_key = settings.IAMPORT_API_KEY
        self.api_secret = settings.IAMPORT_API_SECRET
        self.base_url = "https://api.iamport.kr"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _generate_signature(self, data: str) -> str:
        """iamport 요청에 필요한 서명을 생성합니다."""
        return base64.b64encode(
            hmac.new(
                self.api_secret.encode('utf-8'),
                data.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')

    def _encrypt_card_info(self, card_info: Dict[str, Any]) -> Dict[str, Any]:
        """카드 정보를 암호화합니다."""
        # 실제 운영 환경에서는 iamport의 카드 정보 암호화 API를 사용해야 합니다
        return {
            "card_number": self._encrypt_field(card_info.get("card_number")),
            "expiry": self._encrypt_field(card_info.get("expiry")),
            "birth": self._encrypt_field(card_info.get("birth")),
            "pwd_2digit": self._encrypt_field(card_info.get("pwd_2digit"))
        }

    def _encrypt_field(self, value: str) -> str:
        """개별 필드를 암호화합니다."""
        # 실제 운영 환경에서는 더 강력한 암호화 방식을 사용해야 합니다
        return hashlib.sha256(value.encode()).hexdigest()

    async def prepare_payment(self, payment: Payment) -> Dict[str, Any]:
        """결제 준비 요청을 보냅니다."""
        data = {
            "merchant_uid": f"payment_{payment.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "amount": payment.amount,
            "currency": payment.currency,
            "name": f"캠페인 결제 - {payment.campaign_application.campaign.title}",
            "buyer_name": payment.brand.username,
            "buyer_email": payment.brand.email,
            "buyer_tel": payment.brand.phone,
            "buyer_addr": payment.brand.address,
            "buyer_postcode": payment.brand.postal_code,
            "vbank_due": (datetime.now() + timedelta(days=1)).strftime("%Y%m%d%H%M%S"),
            "notify_url": f"{settings.BASE_URL}/api/v1/payments/webhook",
            "return_url": f"{settings.FRONTEND_URL}/payment/complete/{payment.id}"
        }

        response = requests.post(
            f"{self.base_url}/payments/prepare",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    async def process_payment(self, payment: Payment, payment_method_data: Dict[str, Any]) -> Dict[str, Any]:
        """실제 결제를 처리합니다."""
        if payment.payment_method == "credit_card":
            payment_method_data = self._encrypt_card_info(payment_method_data)

        data = {
            "merchant_uid": f"payment_{payment.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "amount": payment.amount,
            "currency": payment.currency,
            "payment_method": payment.payment_method,
            "payment_method_data": payment_method_data,
            "name": f"캠페인 결제 - {payment.campaign_application.campaign.title}",
            "buyer_name": payment.brand.username,
            "buyer_email": payment.brand.email,
            "buyer_tel": payment.brand.phone,
            "buyer_addr": payment.brand.address,
            "buyer_postcode": payment.brand.postal_code,
            "notify_url": f"{settings.BASE_URL}/api/v1/payments/webhook",
            "return_url": f"{settings.FRONTEND_URL}/payment/complete/{payment.id}"
        }

        response = requests.post(
            f"{self.base_url}/payments/process",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    async def verify_payment(self, payment: Payment, imp_uid: str) -> bool:
        """결제를 검증합니다."""
        response = requests.get(
            f"{self.base_url}/payments/{imp_uid}",
            headers=self.headers
        )
        response.raise_for_status()
        payment_data = response.json()

        # 결제 금액 검증
        if payment_data["amount"] != payment.amount:
            return False

        # 결제 상태 검증
        if payment_data["status"] != "paid":
            return False

        # 가맹점 검증
        if payment_data["merchant_uid"] != f"payment_{payment.id}":
            return False

        return True

    async def cancel_payment(self, payment: Payment, reason: str) -> Dict[str, Any]:
        """결제를 취소합니다."""
        data = {
            "reason": reason,
            "refund_holder": payment.brand.username,
            "refund_bank": payment.refund_bank,
            "refund_account": payment.refund_account
        }

        response = requests.post(
            f"{self.base_url}/payments/cancel/{payment.transaction_id}",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

async def process_payment_with_retry(
    db: Session,
    payment: Payment,
    payment_method_data: Dict[str, Any],
    max_retries: int = 3
) -> bool:
    """결제 처리를 재시도 로직과 함께 수행합니다."""
    iamport = IamportPayment()
    
    for attempt in range(max_retries):
        try:
            # 결제 준비
            prepare_result = await iamport.prepare_payment(payment)
            
            # 결제 처리
            process_result = await iamport.process_payment(payment, payment_method_data)
            
            # 결제 검증
            if await iamport.verify_payment(payment, process_result["imp_uid"]):
                # 결제 성공 처리
                payment.status = PaymentStatus.COMPLETED
                payment.transaction_id = process_result["imp_uid"]
                payment.payment_date = datetime.now()
                payment.updated_at = datetime.now()
                
                db.add(payment)
                db.commit()
                return True
            
            # 결제 검증 실패
            payment.status = PaymentStatus.FAILED
            payment.updated_at = datetime.now()
            db.add(payment)
            db.commit()
            return False
            
        except Exception as e:
            logger.error(f"Payment processing attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                payment.status = PaymentStatus.FAILED
                payment.updated_at = datetime.now()
                db.add(payment)
                db.commit()
                return False
            await asyncio.sleep(1)  # 재시도 전 대기

    return False

async def send_webhook_with_retry(
    payment: Payment,
    max_retries: int = 3,
    retry_delay: int = 1
) -> bool:
    """웹훅 전송을 재시도 로직과 함께 수행합니다."""
    for attempt in range(max_retries):
        try:
            webhook_data = PaymentWebhook(
                payment_id=payment.id,
                status=payment.status,
                transaction_id=payment.transaction_id,
                payment_date=payment.payment_date,
                amount=payment.amount,
                currency=payment.currency,
                payment_method=payment.payment_method,
                metadata={
                    "campaign_application_id": payment.campaign_application_id,
                    "brand_id": payment.brand_id,
                    "influencer_id": payment.influencer_id
                }
            )
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.PAYMENT_WEBHOOK_URL,
                    json=webhook_data.dict(),
                    headers={"Authorization": f"Bearer {settings.PAYMENT_WEBHOOK_SECRET}"}
                )
                response.raise_for_status()
                return True
                
        except Exception as e:
            logger.error(f"Webhook delivery attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                return False
    
    return False

def calculate_payment_stats(db: Session, payment: Payment) -> PaymentStats:
    """결제 통계 정보를 계산합니다."""
    return PaymentStats(
        total_amount=payment.amount,
        status=payment.status,
        created_at=payment.created_at,
        updated_at=payment.updated_at,
        payment_method=payment.payment_method,
        transaction_id=payment.transaction_id,
        refund_status=payment.refund_status,
        refund_amount=payment.refund_amount,
        refund_reason=payment.refund_reason,
        refund_date=payment.refund_date
    ) 