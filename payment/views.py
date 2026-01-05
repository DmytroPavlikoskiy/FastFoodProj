from flask import Blueprint, redirect, url_for, request, abort
from models import db, Payment, Comments
import uuid


payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/example_url')
def example():
    pass


def process_payment(order_id):
    transaction_id = str(uuid.uuid4())

    payment = Payment(
        order_id=order_id,
        status = "success",
        transaction_id=transaction_id
    )


    db.session.add(payment)
    db.session.commit()

    return redirect(url_for('success_page'))


@payment_bp.route('/comment/<int:product_id>/<int:user_id>', methods=['POST'])
def add_comment(product_id, user_id):
    payment = Payment.query.filter_by(status="success").first()
    if not payment:
        abort(403, description="Коментар можна залишити тільки після покупки!")


    text = request.form.get("text")
    rating = request.form.get("rating")



    if not text or not rating:
        abort(400, description="Заповніть всі поля коментаря!")

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            abort(400, description="Рейтинг має бути від 1 до 5")

    except ValueError:
         abort(400, description="Рейтинг має бути числом")

    comment = Comments(
        user_id=user_id,
        product_id=product_id,
        text=text,
        rating=rating
    )

    db.session.add(comment)
    db.session.commit()


    return "Коментар додано успішно"

