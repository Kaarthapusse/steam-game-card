import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

STEAM_ID = "76561198127717896"
API_KEY = os.environ["STEAM_API_KEY"]

# Identifiant Steam de Seven Days to Die
SEVEN_DAYS_APP_ID = 251570

url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
params = {
    "key": API_KEY,
    "steamid": STEAM_ID,
    "include_appinfo": True,
    "include_played_free_games": True
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
games = response.json()["response"].get("games", [])

if not games:
    raise RuntimeError(
        "Aucun jeu trouvé. Vérifie la confidentialité Steam."
    )

# Recherche directe de Seven Days to Die
game = next(
    (g for g in games if g["appid"] == SEVEN_DAYS_APP_ID),
    None
)

if game is None:
    raise RuntimeError(
        "Seven Days to Die introuvable. "
        "Vérifie la confidentialité de tes jeux Steam."
    )

title = game["name"]
hours = game.get("playtime_forever", 0) / 60
app_id = game["appid"]

# Création de la carte
image = Image.new("RGB", (900, 260), "#101820")
draw = ImageDraw.Draw(image)

cover_url = (
    f"https://shared.akamai.steamstatic.com/store_item_assets/"
    f"steam/apps/{app_id}/header.jpg"
)

try:
    cover_response = requests.get(cover_url, timeout=30)
    cover_response.raise_for_status()
    cover = Image.open(
        BytesIO(cover_response.content)
    ).convert("RGB")
    cover.thumbnail((460, 260))
    image.paste(cover, (0, 0))
except Exception:
    pass

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
small_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

try:
    nickname_font = ImageFont.truetype(font_path, 44)
    title_font = ImageFont.truetype(font_path, 30)
    hours_font = ImageFont.truetype(small_path, 25)
except OSError:
    nickname_font = ImageFont.load_default()
    title_font = ImageFont.load_default()
    hours_font = ImageFont.load_default()

draw.text(
    (480, 20),
    "Kaarthapusse",
    fill="#ff3333",
    font=nickname_font
)

draw.text(
    (480, 85),
    title[:30],
    fill="white",
    font=title_font
)

draw.text(
    (480, 145),
    f"{hours:,.1f} heures de jeu",
    fill="#65d46e",
    font=hours_font
)

image.save("steam-game-card.png")

print(f"Carte créée : steam-game-card.png")
print(f"Jeu : {title}")
print(f"Temps de jeu : {hours:.1f} heures")
