class ExpenseNotFoundError(Exception):
    def __init__(self, expense_id: int):
        self.status_code = 404
        self.expense_id = expense_id
        self.message = f"Expense with ID {expense_id} not found."
        super().__init__(self.message)
