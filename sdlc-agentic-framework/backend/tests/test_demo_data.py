from app.api.routes import demo_data


def test_demo_data_exposes_existing_leave_fixture():
    data = demo_data()
    assert data["requirements"][0]["name"] == "Employee Leave Management System"
    assert len(data["existing_data"]["employees"]) == 4
    assert data["existing_data"]["leave_balances"][0] == {
        "employee_id": "E001",
        "days": 12,
    }
