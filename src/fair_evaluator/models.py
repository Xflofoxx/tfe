from sqlalchemy import JSON, Column, Index, Integer, String, Text, ForeignKey, Table, Float, Date
from sqlalchemy.orm import relationship

from .db import Base


fair_contacts = Table(
    'fair_contacts', Base.metadata,
    Column('fair_id', String, ForeignKey('fairs.id'), primary_key=True),
    Column('contact_id', Integer, ForeignKey('contacts.id'), primary_key=True),
    Column('role', String, nullable=True),
    Column('notes', Text, nullable=True),
)


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (Index("idx_contact_email", "email"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    role = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(String, nullable=True)

    fairs = relationship("Fair", secondary=fair_contacts, back_populates="contact_list")

    def __repr__(self):
        return f"<Contact {self.name} ({self.email})>"


class CommercialProposal(Base):
    __tablename__ = "commercial_proposals"
    __table_args__ = (
        Index("idx_proposal_fair", "fair_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    fair_id = Column(String, ForeignKey('fairs.id'), nullable=False)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    stand_size = Column(Integer, nullable=True)
    stand_location = Column(String, nullable=True)
    services = Column(JSON, nullable=True)
    status = Column(String, default="ricevuta")
    notes = Column(Text, nullable=True)
    received_at = Column(String, nullable=True)
    expires_at = Column(String, nullable=True)
    
    fair = relationship("Fair", backref="commercial_proposals")

    def __repr__(self):
        return f"<CommercialProposal {self.name} for {self.fair_id}>"


class FairAnalysis(Base):
    __tablename__ = "fair_analyses"
    __table_args__ = (
        Index("idx_analysis_fair", "fair_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    fair_id = Column(String, ForeignKey('fairs.id'), nullable=False)
    name = Column(String, nullable=True)
    parameters = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(String, nullable=True)
    
    fair = relationship("Fair", backref="analyses")

    def __repr__(self):
        return f"<FairAnalysis {self.id} for {self.fair_id}>"


class OfferComponent(Base):
    __tablename__ = "offer_components"
    __table_args__ = (
        Index("idx_component_fair", "fair_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    fair_id = Column(String, ForeignKey('fairs.id'), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(String, nullable=True)
    
    fair = relationship("Fair", backref="offer_components")

    def __repr__(self):
        return f"<OfferComponent {self.name} for {self.fair_id}>"


class Fair(Base):
    __tablename__ = "fairs"
    __table_args__ = (
        Index("idx_fair_status", "status"),
        Index("idx_fair_location", "location"),
        Index("idx_fair_name_year", "name", "year"),
        Index("idx_fair_created", "id"),
    )

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=False, default=2025)
    url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    folder_path = Column(String, nullable=True)
    network_path = Column(String, nullable=True)
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

    contact_list = relationship("Contact", secondary=fair_contacts, back_populates="fairs")
    previous_editions = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Fair {self.name} {self.year} ({self.id})>"


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    ollama_url = Column(String, default="http://localhost:11434")
    ollama_model = Column(String, default="llama3.2")
    strategy_prompt = Column(Text, nullable=True)
    strategy_pdf = Column(String, nullable=True)
    default_network_path = Column(String, nullable=True)

    def __repr__(self):
        return f"<Settings id={self.id}>"