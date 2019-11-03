import os, django, random, argparse
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Lesson, Commendation, Chastisement


def get_schoolkid(schoolkid_name):
    try:
        kid = Schoolkid.objects.filter(full_name__contains=schoolkid_name).get()
        return kid
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        print("Schoolkid name '{}' doesn't exist.".format(schoolkid_name))


def fix_marks(child_name):
    kid = get_schoolkid(child_name)
    Mark.objects.filter(
        schoolkid=kid, points__in=(2, 3)
    ).update(points=5)


def remove_chastisements(child_name):
    kid = get_schoolkid(child_name)
    chastisments = Chastisement.objects.filter(schoolkid=kid)
    chastisments.delete()


def get_random_commendation():
    commendation_list = ('Молодец!', 'Отлично!', 'Хорошо!',
                         'Гораздо лучше, чем я ожидал!',
                         'Ты меня приятно удивил!',
                         'Великолепно!',
                         'Прекрасно!', 'Ты меня очень обрадовал!',
                         'Именно этого я давно ждал от тебя!',
                         'Сказано здорово – просто и ясно!',
                         'Ты, как всегда, точен!',
                         'Очень хороший ответ!', 'Талантливо!',
                         'Ты сегодня прыгнул выше головы!',
                         'Я поражен!', 'Уже существенно лучше!',
                         'Потрясающе!', 'Змечательно!',
                         'Прекрасное начало!', 'Так держать!',
                         'Ты на верном пути!', 'Здорово!',
                         'Это как раз то, что нужно!', 'Я тобой горжусь!',
                         'С каждым разом у тебя получается всё лучше!',
                         'Мы с тобой не зря поработали!',
                         'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                         'Ты многое сделал, я это вижу!',
                         'Теперь у тебя точно все получится!',
                         )
    return random.choice(commendation_list)


def get_lessons(schoolkid, lesson_name):
    return Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=lesson_name,
    )


def create_commendation(child_name, lesson_name):
    # kid = Schoolkid.objects.filter(full_name__contains=child_name).get()
    kid = get_schoolkid(child_name)
    if not kid:
        return False

    last_kid_lesson = Lesson.objects.filter(
        year_of_study=kid.year_of_study,
        group_letter=kid.group_letter,
        subject__title__contains=lesson_name,
    ).latest('date')

    random_commendation = get_random_commendation()

    new_commendation = Commendation.objects.create(
        text=random_commendation,
        created=last_kid_lesson.date,  # Дата похвалы совпадет с датой урока.
        schoolkid=kid,
        subject=last_kid_lesson.subject,
        teacher=last_kid_lesson.teacher,
    )
    return new_commendation


def set_cli_argument_parse():
    parser = argparse.ArgumentParser(
        description="The hack script for repo: https://github.com/devmanorg/e-diary"
    )

    subparsers = parser.add_subparsers(title='subcommands',
                                      description='valid subcommands',
                                      help='function description'
                                      )

    # create the parser for the "foo" command
    parser_comm = subparsers.add_parser('new-comm', help='create commendation')
    parser_comm.add_argument('-kname', dest="child_name",
                             type=str, help='schoolkid name')
    parser_comm.add_argument('-lesson', dest="lesson_name",
                             type=str, help='lesson name')
    parser_comm.set_defaults(func=create_commendation)

    parser_rmchast = subparsers.add_parser('rm-chast',
                                           help='remove chastisements'
                                           )
    parser_rmchast.add_argument('-kname', dest="child_name",
                                type=str, help='schoolkid name')
    parser_rmchast.set_defaults(func=remove_chastisements)

    parser_fix_marks = subparsers.add_parser(
        'fix-marks', help='remove bad marks and replace them by 5'
                                           )
    parser_fix_marks.add_argument('-kname', dest="child_name",
                                  type=str, help='schoolkid name')
    parser_fix_marks.set_defaults(func=fix_marks)

    return parser.parse_args()


if __name__ == '__main__':

    cli_argument_parser = set_cli_argument_parse()
    print(cli_argument_parser)
    if cli_argument_parser.func == create_commendation:
        cli_argument_parser.func(
            cli_argument_parser.child_name, cli_argument_parser.lesson_name
        )
    if cli_argument_parser.func in (remove_chastisements, fix_marks):
        cli_argument_parser.func(cli_argument_parser.child_name)
