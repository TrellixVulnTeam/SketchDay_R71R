from tqdm import tqdm
from task.ml.clipit import clipit
from task.ml.text2art import Text2Art
from channels.consumer import SyncConsumer
from diary.models import Diary
from PIL import Image

class BackgroundTaskConsumer(SyncConsumer) :
    def sketch(self, message) :
        prompts = message['prompts']
        output = 'static/diary_img/'+ message['userId'] + '.png'
        text2art = Text2Art()
        settings = text2art.do_init(prompts=prompts, output=output)
        cur_iteration = 0
        try :
            with tqdm() as pbar :
                while True :
                    try :
                        clipit.train(settings, cur_iteration)
                        if cur_iteration == settings.iterations :
                            break
                        cur_iteration += 1
                        pbar.update()
                    except RuntimeError as e:
                        print('error: ', e)
        except KeyboardInterrupt:
            pass
        # model에 데이터 저장
        create_image = Image.open(output)
        diary = Diary.objects.get(id=message['diaryID'])
        diary.image = create_image
        print('end')