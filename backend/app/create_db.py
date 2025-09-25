from app.models import Base, engine

Base.metadata.create_all(bind=engine)
print('Database and tables created!')