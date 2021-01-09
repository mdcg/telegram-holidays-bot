heroku container:push worker
heroku container:release worker
heroku ps:scale worker=1