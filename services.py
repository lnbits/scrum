from lnbits.core.models import Payment
from lnbits.core.services import create_invoice
from loguru import logger

from .crud import (
    create_tasks,
    get_tasks_by_id,
    get_scrum_by_id,
    update_tasks,
)
from .models import (
    CreateTasks,
)




async def payment_received_for_tasks(payment: Payment) -> bool:
    logger.info("Payment receive logic generation is disabled.")
    return True


