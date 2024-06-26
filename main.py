import time

import db
from facebook import Facebook
from exceptions import *
import s3


def main():
    while True:
        tasks = db.select_tasks()
        if len(tasks) == 0:
            time.sleep(60)
        for task in tasks:
            account = db.select_account_by_id(task.account_id)
            group = db.select_group_by_id(task.group_id)
            content = db.select_content_by_id(task.content_id)
            image = content.image_id
            image_name = s3.get_object_from_s3(image)
            fb = Facebook(email=account.login, password=account.password)
            try:
                fb.execute(group_url=group.link, text=content.text)
                # db.set_task_status(task.id, "Выполнена")
            except (FacebookAuthError, FacebookZeroSubscription, FacebookSubscribeError, Exception) as e:
                if isinstance(e, FacebookAuthError):
                    db.mark_bad_account(account.id)
                if isinstance(e, Exception):
                    e = 'Неизвестная ошибка'
                # db.set_task_status(task.id, str(e))
            finally:
                fb.close()

            exit(0)



if __name__ == '__main__':
    main()