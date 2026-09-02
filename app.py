@app.route("/promote/<int:user_id>")
def promote(user_id):
    if session.get("role") != "host":
        return "Access denied. Only Host can promote"
    user = User.query.get(user_id)
    if user and user.role == "user":
        user.role = "cohost"
        db.session.commit()
    return redirect(url_for("dashboard"))
