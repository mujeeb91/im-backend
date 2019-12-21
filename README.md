### How to run
#### Database
```docker run --name db -e MYSQL_ROOT_PASSWORD=rootpassword -p 3306:3306 -d mysql```

If the database does not exists, create it,

```
docker exec -it <containerid> bash
mysql -u root -p
CREATE DATABASE instant_messaging;
```

#### Backend
```flask run```
