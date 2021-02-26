

[![Build Status](https://i.ibb.co/VTLVs4N/tergum-green-4.png)]()

Step -1
open command prompt and cd into the base directory and install the dependencies-
```sh
pip install requirements.txt
```
Step -2
Run the VPS
```sh
python manage.py runserver 8000
```
Note- Make sure the port for VPS is  8000

Step -3
Go to http://127.0.0.1:8000 from your browser and make sure it shows the home screen (everything works)

Step-4 
Go to http://127.0.0.1:8000/admin and use these credentials to get into the admin panel-
| username | password |
| ------ | ------ |
|  admin@tergum.com  | tergum |

Step -4
Set-up stripe CLI,

Stripe uses webhooks to notify your application when an event happens 
in your account. Webhooks are particularly useful for asynchronous 
events like when a customer’s bank confirms a payment, a customer 
disputes a charge, or a recurring payment succeeds

We also use this to get confirmation fo our payments for which, we need to listen to stripe's webhooks on our localhost for which we would need to configure stipe CLI.

Here's how-
1. Download the latest windows file from https://github.com/stripe/stripe-cli/releases/latest
2. Unzip the file.
3. Run “stripe.exe” from cmd
4. Execute “stripe login” in the console. 
5. You will be prompted to the browser by pressing the enter key to filling in your credential in order to grant Stripe CLI access to your account. 
Login id-->sanidhyaagrawal08@gmail.com
Password -->Zb@U7veTF9/2cVP
6.  Execute ```stripe listen --forward-to http://127.0.0.1:8000/en/ws/stripe/webhooks ```
7. Copy your webhook signing secret from the CLI (Starts with whsec_)
8. Go to http://127.0.0.1:8000/admin/payment_gateway/stripe_keys/1/change/
9. Paste the signing secret into --> endpoint secret column
10. Save

Now we are all set to start testing our website, make sure you do NOT close the terminal in which stripe CLI is running.

### Languages
Languages can be added from http://127.0.0.1:8000/admin/common/language/

Whenever a new language is added, "Rates" are generated for all the possible combinations of the new language and the existing language for all the existing "Job Types".

A "base price" which can be edited here- http://127.0.0.1:8000/admin/common/variables/1/change/ is used as the default price while creating all the possible combinations. 

Admin can afterward edit the "Rates" for each of the combinations here if needed- http://127.0.0.1:8000/admin/common/rate/ 

### Contracts
Contracts are created for each and every part of a job (posted by the user), For example-
If a job is created which requires translation from English to French and Spanish with ADVANCE+ quality which requires Translation + Proofreading, then-
1. A translation contract will be created for English --> french
2. A translation contract will be created for English --> Spanish
3. A proofreading contract will be created for English --> Spanish with dependency on contract#1 (dependency means this contract will only be available after the completion of contract #1 with submissions (translated files) from contract #1 available as a reference to this contract (for proofreading))
4. A proofreading contract will be created for English --> Spanish with dependency on contract#2

### Price Calculation
Prices for each contract (generated for one single language to another single language) is also pre-calculated using this formula-

language_total = price of all the attachments for a perticualr language
company_gets = (company_share/100)*language_total
remaining = language_total - company_gets

##### if proofreading is required:

  translator_gets = (translator_share/100)*remaining
  proofreader_gets = (proofreader_share/100)*remaining
  
##### else:

  translator_gets = remaining

#### company_share, translator_share & proofreader_share can be edited here- http://127.0.0.1:8000/admin/common/variables/1/change/

Testing flow to check everything out-
#### Admin
1. If not already, Log-in as an Admin via http://127.0.0.1:8000/en/login using these credentials, you will be redirected to the admin dashboard.

| username | password |
| ------ | ------ |
|  admin@tergum.com  | tergum |

Note- Admin dashboard is in its initial stage, only the "create translator" functionality is to be tested here.

2. Click the "Create Translator" button.
3. Fill in all the details presented with an active e-mail address, an invitation link will be sent to the provided email from a temporary email sujatisamaj@gmail.com.
4. Click on the link in the email and follow on-screen instructions to activate and get into your translator account.

### Translator
Now you can use the provided email and password to set via on-screen instruction to log-in as a translator.

1. Available contracts (Translation contracts and Proofreading contracts) according to the skill-set (chosen by the admin during creation) of the translator will be shown on the dashboard. 
2. Translator can sign any of these contracts by clicking the "Accept Contact" and then the "Sign this contract" buttons.
3. If no contracts are available for the translator you created, try creating a new Job with the same skill-set (Source Language and Target Language) as the user or log-in using these credentials- (this account has all the skills so all the already available jobs will be shown to this account)

| username | password |
| ------ | ------ |
|  translator@tergum.com  | tergum |

4. Settings can be used to edit the Profile of your translator account, options to edit skills are yet to be added due to its dependence on admin operations.
5. Accepted contracts and completed contacts can be viewed via options present in Side Navigation Bar
6. View details on translation contracts show the original document uploaded by the user and Proofreading contracts display the original document uploaded by the user and the translated document both.

### User (Customer)
Customers can log-in via Google are creating an account with us. 
After logging in, they can create an order by following the using the on-screen instructions.

For testing purposes, we can use these details on the Stripe gateway to place an order-

##### Note- Make sure you have an active internet connection
 
##### Card information for testing-
Enter 4242 4242 4242 4242 as the card number
Enter any future date for card expiry
Enter any 3-digit number for CVV
Enter any billing address and ZIP code (90210)
Click the “Pay” button
Your order will be placed.

#### As soon as payment is successfully "processed" (might or might not be received yet),
we mark the order Accepted and set its status to PN (PENDING).

#### Once the payment confirmation is received via webhooks, 
we mark the order as OP (OPEN) and now only it will be visible 
to employees to pick. 

View details for a job here in the user dashboard is not active yet due to its dependence on admin operations.




