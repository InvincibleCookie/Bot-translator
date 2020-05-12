import random
# С помощью этой библиотеки генерируется
# random_id, которое нужно для того, чтобы не отправлять пользователю одни и те же сообщения несколько раз.
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
# Подключаемся к ВК
from yandex_translate import YandexTranslate

# Импортируем библиотеку яндекс переводчика

translate = YandexTranslate('enter API-kei')
# Создаем API-ключ яндекс переводчика  по этой ссылке https://translate.yandex.ru/developers/keys


flag = False
translat = False
# Создаем флажки, пригодятся

languages = {'az': 'азербайджанский', 'sq': 'албанский', 'am': 'амхарский', 'en': 'английский', 'ar': 'арабский',
             'hy': 'армянский',
             'af': 'африкаанс', 'eu': 'баскский', 'ba': 'башкирский', 'be': 'белорусский', 'bn': 'бенгальский',
             'my': 'бирманский',
             'bg': 'болгарский', 'bs': 'боснийский', 'cy': 'валлийский', 'hu': 'венгерский', 'vi': 'вьетнамский',
             'gl': 'галисийский', 'nl': 'голландский', 'mrj': 'горномарийский', 'el': 'греческий', 'ka': 'грузинский',
             'gu': 'гуджарати',
             'da': 'датский', 'he': 'иврит', 'yi': 'идиш', 'id': 'индонезийский', 'ga': 'ирландский',
             'it': 'итальянский',
             'is': 'исландский', 'es': 'испанский', 'kk': 'казахский',
             'zh': 'китайский', 'ko': 'корейский', 'xh': 'коса', 'km': 'кхмерский', 'lo': 'лаосский', 'la': 'латынь',
             'lv': 'латышский',
             'lt': 'литовский', 'lb': 'люксембургский', 'mg': 'малагасийский', 'ms': 'малайский', 'ml': 'малаялам',
             'mt': 'мальтийский',
             'mk': 'македонский', 'mi': 'маори', 'mr': 'маратхи', 'mhr': 'марийский', 'mn': 'монгольский',
             'de': 'немецкий',
             'ne': 'непальский', 'no': 'норвежский', 'pa': 'панджаби', 'pap': 'папьяменто', 'fa': 'персидский',
             'pl': 'польский',
             'pt': 'португальский', 'ro': 'румынский', 'ru': 'русский', 'ceb': 'себуанский', 'sr': 'сербский',
             'si': 'сингальский',
             'sk': 'словацкий', 'sl': 'словенский', 'sw': 'суахили', 'su': 'сунданский', 'tg': 'таджикский',
             'th': 'тайский',
             'tl': 'тагальский', 'ta': 'тамильский', 'tt': 'татарский', 'te': 'телугу', 'tr': 'турецкий',
             'udm': 'удмуртский',
             'uz': 'узбекский', 'uk': 'украинский', 'ur': 'урду', 'fi': 'финский', 'fr': 'французский', 'hi': 'хинди',
             'hr': 'хорватский', 'cs': 'чешский', 'sv': 'шведский', 'gd': 'шотландский', 'et': 'эстонский',
             'eo': 'эсперанто',
             'jv': 'яванский', 'ja': 'японский'}


# Словарь со всеми поддерживаемыми языками и кодами этих языков

