# Import libraries
from flask import Flask,request,url_for,redirect,render_template
# Instantiate Flask functionality
app = Flask(__name__)
# Sample data

transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation

@app.route("/")
def get_transactions():
    return render_template("transactions.html",transactions=transactions)

# Create operation

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)
        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])
        
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))

    for transaction in transactions:
         if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction = transaction)

    return {"message":"Transaction not found"},404
    

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if(transaction['id'] == transaction_id):
            transactions.remove(transaction)
            break

    return redirect(url_for("get_transactions"))  

@app.route("/search",methods=["GET","POST"])
def search_transactions():

    if request.method == 'POST':
        filtered_transactions = []
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])
        for transaction in transactions:
            if min< transaction['amount'] <max:
                filtered_transactions.append(transaction)
                
        return render_template("transactions.html", transactions = filtered_transactions)
            
    return render_template("search.html")       


# Run the Flask app
    if __name__ == "__main__":
        app.run(debug=True)