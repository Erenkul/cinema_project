from flask import Flask, render_template, request, redirect, url_for
import cx_Oracle
from db import get_connection, query_all, execute

# Oracle Instant Client konumu (senin sistemine göre doğru)
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Ozi\Desktop\sql\instantclient_21_19")

app = Flask(__name__)

app.secret_key = "eren_cinema_secret_2025"


# ----------------------------------------------------------------------
# 🏠 ANA SAYFA (Now Showing / Coming Soon)
# ----------------------------------------------------------------------
@app.route('/')
def home():
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
    cursor = connection.cursor()

    # Now showing
    cursor.execute("""
        SELECT movie_id, title, genre, duration_minutes, poster_url 
        FROM movies WHERE release_date <= SYSDATE
    """)
    now_showing = cursor.fetchall()

    # Coming soon
    cursor.execute("""
        SELECT movie_id, title, release_date, poster_url 
        FROM movies WHERE release_date > SYSDATE
    """)
    coming_soon = cursor.fetchall()

    connection.close()
    return render_template("index.html", now_showing=now_showing, coming_soon=coming_soon)




# ----------------------------------------------------------------------
# 🎬 FİLM EKLEME
# ----------------------------------------------------------------------
@app.route("/movies/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie_id = request.form["movie_id"]
        title = request.form["title"]
        director = request.form["director"]
        duration = request.form["duration_minutes"]
        genre = request.form["genre"]
        age_rating = request.form["age_rating"]
        release_date = request.form["release_date"]
        description = request.form["description"]
        poster_url = request.form.get("poster_url", "")

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO movies 
                (movie_id, title, director, duration_minutes, genre, age_rating, release_date, description, poster_url)
                VALUES (:1, :2, :3, :4, :5, :6, TO_DATE(:7, 'YYYY-MM-DD'), :8, :9)
            """, (movie_id, title, director, duration, genre, age_rating, release_date, description, poster_url))
            conn.commit()
        return redirect(url_for("show_movies"))

    return render_template("add_movie.html", movie=None)


# ----------------------------------------------------------------------
# 🎬 FİLM GÜNCELLEME (UPDATE)
# ----------------------------------------------------------------------
@app.route("/movies/update/<int:movie_id>", methods=["GET", "POST"])
def update_movie(movie_id):
    connection = get_connection()
    cursor = connection.cursor()

    # GET → sayfayı aç
    if request.method == "GET":
        cursor.execute("""
            SELECT movie_id, title, director, duration_minutes, genre, age_rating, 
                   TO_CHAR(release_date, 'YYYY-MM-DD'), description, poster_url
            FROM movies
            WHERE movie_id = :id
        """, {"id": movie_id})
        movie = cursor.fetchone()
        cursor.close()
        connection.close()

        if not movie:
            return "Movie not found", 404

        # veritabanından gelen tuple’ı dictionary’e çevir
        movie_data = {
            "movie_id": movie[0],
            "title": movie[1],
            "director": movie[2],
            "duration_minutes": movie[3],
            "genre": movie[4],
            "age_rating": movie[5],
            "release_date": movie[6],
            "description": movie[7],
            "poster_url": movie[8]
        }

        return render_template("update_movie.html", movie=movie_data)

    # POST → form gönderilince güncelle
    else:
        title = request.form["title"]
        director = request.form["director"]
        duration = request.form["duration_minutes"]
        genre = request.form["genre"]
        age_rating = request.form["age_rating"]
        release_date = request.form["release_date"]
        description = request.form["description"]
        poster_url = request.form.get("poster_url", "")

        cursor.execute("""
            UPDATE movies
            SET title = :1,
                director = :2,
                duration_minutes = :3,
                genre = :4,
                age_rating = :5,
                release_date = TO_DATE(:6, 'YYYY-MM-DD'),
                description = :7,
                poster_url = :8
            WHERE movie_id = :9
        """, (title, director, duration, genre, age_rating, release_date, description, poster_url, movie_id))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("show_movies"))



# ----------------------------------------------------------------------
# 🗑️ FİLM SİLME (DELETE)
# ----------------------------------------------------------------------
@app.route("/movies/delete/<int:movie_id>", methods=["GET", "POST"])
def delete_movie(movie_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM movies WHERE movie_id = :id", {"id": movie_id})
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Movie {movie_id} deleted successfully")
        return redirect(url_for("show_movies"))
    except Exception as e:
        print("Error deleting movie:", e)
        return f"Error deleting movie: {e}", 500






# ----------------------------------------------------------------------
# 🎞️ TÜM FİLMLER
# ----------------------------------------------------------------------
@app.route("/movies")
def show_movies():
    query = """
        SELECT 
            movie_id, 
            title, 
            director, 
            duration_minutes, 
            genre, 
            age_rating, 
            TO_CHAR(release_date, 'YYYY-MM-DD') as release_date, 
            description
        FROM movies
        ORDER BY movie_id
    """
    rows = query_all(query)
    return render_template("movies.html", movies=rows)

# ----------------------------------------------------------------------
# 👥 MÜŞTERİLER
# ----------------------------------------------------------------------
@app.route("/customers")
def customers():
    query = """
        SELECT CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, 
               JOIN_DATE, LOYALTY_POINTS
        FROM CUSTOMERS
        ORDER BY CUSTOMER_ID
    """
    customers = query_all(query)
    return render_template("customers.html", customers=customers)

# ----------------------------------------------------------------------
# 📄 FİLM DETAYLARI SAYFASI
# ----------------------------------------------------------------------
@app.route("/movies/<int:movie_id>")
def details(movie_id):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT movie_id, title, year, genre, duration_minutes, description, director, poster_url
        FROM movies 
        WHERE movie_id = :id
    """, [movie_id])
    movie = cursor.fetchone()

    #cursor.execute("SELECT genre_name FROM genres WHERE movie_id = :id", [movie_id])
    #genres = [g[0] for g in cursor.fetchall()]
    cursor.execute("""
        SELECT movie_id, title, genre, duration_minutes, poster_url 
        FROM movies
        WHERE genre = :genre AND movie_id != :id
        AND ROWNUM <= 4
    """, {'genre': movie[2], 'id': movie_id})
    similar_movies = cursor.fetchall()
    connection.close()

    return render_template(
        "details.html", movie=movie,
        similar_movies=similar_movies
        )


