
def profile_data(df):
    return {
        "columns": [
            {"name": c, "dtype": str(df[c].dtype)}
            for c in df.columns
        ],
        "row_count": len(df)
    }
