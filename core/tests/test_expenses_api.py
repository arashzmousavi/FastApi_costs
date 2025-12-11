def test_get_expense_item_reponse_404(anon_client):
    response = anon_client.get("/expenses/999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] is True
    assert "Expense with ID 999 not found." in data["message"]


def test_delete_expense_item_reponse_404(auth_client):
    response = auth_client.delete("/expenses/delete/999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] is True
    assert "Expense with ID 999 not found." in data["message"]


def test_delete_existing_expense(auth_client, random_expense):
    expense_id = random_expense.id
    response = auth_client.delete(f"/expenses/delete/{expense_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
