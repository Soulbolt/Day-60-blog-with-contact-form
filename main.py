from flask import Flask, render_template, request
import requests
import smtplib


MY_EMAIL = "EMAIL GOES HERE"
MY_PASSWORD = "PASSWORD HERE"
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        success = "Successfully sent your message."
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:User Message!\n\nName: {request.form.get('name')\nEmail: {request.form.get('email')} \
            \nPhone: {request.form.get('phone')}\nMessage: {request.form.get('message')}"
        )
        return render_template("contact.html", confirm=success)
    else:
        return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

# @app.route("/form-entry", methods=["GET", "POST"])
# def receive_data():
#     return "<h1>Successfully sent your message.</h1>"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
