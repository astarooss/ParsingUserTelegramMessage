# ParsingUserTelegram
Parser nicknames of the most active users

The execution of this code will bring you the nicknames of the most active users from donor chats in telegram, users who wrote at least one message but in all the chats that you specified will be saved in the database with the highest number, thus you can parse the most active users.

 - 1For the program to work, you will need to register your account in the telegram as a developer account using the link: https://my.telegram.org/auth
![Снимок](https://user-images.githubusercontent.com/97433829/205083446-19e5b62e-3ce4-451e-9bab-852342cc19e1.PNG)

 - after registration you will get api_id and api_hash paste them into config.ini fields
 - in the main.py file, insert links to chats into the URL variable
 - in the file invite_done add the names of users who should not get into the database next time
