
from urllib import request
import uuid

import pandas as pd
from app.clickhouse.client import get_clickhouse_client
from app.clickhouse.execute import clickhouse_execute
from app.clickhouse.models import CSVTable


async def load_csv_to_clickhouse(df: pd.DataFrame):

    client = get_clickhouse_client()
    table_name = f"csv_{uuid.uuid4().hex}"

    columns = []
    for col_name, dtype in df.dtypes.items():
        ch_type = "String"
        if pd.api.types.is_numeric_dtype(dtype):
            ch_type = "Float64"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            ch_type = "DateTime"
        columns.append({"name": col_name, "type": ch_type})
    
    table = CSVTable(
        table_name=table_name,
        columns=columns
    )
    
    client.execute(table.create_table_sql())

    data = df.where(pd.notnull(df), None).to_dict("records")

    if data:
        print(data)
        for row in data:
            values = ", ".join(
                [
                    f"'{value}'" if isinstance(value, str) else str(value) for value in row.values()
                ]
            )
            values = f"({values})"
            request = """
            INSERT INTO {table_name}
            VALUES {values}""".format(
                table_name=table_name, values=values
            )
            print(request)
            clickhouse_execute(request)

    return table_name