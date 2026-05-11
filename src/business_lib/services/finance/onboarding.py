from business_lib.domain.interfaces import StoragePort
from pydantic import BaseModel, EmailStr, Field


# En enkel Pydantic-modell för validering
class CustomerOnboardingModel(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    income: float = Field(..., gt=0)


def execute_onboarding(customer_data: dict, storage: StoragePort):
    """
    Affärsprocess för att välkomna en ny kund.
    """
    # 1. Validera indata (Smäller direkt om data är felaktig)
    customer = CustomerOnboardingModel(**customer_data)

    # 2. Utför affärslogik (t.ex. sätt en initial status)
    enriched_data = customer.model_dump()
    enriched_data["status"] = "PENDING_APPROVAL"
    enriched_data["internal_tier"] = "GOLD" if customer.income > 50000 else "SILVER"

    # 3. Spara via Porten
    # Logiken vet inte OM det är SQL eller JSON, den bara anropar .save()
    storage.save(entity_id=customer.email, data=enriched_data)

    return f"Customer {customer.name} processed successfully."
