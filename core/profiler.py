def profile_data(df):
    return {
        "row_count": len(df),
        "columns": [
            {"name": c, "dtype": str(df[c].dtype), "unique": df[c].nunique()}
            for c in df.columns
        ]
    }
