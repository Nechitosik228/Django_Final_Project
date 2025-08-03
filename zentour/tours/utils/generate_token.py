from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from ..models import BoughtTour


def generate_token_for_qr_code(bought_tour:BoughtTour, seat_numbers):
    signer = TimestampSigner()
    value = f"{bought_tour.id}:{seat_numbers}"
    return signer.sign(value)


def validate_token_for_qr_code(token):
    signer = TimestampSigner()
    try:
        unsigned = signer.unsign(token)
    except SignatureExpired:
        raise
    except BadSignature:
        raise

    try:
        bought_tour_id, seat_numbers = unsigned.split(":", 1)
        return int(bought_tour_id), seat_numbers
    except ValueError:
        raise BadSignature("Malformed token")