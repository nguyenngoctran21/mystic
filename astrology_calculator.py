from skyfield.api import load, Topos
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from pytz import timezone
from datetime import datetime

class AstrologyCalculator:
    ZODIAC_SIGNS = [
        ("Bạch Dương", "♈", 0),
        ("Kim Ngưu", "♉", 30),
        ("Song Tử", "♊", 60),
        ("Cự Giải", "♋", 90),
        ("Sư Tử", "♌", 120),
        ("Xử Nữ", "♍", 150),
        ("Thiên Bình", "♎", 180),
        ("Bọ Cạp", "♏", 210),
        ("Nhân Mã", "♐", 240),
        ("Ma Kết", "♑", 270),
        ("Bảo Bình", "♒", 300),
        ("Song Ngư", "♓", 330)
    ]

    def __init__(self, name: str, birthdate: str, birthtime: str, birthplace: str):
        self.name = name
        self.birthdate = birthdate
        self.birthtime = birthtime
        self.birthplace = birthplace

        self.lat, self.lon = self.get_coordinates(birthplace)
        self.tz = self.get_timezone(self.lat, self.lon)
        self.ts = load.timescale()
        self.eph = load('de421.bsp')

        self.utc_dt = self.local_to_utc(birthdate, birthtime, self.tz)
        self.t = self.ts.utc(self.utc_dt.year, self.utc_dt.month, self.utc_dt.day, self.utc_dt.hour, self.utc_dt.minute)

    def get_coordinates(self, place):
        geo = Nominatim(user_agent="astro_bot")
        loc = geo.geocode(place)
        if not loc:
            return 10.0452, 105.7469  # Fallback: Cần Thơ
        return loc.latitude, loc.longitude

    def get_timezone(self, lat, lon):
        tf = TimezoneFinder()
        return timezone(tf.timezone_at(lat=lat, lng=lon))

    def local_to_utc(self, date_str, time_str, tz):
        dt_local = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        return tz.localize(dt_local).astimezone(timezone("UTC"))

    def get_zodiac(self, degrees):
        for name, emoji, start_deg in reversed(self.ZODIAC_SIGNS):
            if degrees >= start_deg:
                return f"{emoji} {name}"
        return "❓ Unknown"

    def get_planet_signs(self):
        obs = Topos(latitude_degrees=self.lat, longitude_degrees=self.lon)
        observer = self.eph["earth"] + obs
        planets = {
            "☀ Mặt Trời": self.eph["sun"],
            "🌙 Mặt Trăng": self.eph["moon"],
            "☿ Sao Thủy": self.eph["mercury"],
            "♀ Sao Kim": self.eph["venus"],
            "♂ Sao Hỏa": self.eph["mars"],
            "♃ Sao Mộc": self.eph["jupiter barycenter"],
            "♄ Sao Thổ": self.eph["saturn barycenter"]
        }

        result = []
        for name, body in planets.items():
            astrometric = observer.at(self.t).observe(body).apparent()
            lon = astrometric.ecliptic_latlon()[1].degrees % 360
            sign = self.get_zodiac(lon)
            result.append(f"{name}: {sign} ({lon:.2f}°)")

        return "\n".join(result)

    def get_birth_chart_text(self):
        return self.get_planet_signs()
