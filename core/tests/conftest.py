import pytest
from random import randint
from fastapi.testclient import TestClient
from main import app
from core.database import Base, create_engine, sessionmaker, get_db
from sqlalchemy import StaticPool
from expenses.models import ExpenseModel
from users.models import UserModel
from auth.jwt_auth import generate_access_token
from faker import Faker

faker = Faker()


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="package")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="session", autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="package")
def anon_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="package")
def auth_client(db_session):
    client = TestClient(app)
    user = db_session.query(UserModel).filter_by(username="usertest").one()
    access_token = generate_access_token(user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest.fixture(scope="package", autouse=True)
def gen_mock_data(db_session):
    user = UserModel(username="usertest")
    user.set_password("87654321")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    expenses_list = []

    for _ in range(10):
        task = ExpenseModel(
            user_id=user.id,
            desc=faker.paragraph(nb_sentences=3),
            amount=randint(1, 500),
        )
        expenses_list.append(task)

    db_session.add_all(expenses_list)
    db_session.commit()


@pytest.fixture(scope="function")
def random_expense(db_session):
    user = db_session.query(UserModel).filter_by(username="usertest").one()
    task = db_session.query(ExpenseModel).filter_by(user_id=user.id).first()
    return task