# ----------------------------------------------------------------------
# 🎟️ KOLTUK SEÇİMİ
# ----------------------------------------------------------------------
@app.route('/seats/<int:movie_id>')
def seats(movie_id):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
    cursor = connection.cursor()

    cursor.execute("SELECT title FROM movies WHERE movie_id = :id", [movie_id])
    movie_title = cursor.fetchone()[0]

    cursor.execute("""
        SELECT row_label, seat_number, LOWER(status)
        FROM seats WHERE movie_id = :id ORDER BY row_label, seat_number
    """, [movie_id])
    all_seats = cursor.fetchall()
    connection.close()

    seat_rows = []
    current_row = None
    for row_label, seat_num, status in all_seats:
        if not current_row or current_row['row_label'] != row_label:
            current_row = {'row_label': row_label, 'seats': []}
            seat_rows.append(current_row)
        current_row['seats'].append({
            'code': f"{row_label}{seat_num}",
            'number': seat_num,
            'status': status
        })

    return render_template("seats.html",
                           movie_id=movie_id,
                           movie_title=movie_title,
                           theater_name="Dark Reel Downtown",
                           show_time="Today, Oct 15 • 3:00 PM",
                           seat_rows=seat_rows,
                           ticket_price=12.99,
                           service_fee=1.50,
                           total_price=14.49)

# ----------------------------------------------------------------------
# 💳 CHECKOUT (ÖDEME SAYFASI)
# ----------------------------------------------------------------------
@app.route('/checkout', methods=['POST'])
def checkout():
    movie_id = request.form['movie_id']
    selected_seats = request.form['selected_seats']

    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM movies WHERE movie_id = :id", [movie_id])
    movie_title = cursor.fetchone()[0]
    connection.close()

    return render_template(
        "checkout.html",
        movie_id=movie_id,
        movie_title=movie_title,
        theater_name="Dark Reel Downtown",
        show_time="Today, Oct 15 • 3:00 PM",
        selected_seats=selected_seats,
        ticket_total=25.98,
        service_fee=2.50,
        total_price=28.48
    )

