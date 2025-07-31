# run source setenv.sh to set env variables from dotenv
export $(cat .env | xargs)
