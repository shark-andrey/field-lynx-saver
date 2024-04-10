# Saving FinishLynx Data


## Установка

На виртуалке с сайтом выполни, поменяв `DB_URL`.
Формат: `mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}`

```bash
cd ~
git clone https://github.com/fertilis/finish-lynx-saver.git
cd finish-lynx-saver
cat > .env <<EOT
DB_URL=mysql+asyncmy://root:password@localhost:3306/dev
PORT=10000
EOT
make build
```

## Запуск

```bash
cd ~/finish-lynx-saver && make run
```


## Остановка

```bash
cd ~/finish-lynx-saver && make stop
```

## Логи

```bash
cd ~/finish-lynx-saver && make logs
```


## Testing (это игнорируй, мне для справки)

```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:latest
mysql --protocol=tcp -hlocalhost -uroot -p
```

```bash
telnet localhost 10000
4,1,1,,13,5,11.08 ,,-0.9 </A SE;4,1,1,,190,4,11.15 ,,-0.9 </A SE;4,1,1,,116,6,12.24 ,,-0.9 </A SE;4,1,1,,297,8,12.29 ,,-0.9 </A SE;4,1,1,,72,2,12.71 ,,-0.9 </A SE;4,1,1,,93,7,13.23 ,,-0.9 </A SE;4,1,1,,171,1,15.42 ,,-0.9 </A SE;4,1,1,,140,3,,,-0.9 </A SE;
```
