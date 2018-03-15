## harder php? (Web, 769pt)

> almost same as `easy php`
> 
> http://47.52.246.175:23333/

The only difference with [easy php](../easy-php-540/README.md) was in the server configuration (diff shown below) and did not affect our solution from the first challenge. So, the solution for easy php gave us both flags.

**run.sh**

```diff
-(while true;do rm -rf /tmp/*;sleep 2;done)&
+(while true;do rm -rf /tmp/*;sleep 1;done)&
 
-## rm sql
-cd /tmp/
-rm sql.sql
 
+sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/cli/php.ini
+sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/apache2/php.ini
+
+cd /etc/php5/apache2/conf.d/
+rm 20-xdebug.ini
+rm 20-memcached.ini
+rm 20-memcache.ini
+
+rm -r /var/www/phpinfo
+
+rm /app/views/phpinfo
+
+## chmod
```

**clean_danger.sh**

```diff
 cd /app/adminpic/
 rm *.jpg
+cd /var/www/html/adminpic/
+rm *
```

```
N1CTF{i'm sorry for it!!!!:p}
```