def main():
    global flag
    global languages
    global translat
    # Подключаем в функцию словарь с языками и флажки

    vk_session = vk_api.VkApi(
        token='TOKEN')
    # Создаем группу вк, в разделе управление сообществом переходим в "Работа с API",
    # Включаем LongPoll API и создаем ключ, который вставляем сюда как TOKEN

    longpoll = VkBotLongPoll(vk_session, "id сообщества")
    # На место "id" ставим id нашего сообщества

    vk = vk_session.get_api()
    # Позволяет обращаться к методам API как к обычным классам

    for event in longpoll.listen():
        # Запускаем цикл
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Если от пользователя пришло сообщение, то программа идет дальше
            if event.message['text'].lower().startswith('перевод:'):
                # Если пользователь напишет "перевод:", он активирует команду быстрого перевода
                flag = True
                # Этот флаг нужен, чтобы гарантировать, что программа не вылетит, в случае ошибки
                try:
                    # Мы лишь пробуем сделать перевод, так как иначе в случае ошибки программа перестанет работать
                    trFrom = translate.detect(event.message['text'][8:])
                    # Определяем язык
                    trResult = translate.translate(event.message['text'][8:], trFrom + '-' + 'ru')
                    # Переводим
                except Exception as e:
                    # Если всё-таки что-то пошло не так, переходим сюда
                    print("Exception:", e)
                    # Пишем в консоль об ошибке
                    flag = False
                    # Флаг - это своеобразные ворота, если произошла ошибка, мы эти ворота закрывем.
                    pass
                if flag:
                    # Если всё хорошо и эти "ворота" открыты, пишем перевод пользователю
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        message=str(*trResult['text']),
                        random_id=random.randint(0, 2 ** 64))
                    # Отправляем сообщение
                    continue
                else:
                    # Если произошла ошибка, отправляем пользователю сообщение об этом
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        message='Извините, произошла какая-то ошибка, но ничего страшного, вы можете начать '
                                'перевод сначала',
                        random_id=random.randint(0, 2 ** 64))
                    continue

            if event.message['text'].lower().startswith('перевод-'):
                # Если пользователь напишет "перевод-xx", активируется другой способ перевода
                trTo = event.message['text'][8:]
                # Последними буквами пользователь указывает код языка, на который хочет перевести фразу
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Введите фразу, которую надо перевести",
                                 random_id=random.randint(0, 2 ** 64))
                # бот запрашивает фразу, которую надо перевести
                translat = True
                # Включается флаг translat
                continue

            if translat:
                # Если бот запросил фразу на перевод и активировался флаг, здесь происходит перевод
                text = event.message['text']
                trNormal = True
                try:
                    trFrom = translate.detect(text)
                    # Определяем язык
                    trResult = translate.translate(text, trFrom + '-' + trTo)
                    # Переводим

                except Exception as e:
                    # Если что-то пошло не так
                    trNormal = False
                    # Пинаем флаг ошибки
                    print("Exception:", e)
                    # Пишем в консоль ошибку
                    pass

                if trNormal:
                    # Если всё хорошо
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        message='Переведено сервисом «Яндекс.Переводчик» translate.yandex.ru\n' + str(
                            *trResult['text']),
                        random_id=random.randint(0, 2 ** 64))
                    # Переводим и отправляем текст

                    if 'лох' in event.message['text'].lower().split():
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Сам лох",
                                         random_id=random.randint(0, 2 ** 64))
                    # Если вдруг, в тексте есть слово "лох", мы должны отправить сообщение пользователю
                    # чтобы больше не ругался. (Шутка разработчика)
                    translat = False
                    continue
                else:
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        message='Извините, произошла какая-то ошибка, но ничего страшного, вы можете начать '
                                'перевод сначала',
                        random_id=random.randint(0, 2 ** 64))
                    translat = False
                    # Сообщаем об ошибке в случае таковой
                    continue

            if event.message['text'].lower().startswith('определить язык:'):
                language_detect = True
                # Функция определения языка
                try:
                    language_text = event.message['text'][15:]
                    # выписываем текст после 'определить язык:' в отдельную переменную
                    tr = translate.detect(language_text)
                    # получаем код переводимого языка
                except Exception as e:
                    language_detect = False
                    print("Exception:", e)
                    pass
                if language_detect:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=languages[tr],
                                     random_id=random.randint(0, 2 ** 64))
                    # Если всё хорошо, мы используем код переводимого языка как ключ в словаре,
                    # И отправляем пользователю язык, который является элементом словаря, на который ссылает ключ
                    continue
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Язык не смогли разобрать',
                                     random_id=random.randint(0, 2 ** 64))
                    # Если язык не смогли разобрать, отправляем сообщение об этом.
                    continue

            if event.message['text'].lower() == '/skills':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Я бот, который на данный момент владеет следующими функцими:\n \n \n"
                                         "Быстрый перевод на русский - напиши \n «Перевод:*Фраза на любом языке*»\n \n"
                                         "Пример диалога:\n"
                                         "(Пользователь) — Перевод: Hi\n"
                                         "(Бот-переводчик) — Привет\n \n \n"
                                         "Перевод с любого языка на любой другой"
                                         " - напиши \n «Перевод-*код языка, на который надо перевести*» (Код русского языка - "
                                         "ru, английского - en) \n и отправь, "
                                         "после этого введи фразу на любом языке, которую надо перевести.\n \n"
                                         "Пример диалога:\n"
                                         "(Пользователь) — Перевод-ru\n"
                                         "(Бот-переводчик) — Введите фразу, которую надо перевести\n"
                                         "(Пользователь) — Hello\n"
                                         "(Бот-переводчик) — Привет\n\n\n"
                                         "Определитель языка - «Определить язык: *фраза на языке, который надо определить*»\n \n"
                                         "Пример диалога:\n"
                                         "(Пользователь) — Определить язык: 우저를 사\n"
                                         "(Бот-переводчик) — корейский\n\n\n"
                                         "Все поддерживаемые языки и их кода\n"
                                         " https://yandex.ru/dev/translate/doc/dg/concepts/api-overview-docpage/\n"
                                         "(Если по ссылке пишет, что 'Нет такой страницы',"
                                         " в содержании слева выберите любой пункт,"
                                         "а потом вернитесь к пункту 'Общие сведения')\n\n\n"
                                         "Бот использует переводчик яндекса, который предоставляется бесплатно, одно "
                                         "условие - необходимо указывать ссылку на яндекс переводчик. Боту не сложно, "
                                         "яндексу приятно\n\n\n"
                                         "На данный момент это все функции, но их список будет расширяться",
                                 random_id=random.randint(0, 2 ** 64))
                # Все возможности бота
                continue

            else:
                flag_thanks = False
                flag_hi = False
                try:
                    trFrom = translate.detect(event.message['text'])
                    trResult = translate.translate(event.message['text'], trFrom + '-' + 'ru')
                    if 'спасибо' in str(*trResult['text']).lower() or 'благодар' in str(*trResult['text']).lower():
                        # Если сообщение на любом языке означает "спасибо", активируем "флаг благодарения"
                        flag_thanks = True
                    for e in ['привет', 'здравств', 'доброе утро', 'добрый день', 'добрый вечер']:
                        if e in str(*trResult['text']).lower():
                            # Если сообщение - приветствие на любом языке, включается "привет флаг"
                            flag_hi = True
                            break
                except Exception as e:
                    print("Exception:", e)
                    pass
                if flag_thanks:
                    vk.messages.send(
                        user_id=event.obj.message['from_id'],
                        message="Благодарность принята к сведению",
                        random_id=random.randint(0, 2 ** 64))
                # Если включился "флаг благодарения", мы говорим, что благодарность принята к сведению
                elif flag_hi:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Приветствую. Отправь «/skills» чтобы ознакомиться с моими навыками.",
                                     random_id=random.randint(0, 2 ** 64))
                # Если нам говорят привет, приветствуем пользователя, и говорим на всякий случай команду, сообщающую о
                # навыках бота
                elif 'лох' in event.message['text'].lower().split():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Сам лох",
                                     random_id=random.randint(0, 2 ** 64))
                # Сам лох
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="пь)))\n"
                                             "Если что, отправь «/skills», чтобы получить список команд",
                                     random_id=random.randint(0, 2 ** 64))
                    # В случае неизвестной фразы, отправляем универсальное слово пь)))
                    # А также на всякий случай отправляем команду, сообщающую о всех навыках бота


if __name__ == '__main__':
    main()
