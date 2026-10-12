# Online Ticket Booking Platform

This repository contains the coding demonstrations for:

- **Round 2 – Low-Level Design:** REST APIs implemented using Python Flask.
- **Round 3 – High-Level System Design:** MySQL script demonstrating atomic seat reservation to help prevent double booking.

## Folder contents

```text
online-ticket-booking-platform/
├── app.py
├── round3_seat_reservation.sql
├── requirements.txt
├── README.md
└── .gitignore
```

## Round 2: Run the Flask API

Requirements: Python 3.9+ recommended.

1. Open this folder in VS Code.
2. Open Terminal and run:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the server:

   ```bash
   python app.py
   ```

4. Open these URLs in your browser while the server is running:

   - `http://127.0.0.1:5000/api/events`
   - `http://127.0.0.1:5000/api/events?keyword=concert`
   - `http://127.0.0.1:5000/api/events/1/seats`

### Test POST and DELETE APIs

Use Postman or another API client.

**Reserve a seat**

- Method: `POST`
- URL: `http://127.0.0.1:5000/api/reservations`
- Body type: JSON

  ```json
  {
    "userId": 101,
    "eventId": 1,
    "seatId": 101
  }
  ```

The response contains a booking ID. Use that ID for the next requests.

**Get booking details**

- Method: `GET`
- URL: `http://127.0.0.1:5000/api/bookings/1`

**Cancel booking**

- Method: `DELETE`
- URL: `http://127.0.0.1:5000/api/bookings/1`

This is an educational in-memory demonstration. Data resets when the Python server restarts. The code marks a reservation but does not implement real payment processing, ticket generation, or reservation expiry.

## Round 3: Run the MySQL script

1. Open MySQL Workbench and connect to your MySQL server.
2. Open `round3_seat_reservation.sql` (File → Open SQL Script).
3. Execute the script.
4. Inspect the output for seat `101`.

The first conditional `UPDATE` should affect one row and set the seat to `RESERVED`. The second should affect zero rows because the seat is no longer `AVAILABLE`.

This demonstrates the core database technique. In a production service, use a transaction and additional booking constraints, payment verification, idempotency, and reservation-expiry handling.

## GitHub upload

1. Sign in to GitHub and create a new repository, for example `online-ticket-booking-platform`.
2. Choose **Public** or **Private** as appropriate.
3. Upload the files from this folder, or extract the ZIP and use Git.

Example Git commands (run inside this project folder):

```bash
git init
git add .
git commit -m "Add ticket booking design demos"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/online-ticket-booking-platform.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not upload passwords, API keys, or database credentials.
