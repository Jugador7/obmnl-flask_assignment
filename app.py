# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask("My first Application")

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    total_balance = sum(transaction['amount'] for transaction in transactions)  # Assuming each transaction is a dictionary with an 'amount' key
    return render_template('transactions.html', transactions=transactions, total_balance=total_balance)

# Create operation
@app.route("/add", methods=['GET','POST'])
def add_transaction():
    if request.method=='POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Render the form template to display the add transaction form
    return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods=['GET','POST'])
def edit_transaction(transaction_id):
    if request.method=='POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation

@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

#Show total transaction balance 
@app.route("/balance")
def total_balance():
    """calculates the total amount for all saved transactions
    Returns:
        total balance
    """
    for transaction in transactions:
        total_balance = transaction['amount'] + total_balance
    return {f"Total Balance : {total_balance}"}, 400

#Find transaction by amount range
@app.route("/search", methods=['GET','POST'])
def search_transactions():
    """Finds all transactions between certain amounts.
    Returns:
        HTML template: With transactions if found.
        Redirects: To a search page with error message if validation fails.
    """
    if request.method=='POST':
        try:
            min_amount = float(request.form['min_amount'])
            max_amount = float(request.form['max_amount'])
        except KeyError:
            # Redirects to the form page with an error if the necessary keys are not found in the form data.
            return redirect(url_for('search_form', error="Missing required fields")), 422
        except ValueError:
            # Redirects to the form page with an error if the values are not valid floats.
            return redirect(url_for('search_form', error="Invalid input types")), 400

        filtered_transactions = [
            transaction for transaction in transactions
            if float(transaction['amount']) >= min_amount and float(transaction['amount']) <= max_amount
        ]

        if filtered_transactions:
            return render_template("transactions.html", transactions=filtered_transactions)
        else:
            # Redirects to the form page with an error if no transactions are found.
            return redirect(url_for('search_form', error="No transactions found within the provided range")), 404
    return render_template("search.html")

@app.route("/search_form")
def search_form():
    error = request.args.get('error')
    return render_template("search.html", error=error)

# Run the Flask app

if __name__ == "__main__":
    app.run(debug=True)