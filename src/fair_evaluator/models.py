from sqlalchemy import (
    JSON,
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from .db import Base

fair_contacts = Table(
    'fair_contacts', Base.metadata,
    Column('fair_id', String, ForeignKey('fairs.id'), primary_key=True),
    Column('contact_id', Integer, ForeignKey('contacts.id'), primary_key=True),
    Column('role', String, nullable=True),
    Column('notes', Text, nullable=True),
)

fair_tags = Table(
    'fair_tags', Base.metadata,
    Column('fair_id', String, ForeignKey('fairs.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
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


class TagCategory(Base):
    __tablename__ = "tag_categories"
    __table_args__ = (Index("idx_tag_category_name", "name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    color = Column(String, default="#3b82f6")
    icon = Column(String, nullable=True)  # fontawesome icon name
    parent_id = Column(Integer, ForeignKey('tag_categories.id'), nullable=True)
    created_at = Column(String, nullable=True)

    # Relationships
    parent = relationship("TagCategory", remote_side=[id], backref="children")
    tags = relationship("Tag", back_populates="category_obj")

    def __repr__(self):
        return f"<TagCategory {self.name}>"


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (Index("idx_tag_name", "name"), Index("idx_tag_category", "category_id"))

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String, default="#3b82f6")
    category_id = Column(Integer, ForeignKey('tag_categories.id'), nullable=True)

    # Advanced features
    tag_type = Column(String, default="user")  # 'user' or 'system'
    usage_count = Column(Integer, default=0)
    ai_confidence = Column(Float, nullable=True)  # for AI-generated tags
    created_by = Column(Integer, nullable=True)  # user ID who created it
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)

    # Relationships
    category_obj = relationship("TagCategory", back_populates="tags")
    fairs = relationship("Fair", secondary=fair_tags, back_populates="tags")

    @property
    def category(self):
        """Backward compatibility property"""
        return self.category_obj.name if self.category_obj else None

    def __repr__(self):
        return f"<Tag {self.name} (type: {self.tag_type})>"


class TagAnalytics(Base):
    __tablename__ = "tag_analytics"
    __table_args__ = (
        Index("idx_tag_analytics_tag", "tag_id"),
        Index("idx_tag_analytics_fair", "fair_id"),
        Index("idx_tag_analytics_timestamp", "timestamp")
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    fair_id = Column(String, ForeignKey('fairs.id'), nullable=True)
    action = Column(String, nullable=False)  # 'added', 'removed', 'suggested', 'merged'
    timestamp = Column(String, nullable=False)

    # Relationships
    tag = relationship("Tag", backref="analytics")
    fair = relationship("Fair", backref="tag_analytics")

    def __repr__(self):
        return f"<TagAnalytics {self.action} on tag {self.tag_id}>"


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
    duration_days = Column(Integer, nullable=True)
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
    web_sources = Column(JSON, nullable=True)
    extraction_regions = Column(JSON, nullable=True)
    company_website = Column(String, nullable=True)
    company_linkedin = Column(String, nullable=True)
    fair_email = Column(String, nullable=True)
    gallery = Column(JSON, nullable=True)
    attachments = Column(JSON, nullable=True)
    contacts = Column(JSON, nullable=True)
    stand_cost = Column(Integer, nullable=True)
    status = Column(String, default="in_valutazione", index=True)
    archived = Column(String, default="no")
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
    ai_analysis_enabled = Column(String, default="no")
    ai_last_updated = Column(String, nullable=True)

    contact_list = relationship("Contact", secondary=fair_contacts, back_populates="fairs")
    tags = relationship("Tag", secondary=fair_tags, back_populates="fairs")
    previous_editions = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Fair {self.name} {self.year} ({self.id})>"


class Settings(Base):
    __tablename__ = "settings"
    __table_args__ = (Index("idx_settings_id", "id"),)

    id = Column(Integer, primary_key=True)

    # AI & LLM Settings
    ollama_url = Column(String, default="http://localhost:11434")
    ollama_model = Column(String, default="llama3.2")
    ollama_timeout = Column(Integer, default=120)  # seconds
    ollama_fallback_enabled = Column(String, default="yes")

    # Business Strategy
    strategy_prompt = Column(Text, nullable=True)
    strategy_pdf_path = Column(String, nullable=True)
    business_objectives = Column(Text, nullable=True)
    target_markets = Column(JSON, nullable=True)
    annual_budget = Column(Float, nullable=True)
    participation_criteria = Column(JSON, nullable=True)

    # UI Preferences
    ui_theme = Column(String, default="light")  # light, dark, auto
    ui_compact_mode = Column(String, default="no")
    notifications_enabled = Column(String, default="yes")
    email_notifications = Column(String, default="yes")
    language = Column(String, default="it")

    # System Settings
    max_upload_size = Column(Integer, default=10485760)  # 10MB in bytes
    max_files_per_fair = Column(Integer, default=50)
    cache_ttl = Column(Integer, default=3600)  # seconds
    background_jobs_concurrency = Column(Integer, default=5)
    password_policy = Column(JSON, nullable=True)
    session_timeout = Column(Integer, default=3600)  # seconds
    audit_logging = Column(String, default="yes")

    # Integrations
    webhooks_enabled = Column(String, default="no")
    webhook_url = Column(String, nullable=True)
    webhook_secret = Column(String, nullable=True)
    api_keys = Column(JSON, nullable=True)  # list of active API keys

    # Legacy fields (for backward compatibility)
    default_network_path = Column(String, nullable=True)

    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)

    def __repr__(self):
        return f"<Settings id={self.id}>"
