from src.shared.entities.basemodel import BaseModel
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime, ForeignKey, String, Integer, func, text

class DealerForecastModel(BaseModel):
    __tablename__ = "va_dealer_forecast_model"

    id = mapped_column(String(255), primary_key=True, nullable=False)
    # AMBIGOUS with dealer_forecast
    dealer_forecast_id = mapped_column(String(255), ForeignKey('va_dealer_forecast.id'),nullable=False)
    model_id = mapped_column(String(255), ForeignKey('va_models.id'),nullable=False)
    dealer_end_stock = mapped_column(Integer, nullable=False)
    # created_by = mapped_column(
    #     String(255),
    #     ForeignKey("va_users.id"),
    #     nullable=True,
    # )
     # updated_by = mapped_column(
    #     String(255),
    #     ForeignKey("va_users.id"),
    #     nullable=True,
    # )
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    deletable = mapped_column(Integer, server_default=text("0"))