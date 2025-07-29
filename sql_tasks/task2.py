TASK2_QUERY = """
    WITH Ranked AS (
        SELECT 
            Группа,
            Возраст,
            Рост,
            MAX(Рост) OVER (PARTITION BY Группа) AS МаксРост,
            MIN(Рост) OVER (PARTITION BY Группа) AS МинРост
        FROM Группы
    )
    SELECT 
        Группа,
        AVG(CASE WHEN Рост = МаксРост THEN Возраст END) AS СреднийВозрастМаксРост,
        AVG(CASE WHEN Рост = МинРост THEN Возраст END) AS СреднийВозрастМинРост
    FROM Ranked
    GROUP BY Группа
"""