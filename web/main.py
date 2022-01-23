from flask import Flask, render_template, redirect, url_for, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

# TODO: Add env variables to docker-compose.yaml
app.config['SECRET_KEY'] = 'ABCDEFGHI1234'
# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.getenv("OAUTHLIB_INSECURE_TRANSPORT")

app.config["DISCORD_CLIENT_ID"] = os.getenv("DISCORD_CLIENT_ID")  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = os.getenv("DISCORD_REDIRECT_URI")  # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")  # Required to access BOT resources.
discord = DiscordOAuth2Session(app)

client = MongoClient(os.getenv("MONGO_URL"), int(os.getenv("MONGO_PORT")))
db = client.get_database("GuildData").get_collection("GuildConfig")


@app.route("/")
@app.route("/home/")
def home():
    return render_template("dashboard/home.html", discord=discord)


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".guilds"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/guilds/")
@requires_authorization
def guilds():
    guilds = discord.fetch_guilds()
    return render_template("dashboard/guilds.html", guilds=guilds, discord=discord)


@app.route("/guild/<int:id>/", methods=['GET', 'POST'])
@requires_authorization
def guild(id):
    if request.method == "POST":
        settings = db.update_one(
            {"guildID": id},
            {"$set": {"prefix": request.form['prefix'],
                      "welcomeChannelId": request.form['welcomeChannelId'],
                      "goodbyeChannelId": request.form['goodbyeChannelId']
                      }
             }
        )
        return redirect(url_for("guild", id=id))
    else:
        # TODO: Add checking for bot in guilds
        guild = next(guild for guild in discord.fetch_guilds() if guild.id == id)
        if guild.is_owner:
            settings = db.find({"guildID": guild.id})
            return render_template("dashboard/guild.html", settings=settings[0], discord=discord)


if __name__ == '__main__':
    app.run(os.getenv("FLASK_HOST"), os.getenv("FLASK_PORT"), debug=True)
