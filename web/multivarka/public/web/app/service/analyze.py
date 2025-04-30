from typing import List, Dict, Any
from app.clickhouse.client import get_clickhouse_client

async def analyze_columns(table_name: str) -> List[Dict[str, Any]]:
    client = get_clickhouse_client()
    
    columns_info = client.execute(f"""
    SELECT name, type FROM system.columns 
    WHERE table = '{table_name}' AND database = 'default'
    """)
    
    results = []
    for col_name, col_type in columns_info:
        numeric_type = any(t in col_type.lower() for t in ['int', 'float', 'decimal'])
        
        if numeric_type:
            stats_query = f"""
            SELECT
                count() as count,
                countIf({col_name} IS NULL) as null_count,
                min({col_name}) as min,
                max({col_name}) as max,
                median({col_name}) as median,
                avg({col_name}) as mean
            FROM {table_name}
            """
        else:
            stats_query = f"""
            SELECT
                count() as count,
                countIf({col_name} IS NULL) as null_count,
                min({col_name}) as min,
                max({col_name}) as max,
                NULL as median,
                NULL as mean
            FROM {table_name}
            """
        
        stats = client.execute(stats_query)[0]
        
        try:
            mode = client.execute(f"""
            SELECT {col_name} as mode_value
            FROM {table_name}
            WHERE {col_name} IS NOT NULL
            GROUP BY {col_name}
            ORDER BY count() DESC
            LIMIT 1
            """)
            mode_value = mode[0][0] if mode else None
        except Exception as e:
            print(f"Error calculating mode for {col_name}: {str(e)}")
            mode_value = None
        
        additional_stats = {}
        if not numeric_type:
            try:
                str_stats = client.execute(f"""
                SELECT
                    avg(length(toString({col_name}))) as avg_length,
                    min(length(toString({col_name}))) as min_length,
                    max(length(toString({col_name}))) as max_length
                FROM {table_name}
                WHERE {col_name} IS NOT NULL
                """)[0]
                additional_stats.update({
                    "avg_length": str_stats[0],
                    "min_length": str_stats[1],
                    "max_length": str_stats[2]
                })
            except Exception as e:
                print(f"Error calculating string stats for {col_name}: {str(e)}")
        
        results.append({
            "column": col_name,
            "type": col_type,
            "count": stats[0],
            "null_count": stats[1],
            "min": stats[2],
            "max": stats[3],
            "median": stats[4] if numeric_type else None,
            "mean": stats[5] if numeric_type else None,
            "mode": mode_value,
            **additional_stats
        })
    
    return results