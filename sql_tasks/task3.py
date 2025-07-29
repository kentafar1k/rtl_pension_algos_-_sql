TASK3_QUERY = """
    WITH Numbered AS (
        SELECT 
            Number,
            LEAD(Number) OVER (ORDER BY Number) AS NextNumber
        FROM Numbers
    )
    SELECT 
        Number + 1 AS "Left",
        NextNumber - 1 AS "Right"
    FROM Numbered
    WHERE NextNumber - Number > 1
"""