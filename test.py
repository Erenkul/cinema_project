from db import get_connection

try:
    conn = get_connection()
    print("✅ Oracle bağlantısı başarılı:", conn.version)
    conn.close()
except Exception as e:
    print("❌ Hata:", e)
