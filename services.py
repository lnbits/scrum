from lnbits.core.models import Payment
from loguru import logger


async def payment_received_for_tasks(payment: Payment) -> bool:
    logger.info("Payment receive logic generation is disabled.")
    return True
