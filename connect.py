import pymysql

def get_outfit_recommendations(season, style, gender):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1234qwer',
        database='clothing_recommendation',
        charset='utf8mb4'
    )
    
    query = """
    SELECT o.name, s.name, se.name, g.name, c.name, o.description
    FROM Outfit o
    JOIN Style s ON o.style_id = s.style_id
    JOIN Season se ON o.season_id = se.season_id
    JOIN Gender g ON o.gender_id = g.gender_id
    JOIN Color c ON o.color_id = c.color_id
    WHERE o.season_id = %s AND o.style_id = %s AND o.gender_id = %s;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (season, style, gender))
            results = cursor.fetchall()
            for row in results:
                print(f"Outfit: {row[0]}, Style: {row[1]}, Season: {row[2]}, Gender: {row[3]}, Color: {row[4]}")
    finally:
        connection.close()

# Example usage
get_outfit_recommendations(2, 2, 3)  # Summer, Street, Unisex
