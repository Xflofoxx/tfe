from .db import Base, engine
from .models import TagCategory

def init_default_tag_categories():
    """Initialize default tag categories as specified in the requirements."""
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if categories already exist
        existing_count = db.query(TagCategory).count()
        if existing_count > 0:
            print(f"Tag categories already initialized ({existing_count} categories found)")
            return

        # Create default categories as per specifications
        default_categories = [
            # Business categories
            {"name": "Company", "description": "Company-related attributes", "color": "#3b82f6", "icon": "building"},
            {"name": "Industry", "description": "Industry sectors", "color": "#10b981", "icon": "industry"},
            {"name": "Strategy", "description": "Business strategies", "color": "#f59e0b", "icon": "target"},
            {"name": "Goals", "description": "Business objectives", "color": "#ef4444", "icon": "bullseye"},
            {"name": "Budget", "description": "Budget-related tags", "color": "#8b5cf6", "icon": "dollar-sign"},

            # Product categories
            {"name": "Product Type", "description": "Types of products/services", "color": "#06b6d4", "icon": "package"},
            {"name": "Price Range", "description": "Pricing categories", "color": "#84cc16", "icon": "tag"},
            {"name": "Innovation", "description": "Innovation levels", "color": "#f97316", "icon": "lightbulb"},

            # Market categories
            {"name": "Target Market", "description": "Target market segments", "color": "#ec4899", "icon": "users"},
            {"name": "Geography", "description": "Geographic regions", "color": "#6366f1", "icon": "map"},
            {"name": "Channel", "description": "Sales/marketing channels", "color": "#14b8a6", "icon": "shopping-cart"},
        ]

        for cat_data in default_categories:
            category = TagCategory(
                name=cat_data["name"],
                description=cat_data["description"],
                color=cat_data["color"],
                icon=cat_data["icon"],
                created_at="2026-04-20T10:00:00Z"
            )
            db.add(category)

        db.commit()
        print(f"Initialized {len(default_categories)} default tag categories")

    except Exception as e:
        print(f"Error initializing tag categories: {e}")
        db.rollback()
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize default data
init_default_tag_categories()
