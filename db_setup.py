import sqlite3
import pandas as pd

DB_PATH = "data.db"


def setup_database():
    conn = sqlite3.connect(DB_PATH)

    data = pd.DataFrame(
        [
            ("Japan", 2019, 31, 190),
            ("Japan", 2022, 25, 170),
            ("Japan", 2023, 32, 210),

            ("France", 2019, 90, 210),
            ("France", 2022, 75, 185),
            ("France", 2023, 79, 190),

            ("Italy", 2019, 65, 175),
            ("Italy", 2022, 60, 170),
            ("Italy", 2023, 65, 180),

            ("Spain", 2019, 83, 205),
            ("Spain", 2022, 80, 195),
            ("Spain", 2023, 83, 200),

            ("Ukraine", 2019, 14, 12),
            ("Ukraine", 2022, 4, 3),
            ("Ukraine", 2023, 14, 8),

            ("Germany", 2019, 39, 150),
            ("Germany", 2022, 33, 135),
            ("Germany", 2023, 35, 140),

            ("United Kingdom", 2019, 41, 155),
            ("United Kingdom", 2022, 37, 145),
            ("United Kingdom", 2023, 39, 150),
        ],
        columns=[
            "country",
            "year",
            "visitors_millions",
            "tourism_revenue_usd",
        ],
    )

    data.to_sql("tourism_stats", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ Database initialized")


# дозволяє запускати і напряму
if __name__ == "__main__":
    setup_database()
