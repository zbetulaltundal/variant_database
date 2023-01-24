
# Varyant Veritabanı

5 farklı varyant veritabanındaki (UniProt Variants, ClinVar, ClinGen, CIViC, PharmGKB) verileri bir arada toplayan, bu veritabanlarının offline biçimde erişilebilir ve sorgulanabilir olmasını amaçlayan bir uygulamadır.
Ayriyeten kullanıcı tarafından veritabanına yeni varyant eklenmesini de mümkün kılar. 

# Kurulum
Repository zip formatında veya 'git clone' komutuyla indirebilir.

### Git Komutu
```bash
git clone git@github.com:zbetulaltundal/variant_database.git 
```

PostgreSQL(10.22) ve python(3.10) kurulu olmalıdır. 

Repository'nin indirildiği dizine gidilerek gerekli paketler aşağıdaki komutlarla indirilir: 

```bash
pip install -r .\web_app\requirements.txt
pip install -r .\database\requirements.txt
```

Veritabanlarını lokalde çalıştırmak için aşağıdaki komut çalıştırılır:

```bash
python .\database\backup.py 
```

Sonrasında 

# Kullanım
Repository'nin indirildiği dizinde aşağıdaki komut çalıştırılır:

```bash
python .\web_app\app.py
```

Programın hangi URL'de çalıştığına dair bir çıktı alınır:
 
```bash
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.1.120:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 120-867-965
127.0.0.1 - - [24/Jan/2023 14:53:12] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2023 14:53:12] "GET /static/custom/css/app.css HTTP/1.1" 304 -
127.0.0.1 - - [24/Jan/2023 14:53:12] "GET /static/custom/js/app.js HTTP/1.1" 304 -
```

http://127.0.0.1:8080 adresini tarayıcıda açarak uygulamaya erişebilirsiniz. 

