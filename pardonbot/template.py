dialogue = [
    {"sender": "user", "message": "/start"},
    {"sender": "bot", "message": "К сожалению, кто-то из пользователей Telegram посчитал ваши сообщения нежелательными и переслал на проверку нашей команде модераторов. Модераторы подтвердили, что эти сообщения были спамом. Теперь ваш аккаунт ограничен: вы не можете писать тем, кто не сохранил ваш номер в список контактов, а также приглашать других пользователей в группы или каналы и писать в публичных группах. Если пользователи написали вам первым, вы сможете ответить, несмотря на ограничения."},
    {"sender": "user", "message": "Это ошибка"},
    {"sender": "bot", "message": "Если вы считаете, что получили ограничения по ошибке, пожалуйста, сообщите об этом. Все апелляции рассматриваются специалистами из команды Telegram. Обратите внимание, что это не поможет, если ограничения не были ошибочными. Хотите отправить апелляцию?"},
    {"sender": "user", "message": "Да"},
    {"sender": "bot", "message": "Пожалуйста, подтвердите, что вы никогда не отправляли незнакомым людям:\n- Рекламу, которую они не запрашивали\n- Материалы для продвижения чего-либо\n- Шок-контент\nВы отправляли что-нибудь подобное?"},
    {"sender": "user", "message": "Нет, ничего подобного не было."},
    {"sender": "bot", "message": "Хорошо! Простите, если аккаунт ограничили по ошибке. Пожалуйста, расскажите подробнее о вашей ситуации, и я передам эту информацию нашим специалистам. Как вы считаете, что могло привести к ограничениям?"},
    {"sender": "user", "message": "Telegram developers! I have not logged into Telegram for a long time, and have not corresponded in various public groups. However, it seems that my account has been marked as a spammer and most likely blocked! I believe this was not right because I did not do anything special! Therefore, I ask you to remove my restrictions!"},
    {"sender": "bot", "message": "Спасибо! Ваша заявка отправлена. Наши специалисты постараются рассмотреть её как можно быстрее, и если действительно случилась ошибка, все ограничения вскоре будут сняты."},
    {"sender": "bot", "message": "Ваш аккаунт свободен от каких-либо ограничений."}
]



"""
SpamBot:
I’m afraid some Telegram users found your messages annoying and forwarded them to our team of moderators for inspection. The moderators have confirmed the report and your account is now limited until 6 Jun 2024, 20:20 UTC.

While the account is limited, you will not be able to do certain things on Telegram, like writing to strangers who haven’t contacted you first or adding them to groups and channels.

Your account will be automatically released on 6 Jun 2024, 20:20 UTC. Please note that if you repeat what got you limited and users report you again,
the limitations will last longer next time. Subscribers of [Telegram Premium](tg://premium_offer?ref=spambot) have reduced times for initial limitations.

---
К сожалению, кто-то из пользователей Telegram посчитал Ваши сообщения нежелательными и переслал их на проверку команде модераторов. Модераторы подтвердили, что жалоба была обоснованной.

Ваш аккаунт временно ограничен: Вы не можете писать тем, кто не сохранил Ваш номер в список контактов, а также приглашать таких пользователей в группы или каналы. Если незнакомый пользователь напишет Вам первым, Вы сможете ему ответить.

Ограничения будут автоматически сняты 6 Jun 2024, 20:20 UTC (по московскому времени — на три часа позже). Обратите внимание, что если пользователи будут жаловаться на новые нежелательные сообщения от Вас, в следующий раз аккаунт будет ограничен на больший срок. Ограничения, наложенные впервые, снимаются быстрее при наличии действующей подписки Telegram Premium (tg://premium_offer?ref=spambot).
---


SpamBot: Please use buttons to communicate with me.

"""




-----
SpamBot: Hello Лида!

I’m very sorry that you had to contact me. Unfortunately, some actions can trigger a harsh response from our anti-spam systems. If you think your account was limited by mistake, you can submit a complaint to our moderators.

While the account is limited, you will not be able to send messages to people who do not have your number in their phone contacts or add them to groups and channels. Of course, when people contact you first, you can always reply to them.


2024-06-06 15:57:53,863 DEBUG check_keyboard_buttons Клавиатурная кнопка: OK
2024-06-06 15:57:53,863 DEBUG check_keyboard_buttons Клавиатурная кнопка: What is spam?
2024-06-06 15:57:53,863 DEBUG check_keyboard_buttons Клавиатурная кнопка: I was wrong, please release me
2024-06-06 15:57:53,863 DEBUG check_keyboard_buttons Клавиатурная кнопка: This is a mistake

79965344182| ->: This is a mistake

SpamBot: If you think the limitations on your account were applied by mistake, you can submit a complaint. All complaints will be reviewed by the team’s supervisor. Please note that this will have no effect on limitations that were applied with a good reason. Would you like to submit a complaint?

2024-06-06 15:57:59,526 DEBUG check_keyboard_buttons Клавиатурная кнопка: Yes
2024-06-06 15:57:59,526 DEBUG check_keyboard_buttons Клавиатурная кнопка: No


 SpamBot: Great! Please confirm that you have never sent this to strangers:
- Unsolicited advertising of any kind
- Promotional messages
- Shocking materials

Did you ever do any of this?
2024-06-06 16:11:00,491 DEBUG check_keyboard_buttons Клавиатурная кнопка: No! Never did that!
2024-06-06 16:11:00,491 DEBUG check_keyboard_buttons Клавиатурная кнопка: Well… In fact I did.


