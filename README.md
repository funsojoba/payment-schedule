# PAYMENT SCHEDULER

## Use Case

A user has a wallet and would like to schedule a payment for a specific time. The user can schedule the payment given that the amount is less than what the user has in their wallet balance. On the set day, the amount is deducted from their wallet and the payment is made while a notification is sent to the said user about the payment made.

## How to get started

- Make sure you have docker installed on your machine
- Clone the repo
- Run `cd payment-schedule` into the root directory of the project
- A lot of the the Docker command has been abstracted using the `Makefile` so running `make` with desired command will get you started.
- Run `make build`
- Run `make up`
- You can also check the `Makefile` to see other commands needed

The app should be running on `localhost:8080`
The email server is hosted locally and  running on `localhost:1025`


## Technologies used
- Djano Rest Framework
- Django
- Docker
- SQLite
- Redis
- Celery



Happy hacking 🎉