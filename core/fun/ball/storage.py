import random

eight_ball_answers = {
    "ru_ru": (
        "Бесспорно!",
        "Да, это предрешено звёздами и судьбой!",
        "Никаких сомнений",
        "Определённо да",
        "Можешь быть уверен в утвердительном ответе на свой вопрос",
        "Вероятнее всего",
        "Звёзды говорят 'да'",
        "Да",
        "Пока что ещё сложно сказать, попробуй ещё раз"
        "Спроси позже",
        "Об этом лучше не рассказывать",
        "Сейчас нельзя это сказать",
        "Спроси ещё раз",
        "Да быть такого не может!"
        "Конечно же нет!",
        "Весьма сомнительно",
        "Нет! Нет! Нет! Нет!",
        "Нет"
    ),
    "en_us":
        ('As I see it, yes.',
         'Yes.',
         'Positive',
         'Without a doubt ',
         'From my point of view, yes',
         'Convinced.',
         'Most Likley.',
         'Chances High',
         'No.',
         'Very doubtful',
         'Don’t count on it',
         'Negative.',
         'Not Convinced.',
         'Perhaps.',
         'Not Sure',
         'Maybe',
         'Outlook good',
         'I cannot predict now.',
         'Im to lazy to predict.',
         'Concentrate and ask again'
         'I am tired. *proceeds with sleeping*')
}


def get_eight_ball_answer(guild_locale) -> str:
    return random.choice(eight_ball_answers[guild_locale])
