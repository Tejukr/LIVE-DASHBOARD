import random
import time
from datetime import datetime
from sqlalchemy import create_engine, text

# --- PostgreSQL Connection ---
engine = create_engine(
    "postgresql+psycopg2://postgres:superuser@localhost:5432/SALES_DASHBOARD",
    echo=True  # shows SQL logs (IMPORTANT for debugging)
)

regions = ["North", "South", "East", "West"]
products = ["Product A", "Product B", "Product C", "Product D"]

insert_sql = text("""
    INSERT INTO sales_data (region, product, quantity, total_sales, sale_time)
    VALUES (:region, :product, :quantity, :total_sales, :sale_time)
""")

print("✅ Sales simulator started... Press Ctrl+C to stop.")

while True:
    data = {
        "region": random.choice(regions),
        "product": random.choice(products),
        "quantity": random.randint(1, 10),
        "total_sales": round(random.uniform(50, 500), 2),
        "sale_time": datetime.now()
    }

    try:
        with engine.begin() as conn:   # ✅ auto-commit
            conn.execute(insert_sql, data)

        print(f"INSERTED → {data}")

    except Exception as e:
        print("❌ INSERT FAILED:", e)

    time.sleep(20)   # ⏱️ 20 seconds (faster demo)
