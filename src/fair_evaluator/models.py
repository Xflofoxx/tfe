from sqlalchemy import JSON, Column, Index, Integer, String, Text

from .db import Base


class Fair(Base):
    __tablename__ = "fairs"
    __table_args__ = (
        Index("idx_fair_status", "status"),
        Index("idx_fair_location", "location"),
        Index("idx_fair_name", "name"),
        Index("idx_fair_created", "id"),
    )

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    folder_path = Column(String, nullable=True)
    dates = Column(JSON, nullable=True)
    location = Column(String, nullable=True, index=True)
    target_segments = Column(JSON, nullable=True)
    expected_visitors = Column(Integer, nullable=True)
    exhibitors_count = Column(Integer, nullable=True)
    sources = Column(JSON, nullable=True)
    company_website = Column(String, nullable=True)
    company_linkedin = Column(String, nullable=True)
    fair_email = Column(String, nullable=True)
    gallery = Column(JSON, nullable=True)
    attachments = Column(JSON, nullable=True)
    contacts = Column(JSON, nullable=True)
    stand_cost = Column(Integer, nullable=True)
    status = Column(String, default="in_valutazione", index=True)
    scraped_data = Column(JSON, nullable=True)
    historical_data = Column(JSON, nullable=True)
    ROI_assessment = Column(JSON, nullable=True)
    cost_estimate = Column(JSON, nullable=True)
    recommendation = Column(String, nullable=True)
    rationale = Column(Text, nullable=True)
    report_pdf_path = Column(String, nullable=True)
    report_html_path = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    edition = Column(String, nullable=True)
    organizer = Column(String, nullable=True)
    sector = Column(String, nullable=True, index=True)
    exhibitor_countries = Column(JSON, nullable=True)
    visitor_profile = Column(Text, nullable=True)
    product_categories = Column(JSON, nullable=True)
    key_features = Column(JSON, nullable=True)
    venue = Column(String, nullable=True)
    address = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)

    def __repr__(self):
        return f"<Fair {self.name} ({self.id})>"


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    ollama_url = Column(String, default="http://localhost:11434")
    ollama_model = Column(String, default="llama3.2")
    strategy_prompt = Column(Text, nullable=True)
    strategy_pdf = Column(String, nullable=True)

    def __repr__(self):
        return f"<Settings id={self.id}>"