No! Never did that!


Great! I’m very sorry if your account was limited by mistake. Please write me some details about your case, I will forward it to the supervisor. Why do you think your account was limited, what went wrong?

-> My message

SpamBot: Thank you! Your complaint has been successfully submitted. Our team’s supervisors will check it as soon as possible. If this was a mistake, all limitations will be lifted from your account soon.
-------------------------------------------------------------------------------------------------------
Здравствуйте, Лида!

Очень жаль, что Вы с этим столкнулись. К сожалению, иногда наша антиспам-система излишне сурово реагирует на некоторые действия. Если Вы считаете, что Ваш аккаунт ограничен по ошибке, пожалуйста, сообщите об этом нашим модераторам.

Пока действуют ограничения, Вы не сможете писать тем, кто не сохранил Ваш номер в список контактов, а также приглашать таких пользователей в группы или каналы. Если пользователь написал Вам первым, Вы сможете ответить, несмотря на ограничения.


-> Это ошибка


Если Вы считаете, что получили ограничения по ошибке, пожалуйста, сообщите об этом. Все апелляции рассматриваются специалистами из команды Телеграма. Обратите внимание, что это не поможет, если ограничения не были ошибочными. Хотите отправить апелляцию?

-> Да


Хорошо. Пожалуйста, подтвердите, что Вы никогда не отправляли незнакомым людям:
- Рекламу, которую они не запрашивали
- Материалы для продвижения чего-либо
- Шок-контент

Вы отправляли что-нибудь подобное?


->  Нет, ничего подобного не было.

Хорошо! Простите, если аккаунт ограничен по ошибке. Пожалуйста, расскажите подробнее о Вашей ситуации, и я перешлю эту информацию нашим специалистам. Как Вы считаете, что могло привести к ограничениям?




SpamBot 178220800
------
Good news, no limits are currently applied to your account. You’re free as a bird!
2024-06-06 20:11:25,748 DEBUG check_keyboard_buttons Клавиатурная кнопка: Cool, thanks
2024-06-06 20:11:25,748 DEBUG check_keyboard_buttons Клавиатурная кнопка: But I can’t message non-contacts!




2024-06-06 20:08:39,841 DEBUG send_message_and_wait_for_response 79965344182| SpamBot: Ваш аккаунт свободен от каких-либо ограничений.
2024-06-06 20:08:39,841 DEBUG check_keyboard_buttons Клавиатурная кнопка: Хорошо, спасибо
2024-06-06 20:08:39,841 DEBUG check_keyboard_buttons Клавиатурная кнопка: Но я не могу писать неконтактам


----------

Ограничения будут автоматически сняты


К сожалению, кто-то из пользователей Telegram посчитал Ваши сообщения нежелательными и переслал их на проверку команде модераторов. Модераторы подтвердили, что жалоба была обоснованной.

Ваш аккаунт временно ограничен: Вы не можете писать тем, кто не сохранил Ваш номер в список контактов, а также приглашать таких пользователей в
группы или каналы. Если незнакомый пользователь напишет Вам первым, Вы сможете ему ответить.

Ограничения будут автоматически сняты 10 Jun 2024, 13:45 UTC (по московскому времени — на три часа позже). Обратите внимание, что если пользователи будут жаловаться на новые нежелательные сообщения от Вас, в следующий раз аккаунт будет ограничен на больший срок. Ограничения, наложенные впервые, снимаются быстрее при наличии действующей [подписки Telegram Premium](tg://premium_offer?ref=spambot).




иногда бывает
SpamBot 178220800: К сожалению, кто-то из пользователей Telegram посчитал Ваши сообщения нежелательными и переслал их на проверку команде модераторов. Модераторы подтвердили, что жалоба была обоснованной.

Ваш аккаунт временно ограничен: Вы не можете писать тем, кто не сохранил Ваш номер в список контактов, а также приглашать таких пользователей в группы или каналы. Если незнакомый пользователь напишет Вам первым, Вы сможете ему ответить.

Ограничения будут автоматически сняты 14 Jun 2024, 19:45 UTC (по московскому времени — на три часа позже). Обратите внимание, что если пользователи будут жаловаться на новые нежелательные сообщения от Вас, в следующий раз аккаунт будет ограничен на больший срок. Ограничения, наложенные впервые, снимаются быстрее при наличии действующей [подписки Telegram Premium](tg://premium_offer?ref=spambot).
2024-06-09 22:05:17,628 DEBUG check_keyboard_buttons Клавиатурная кнопка: ОК
2024-06-09 22:05:17,628 DEBUG check_keyboard_buttons Клавиатурная кнопка: Почему на меня могли жаловаться?
2024-06-09 22:05:17,628 DEBUG check_keyboard_buttons Клавиатурная кнопка: Признаю свою вину, снимите ограничения
2024-06-09 22:05:17,628 DEBUG check_keyboard_buttons Клавиатурная кнопка: Это ошибка





убрать [Your Name]


Thank you! Your complaint has been successfully submitted. Our team’s supervisors will check it as soon as possible. If this was a mistake, all limitations will be lifted from your account soon.


Please use buttons to communicate with me.


 <- SpamBot: You've already submitted a complaint recently. Our team’s supervisors will check it as soon as possible. Thank you for your patience.

You've already submitted a complaint recently