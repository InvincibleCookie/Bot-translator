import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from yandex_translate import YandexTranslate  # Импортируем библиотеку

translate = YandexTranslate('trnsl.1.1.20200506T024548Z.2b01b3880aaca6e8.1bfca8ad717538da8bc43c7ed203ea354bf2943d')

flag = False
language = False
translat = False

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


def main():
    global flag
    global languages
    global language
    global translat

    vk_session = vk_api.VkApi(
        token='fbad5600dad2bca71dcb11ed96c3952e6daca6c50ca207c37833ab040e3dcb19b9f50e09cf0a31433f85c')
    longpoll = VkBotLongPoll(vk_session, "195184104")
    vk = vk_session.get_api()

    for event in longpoll.listen():
        language_detect = True

        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message['text'].lower().startswith('перевод:'):
                flag = True
                try:
                    trFrom = translate.detect(event.message['text'][8:])  # Определяем язык
                    trResult = translate.translate(event.message['text'][8:], trFrom + '-' + 'ru')  # Переводим
                except Exception as e:  # Если что-то пошло не так
                    print("Exception:", e)  # Пишем в консоль
                    flag = False
                    pass
                if flag:
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.obj.message['from_id'],
                        message=str(*trResult['text']),
                        random_id=random.randint(0, 2 ** 64))
                    continue
                else:
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.obj.message['from_id'],
                        message='Извините, произошла какая-то ошибка, но ничего страшного, вы можете начать '
                                'перевод сначала',
                        random_id=random.randint(0, 2 ** 64))
                    continue

            if event.message['text'].lower().startswith('перевод-'):
                trTo = event.message['text'][8:]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Введите фразу, которую надо перевести",
                                 random_id=random.randint(0, 2 ** 64))
                translat = True
                continue

            if translat:
                text = event.message['text']
                trNormal = True
                try:
                    trFrom = translate.detect(text)
                    # Определяем язык
                    trResult = translate.translate(text, trFrom + '-' + trTo)
                    # Переводим
                except Exception as e:  # Если что-то пошло не так
                    trNormal = False  # Пинаем флаг ошибки
                    print("Exception:", e)  # Пишем в консоль
                    pass

                if trNormal:
                    # Если всё хорошо
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.obj.message['from_id'],
                        message='Переведено сервисом «Яндекс.Переводчик» translate.yandex.ru\n' + str(
                            *trResult['text']),
                        random_id=random.randint(0, 2 ** 64))

                    if 'лох' in event.message['text'].lower().split():
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Сам лох",
                                         random_id=random.randint(0, 2 ** 64))

                    translat = False
                    continue
                else:
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.obj.message['from_id'],
                        message='Извините, произошла какая-то ошибка, но ничего страшного, вы можете начать '
                                'перевод сначала',
                        random_id=random.randint(0, 2 ** 64))
                    translat = False
                    continue

            if event.message['text'].lower().startswith('определить язык:'):
                try:
                    language_text = event.message['text'][15:]
                    tr = translate.detect(language_text)
                except Exception as e:  # Если что-то пошло не так
                    language_detect = False  # Пинаем флаг ошибки
                    print("Exception:", e)  # Пишем в консоль
                    pass
                if language_detect:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=languages[tr],
                                     random_id=random.randint(0, 2 ** 64))
                    continue
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Язык не смогли разобрать',
                                     random_id=random.randint(0, 2 ** 64))
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
                continue

            else:
                flag_thanks = False
                flag_hi = False
                try:
                    trFrom = translate.detect(event.message['text'])  # Определяем язык
                    trResult = translate.translate(event.message['text'], trFrom + '-' + 'ru')
                    if 'спасибо' in str(*trResult['text']).lower() or 'благодар' in str(*trResult['text']).lower():
                        flag_thanks = True
                    for e in ['привет', 'здравств', 'доброе утро', 'добрый день', 'добрый вечер']:
                        if e in str(*trResult['text']).lower():
                            flag_hi = True
                            break
                except Exception as e:  # Если что-то пошло не так
                    print("Exception:", e)  # Пишем в консоль
                    pass
                if flag_thanks:
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.obj.message['from_id'],
                        message="Благодарность принята к сведению",
                        random_id=random.randint(0, 2 ** 64))
                elif flag_hi:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Приветствую. Отправь «/skills» чтобы ознакомиться с моими навыками.",
                                     random_id=random.randint(0, 2 ** 64))
                elif 'лох' in event.message['text'].lower().split():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Сам лох",
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="пь)))\n"
                                             "Если что, отправь «/skills», чтобы получить список команд",
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
