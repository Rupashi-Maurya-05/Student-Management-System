from sqlalchemy import create_engine, text

# --- change these values to your own setup ---
print("starting test...")
DB_USER = "root"
DB_PASS = "rm123"   # <- your MySQL password
DB_HOST = "localhost"
DB_NAME = "student_management"   # <- replace with your DB name
# ---------------------------------------------

try:
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Connected to database successfully!", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
