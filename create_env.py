import os

if not os.path.exists("./.env"):
    print("Creating .env file...")

    with open(".env", "w") as env_file:
        env_file.write(
            """
            DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

            #mysql settings 
            MYSQL_ROOT_PASSWORD=my-secret-password
            MYSQL_DATABASE=sampleshare_db
            MYSQL_PASSWORD=my-secret-password

            DB_HOST=db
            DB_PORT=3306
            """
        )
else:
    print(".env file already exists")
