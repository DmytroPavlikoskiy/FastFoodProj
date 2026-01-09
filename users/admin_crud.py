from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from models import db, User
from flask_login import current_user, login_required
from db_config.decorators import admin_required

admin_users_bp = Blueprint("admin_users", __name__, template_folder="templates")

def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


@admin_users_bp.route("/users")
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template("admin_panel/users.html", users=users)


@admin_users_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.role = request.form.get("role")
        db.session.commit()
        flash("Дані користувача оновлено!", "success")
        return redirect(url_for("admin_users.list_users"))
        
    return render_template("admin_panel/edit_user.html", user=user)


@admin_users_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    
    if current_user.id == user_id:
        flash("Ви не можете видалити власного користувача!", "danger")
        return redirect(url_for("admin_users.list_users"))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Користувача видалено", "danger")
    return redirect(url_for("admin_users.list_users"))