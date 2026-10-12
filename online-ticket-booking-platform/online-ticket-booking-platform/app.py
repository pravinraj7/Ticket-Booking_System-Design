from flask import Flask, request, jsonify
from threading import Lock

app = Flask(__name__)
events = {
    1: {"id": 1, "name": "Music Concert", "location": "Coimbatore"},
    2: {"id": 2, "name": "Movie Show", "location": "Chennai"},
}

seats = {
    101: {"event_id": 1, "status": "AVAILABLE"},
    102: {"event_id": 1, "status": "AVAILABLE"},
    103: {"event_id": 1, "status": "BOOKED"},
    201: {"event_id": 2, "status": "AVAILABLE"},
}

bookings = {}
next_booking_id = 1
seat_lock = Lock()


@app.route("/api/events", methods=["GET"])
def search_events():
    keyword = request.args.get("keyword", "").lower()
    result = [
        event for event in events.values()
        if keyword in event["name"].lower()
    ]
    return jsonify(result), 200


@app.route("/api/events/<int:event_id>/seats", methods=["GET"])
def get_seat_availability(event_id):
    if event_id not in events:
        return jsonify({"error": "Event not found"}), 404

    result = {
        str(seat_id): seat["status"]
        for seat_id, seat in seats.items()
        if seat["event_id"] == event_id
    }
    return jsonify(result), 200


@app.route("/api/reservations", methods=["POST"])
def reserve_seat():
    global next_booking_id
    data = request.get_json(silent=True) or {}

    user_id = data.get("userId")
    event_id = data.get("eventId")
    seat_id = data.get("seatId")

    if user_id is None or event_id is None or seat_id is None:
        return jsonify({
            "error": "Required fields: userId, eventId, seatId"
        }), 400
        
    try:
        user_id, event_id, seat_id = int(user_id), int(event_id), int(seat_id)
    except (TypeError, ValueError):
        return jsonify({"error": "IDs must be integers"}), 400

    with seat_lock:
        if event_id not in events or seat_id not in seats:
            return jsonify({"error": "Event or seat not found"}), 404

        if seats[seat_id]["event_id"] != event_id:
            return jsonify({"error": "Seat does not belong to this event"}), 400

        if seats[seat_id]["status"] != "AVAILABLE":
            return jsonify({"error": "Seat unavailable"}), 409

        seats[seat_id]["status"] = "RESERVED"
        booking_id = next_booking_id
        next_booking_id += 1

        bookings[booking_id] = {
            "bookingId": booking_id,
            "userId": user_id,
            "eventId": event_id,
            "seatId": seat_id,
            "status": "RESERVED"
        }

    return jsonify(bookings[booking_id]), 201


@app.route("/api/bookings/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(booking), 200


@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    with seat_lock:
        booking = bookings.get(booking_id)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        if booking["status"] == "CANCELLED":
            return jsonify({"error": "Booking already cancelled"}), 409

        seats[booking["seatId"]]["status"] = "AVAILABLE"
        booking["status"] = "CANCELLED"

    return jsonify({
        "message": "Ticket cancelled successfully",
        "bookingId": booking_id,
        "status": "CANCELLED"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
