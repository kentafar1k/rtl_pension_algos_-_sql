TASK1_QUERIES = {
    "not_exists": """
        SELECT a.Имя, a.Фамилия
        FROM A a
        WHERE NOT EXISTS (
            SELECT 1 FROM Б b 
            WHERE b.Имя = a.Имя AND b.Фамилия = a.Фамилия
        )
    """,

    "left_join": """
        SELECT a.Имя, a.Фамилия
        FROM A a
        LEFT JOIN Б b ON a.Имя = b.Имя AND a.Фамилия = b.Фамилия
        WHERE b.Имя IS NULL
    """,

    "except": """
        SELECT Имя, Фамилия FROM A
        EXCEPT
        SELECT Имя, Фамилия FROM Б
    """
}