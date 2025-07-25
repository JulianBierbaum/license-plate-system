import os


class Settings:
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "")

    db_url: str = (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
    )

    csv_file: str = os.path.join(os.getenv("CSV_PATH", ""), "vehicle_data.csv")
    municipalities_json_file: str = os.getenv("MUNICIPALITIES_JSON_FILE", "")
    save_dir: str = os.getenv("SAVE_DIR", "")
    synology_host: str = os.getenv("SYNOLOGY_HOST", "")
    synology_username: str = os.getenv("SYNOLOGY_USERNAME", "")
    synology_password: str = os.getenv("SYNOLOGY_PASSWORD", "")
    api_key: str = os.getenv("API_KEY", "")
    save_images_for_debug: bool = (
        os.getenv("SAVE_IMAGES_FOR_DEBUG", "False").lower() == "true"
    )


settings = Settings()
