#!/bin/bash
heroku login
heroku git:remote -a <APP_NAME>
heroku stack:set container
git push heroku main
heroku ps:scale worker=1
heroku logs --tail