# ----------------------------------------------------------------------
# ✅ ÖDEME ONAYI
# ----------------------------------------------------------------------
@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    # 1️⃣ Form verilerini al
    data = {
        'movie_id': request.form['movie_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'selected_seats': request.form['selected_seats']
    }

    # 2️⃣ Veritabanı bağlantısı
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
    cursor = connection.cursor()

    # 3️⃣ Aynı email varsa o müşteri kullanılsın
    cursor.execute("SELECT customer_id FROM customers WHERE email = :email", {'email': data['email']})
    existing_customer = cursor.fetchone()

    if existing_customer:
        # ✅ Zaten kayıtlı müşteri
        customer_id = existing_customer[0]
    else:
        # ❌ Yeni müşteri oluştur
        cursor.execute("SELECT CUSTOMER_SEQ.NEXTVAL FROM dual")
        customer_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO customers (customer_id, first_name, last_name, email, phone, join_date, loyalty_points)
            VALUES (:customer_id, :first_name, :last_name, :email, :phone, SYSDATE, 0)
        """, {
            'customer_id': customer_id,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'phone': data['phone']
        })

    # 4️⃣ Rezervasyon kaydını oluştur
    cursor.execute("""
        INSERT INTO reservations (movie_id, customer_id, selected_seats)
        VALUES (:movie_id, :customer_id, :selected_seats)
    """, {
        'movie_id': data['movie_id'],
        'customer_id': customer_id,
        'selected_seats': data['selected_seats']
    })

    # 5️⃣ Commit ve bağlantı kapatma
    connection.commit()
    cursor.close()
    connection.close()

    # 6️⃣ Onay sayfasına yönlendir
    return render_template("reservation.html", data={**data, 'customer_id': customer_id})








@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        join_date = request.form['join_date']
        loyalty_points = request.form.get('loyalty_points', 0)

        # 🔹 Oracle bağlantısı
        connection = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
        cursor = connection.cursor()

        # 🔹 Yeni ID'yi Python tarafında al (trigger yok)
        cursor.execute("SELECT CUSTOMER_SEQ.NEXTVAL FROM dual")
        customer_id = cursor.fetchone()[0]

        # 🔹 Veriyi ekle
        cursor.execute("""
            INSERT INTO customers (customer_id, first_name, last_name, email, phone, join_date, loyalty_points)
            VALUES (:customer_id, :first_name, :last_name, :email, :phone, TO_DATE(:join_date, 'YYYY-MM-DD'), :loyalty_points)
        """, {
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'join_date': join_date,
            'loyalty_points': loyalty_points
        })

        connection.commit()
        cursor.close()
        connection.close()

        flash("✅ Customer added successfully!", "success")
        return redirect(url_for('customers'))

    # 🔹 GET isteği: formu göster
    return render_template("add_customer.html")



@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    try:
        conn = cx_Oracle.connect("hr", "hr", "localhost:1521/XE")
        cur = conn.cursor()
        cur.execute("DELETE FROM CUSTOMERS WHERE CUSTOMER_ID = :id", {'id': customer_id})
        conn.commit()
        flash("🗑️ Customer deleted successfully!", "success")
    except Exception as e:
        flash(f"❌ Error deleting customer: {e}", "error")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('customers'))

















# ============================================
# 🎬 FILM ÖNERİLERİ (ORACLE BAĞLANTILI)
# ============================================

from flask import render_template, request, redirect, url_for, flash, jsonify
import cx_Oracle
from datetime import datetime

# 🔹 Oracle bağlantısı
def get_db_connection():
    return cx_Oracle.connect("hr", "hr", "localhost:1521/XE")


# ============================================
# ROUTES
# ============================================

# 1️⃣ TÜM ÖNERİLERİ LİSTELE
@app.route('/suggestions')
def suggestions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT SUGGESTION_ID, MOVIE_TITLE, DIRECTOR, GENRE, YEAR, 
               REASON, SUGGESTED_BY, EMAIL, STATUS,
               TO_CHAR(CREATED_AT, 'YYYY-MM-DD HH24:MI:SS') AS CREATED_AT,
               TO_CHAR(UPDATED_AT, 'YYYY-MM-DD HH24:MI:SS') AS UPDATED_AT
        FROM MOVIE_SUGGESTIONS
        ORDER BY CREATED_AT DESC
    """)
    rows = [
        dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return render_template("suggestions.html", suggestions=rows)

#
# 2️⃣ YENİ ÖNERİ EKLE (INSERT)
#

@app.route('/suggestions/add', methods=['POST'])
def add_suggestion():
    title = request.form['movie_title']
    director = request.form.get('director', '')
    genre = request.form.get('genre', '')
    year = request.form.get('year', None)
    reason = request.form['reason']
    suggested_by = request.form['suggested_by']
    email = request.form.get('email', '')

    conn = get_db_connection()
    cur = conn.cursor()

    # 🔹 Sequence'ten ID al
    cur.execute("SELECT SUGGESTION_SEQ.NEXTVAL FROM dual")
    suggestion_id = cur.fetchone()[0]

    # 🔹 Tüm kolonları dahil et (STATUS ve tarihler dâhil)
    cur.execute("""
        INSERT INTO MOVIE_SUGGESTIONS (
            SUGGESTION_ID, MOVIE_TITLE, DIRECTOR, GENRE, YEAR,
            REASON, SUGGESTED_BY, EMAIL, STATUS, CREATED_AT, UPDATED_AT
        )
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, 'pending', SYSDATE, SYSDATE)
    """, (suggestion_id, title, director, genre, year, reason, suggested_by, email))

    conn.commit()
    cur.close()
    conn.close()

    flash("🎬 Film öneriniz başarıyla gönderildi!", "success")
    return redirect(url_for('suggestions'))



# 3️⃣ TEK ÖNERİ DETAYI (MODAL - JSON)


@app.route('/suggestions/detail/<int:suggestion_id>')
def suggestion_detail(suggestion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM MOVIE_SUGGESTIONS WHERE SUGGESTION_ID = :1
    """, [suggestion_id])
    row = cur.fetchone()
    if not row:
        return jsonify({'error': 'Öneri bulunamadı'}), 404
    data = dict(zip([d[0] for d in cur.description], row))
    cur.close()
    conn.close()
    return jsonify(data)



# 4️⃣ GÜNCELLEME SAYFASI (GET) SAYFAYI AÇAR HTML RENDER EDER

@app.route('/suggestions/update/<int:suggestion_id>')
def suggestion_edit_page(suggestion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM MOVIE_SUGGESTIONS WHERE SUGGESTION_ID = :1", [suggestion_id])
    row = cur.fetchone()
    if not row:
        flash("❌ Öneri bulunamadı!", "error")
        return redirect(url_for('suggestions'))
    suggestion = dict(zip([d[0] for d in cur.description], row))
    cur.close()
    conn.close()
    return render_template("update_suggestions.html", suggestion=suggestion)



# 5️⃣ GÜNCELLEME (POST)

@app.route('/suggestions/update/<int:suggestion_id>', methods=['POST'])
def suggestion_update(suggestion_id):
    title = request.form['movie_title']
    director = request.form.get('director', '')
    genre = request.form.get('genre', '')
    year = request.form.get('year', None)
    reason = request.form['reason']
    suggested_by = request.form['suggested_by']
    email = request.form.get('email', '')
    status = request.form.get('status', 'pending')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE MOVIE_SUGGESTIONS
        SET MOVIE_TITLE=:1, DIRECTOR=:2, GENRE=:3, YEAR=:4, REASON=:5,
            SUGGESTED_BY=:6, EMAIL=:7, STATUS=:8, UPDATED_AT=SYSDATE
        WHERE SUGGESTION_ID=:9
    """, (title, director, genre, year, reason, suggested_by, email, status, suggestion_id))
    conn.commit()
    cur.close()
    conn.close()

    flash("✅ Öneri başarıyla güncellendi!", "success")
    return redirect(url_for('suggestions'))



# 6️⃣ SİLME

@app.route('/suggestions/delete/<int:suggestion_id>')
def suggestion_delete(suggestion_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MOVIE_TITLE FROM MOVIE_SUGGESTIONS WHERE SUGGESTION_ID=:1", [suggestion_id])
    row = cur.fetchone()
    if not row:
        flash("❌ Öneri bulunamadı!", "error")
        return redirect(url_for('suggestions'))

    cur.execute("DELETE FROM MOVIE_SUGGESTIONS WHERE SUGGESTION_ID=:1", [suggestion_id])
    conn.commit()
    flash(f"🗑️ '{row[0]}' önerisi silindi!", "success")
    cur.close()
    conn.close()
    return redirect(url_for('suggestions'))



# 7️⃣ DURUM GÜNCELLEME (Admin - approved/rejected/pending)

@app.route('/suggestions/status/<int:suggestion_id>/<status>')
def suggestion_status(suggestion_id, status):
    if status not in ['pending', 'approved', 'rejected']:
        flash("❌ Geçersiz durum!", "error")
        return redirect(url_for('suggestions'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE MOVIE_SUGGESTIONS 
        SET STATUS=:1, UPDATED_AT=SYSDATE
        WHERE SUGGESTION_ID=:2
    """, (status, suggestion_id))
    conn.commit()
    cur.close()
    conn.close()

    flash(f"✅ Öneri durumu '{status}' olarak güncellendi!", "success")
    return redirect(url_for('suggestions'))




if __name__ == "__main__":
    app.run(debug=True)
