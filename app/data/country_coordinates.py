"""
Country coordinates data
Matches the frontend's country-coordinates.ts
"""
from app.domain.models import CountryCoordinates

COUNTRY_COORDINATES = [
    CountryCoordinates(iso3_code="IDN", label="Indonesia", latitude=-0.7893, longitude=113.9213),
    CountryCoordinates(iso3_code="IND", label="India", latitude=20.5937, longitude=78.9629),
    CountryCoordinates(iso3_code="BRA", label="Brazil", latitude=-14.2350, longitude=-51.9253),
    CountryCoordinates(iso3_code="USA", label="United States", latitude=37.0902, longitude=-95.7129),
    CountryCoordinates(iso3_code="CHN", label="China", latitude=35.8617, longitude=104.1954),
    CountryCoordinates(iso3_code="RUS", label="Russia", latitude=61.5240, longitude=105.3188),
    CountryCoordinates(iso3_code="JPN", label="Japan", latitude=36.2048, longitude=138.2529),
    CountryCoordinates(iso3_code="DEU", label="Germany", latitude=51.1657, longitude=10.4515),
    CountryCoordinates(iso3_code="GBR", label="United Kingdom", latitude=55.3781, longitude=-3.4360),
    CountryCoordinates(iso3_code="FRA", label="France", latitude=46.2276, longitude=2.2137),
    CountryCoordinates(iso3_code="ITA", label="Italy", latitude=41.8719, longitude=12.5674),
    CountryCoordinates(iso3_code="CAN", label="Canada", latitude=56.1304, longitude=-106.3468),
    CountryCoordinates(iso3_code="AUS", label="Australia", latitude=-25.2744, longitude=133.7751),
    CountryCoordinates(iso3_code="MEX", label="Mexico", latitude=23.6345, longitude=-102.5528),
    CountryCoordinates(iso3_code="ARG", label="Argentina", latitude=-38.4161, longitude=-63.6167),
    CountryCoordinates(iso3_code="ZAF", label="South Africa", latitude=-30.5595, longitude=22.9375),
    CountryCoordinates(iso3_code="EGY", label="Egypt", latitude=26.8206, longitude=30.8025),
    CountryCoordinates(iso3_code="NGA", label="Nigeria", latitude=9.0820, longitude=8.6753),
    CountryCoordinates(iso3_code="KEN", label="Kenya", latitude=-0.0236, longitude=37.9062),
    CountryCoordinates(iso3_code="ETH", label="Ethiopia", latitude=9.1450, longitude=40.4897),
    CountryCoordinates(iso3_code="THA", label="Thailand", latitude=15.8700, longitude=100.9925),
    CountryCoordinates(iso3_code="VNM", label="Vietnam", latitude=14.0583, longitude=108.2772),
    CountryCoordinates(iso3_code="PHL", label="Philippines", latitude=12.8797, longitude=121.7740),
    CountryCoordinates(iso3_code="PAK", label="Pakistan", latitude=30.3753, longitude=69.3451),
    CountryCoordinates(iso3_code="BGD", label="Bangladesh", latitude=23.6850, longitude=90.3563),
]
