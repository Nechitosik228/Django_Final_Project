from accounts.models import Transaction, Balance


def create_transaction(balance: Balance, action, amount, category, status):
    Transaction.objects.create(
        balance=balance,
        money_amount=amount,
        category=category,
        action=action if action != None else 1,
        status=status if status != None else 1,
    )
