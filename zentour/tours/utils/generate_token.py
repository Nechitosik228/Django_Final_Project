from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from ..models import BoughtTour


def generate_token_for_qr_code(bought_tour:BoughtTour):
    signer = TimestampSigner()
    value = f"{bought_tour.id}"
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
        bought_tour_id = unsigned
        return int(bought_tour_id)
    except ValueError:
        raise BadSignature("Malformed token")