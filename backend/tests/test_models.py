from app.database import Base

def test_models_base_exists():
    assert Base is not None
