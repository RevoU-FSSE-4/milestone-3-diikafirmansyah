# Milestone 3 - RevoU
1.⁠ ⁠To run the app, open terminal or command prompt then navigate to your project directory 
⁠ flask --app index run --debug ⁠

2.⁠ ⁠Open Postman then setup
⁠ IP: http://127.0.0.1:5000 ⁠
and ⁠ variable: url_base ⁠

3.⁠ ⁠Open MySQL Workbench setting:
•⁠  ⁠USERNAME=root
•⁠  ⁠PASSWORD=477035
•⁠  ⁠HOST=127.0.0.1
•⁠  ⁠DATABASE=milestone_3

### User Management:
•⁠  ⁠[POST] Register New User: Creates new user.

        {{url_base}}/register

•⁠  ⁠[GET] Get User Profile: Show profile of the currently authenticated user.

        {{url_base}}/users/me

•⁠  ⁠[PUT] Update User Profile: Update user  information of the currently authenticated user.

        {{url_base}}/users/me

•⁠  ⁠[POST] Login User: login from registered User using username, email and password.

        {{url_base}}/login

•⁠  ⁠[POST] Logout User: logout from currently authenticated User by revoking the token.

        {{url_base}}/logout

### Account Management:
•⁠  ⁠[POST] Register New Account: Creates new Account.

        {{url_base}}/accounts/register

•⁠  ⁠[GET] Get Account by ID: Retrieve details of a specific account by its ID. (Authorization required for account owner)

        {{url_base}}/accounts/<id>

•⁠  ⁠[GET] Get All Account Profile: Create a new account for the currently authenticated user.

        {{url_base}}/accounts

•⁠  ⁠[PUT]  Update Account: Update details of an existing account. (Authorization required for account owner)

        {{url_base}}/accounts/<id>

•⁠  ⁠[POST] Delete Account: Delete an existing account. (Authorization required for account owner)

        {{url_base}}/accounts/<id>

### Transaction Management:
•⁠  ⁠[GET] Get All Transactions: Retrieve a list of all transactions for the currently authenticated user's accounts. (Optional: filter by account ID)

        {{url_base}}/transactions

•⁠  ⁠[GET] Get Transaction by ID:  Retrieve details of a specific transaction by its ID. (Authorization required for related account owner)

        {{url_base}}/transactions/<id>

•⁠  ⁠[POST] Transactions: Initiate a new transaction.

        {{url_base}}/transactions

•⁠  ⁠[POST] Withdrawal: substract amount of money. (Authorization required for related account owner)

        {{url_base}}/transaction/withdrawal

•⁠  ⁠[POST] Deposit: Adding amount of money. (Authorization required for related account owner)

        {{url_base}}/transaction/deposit