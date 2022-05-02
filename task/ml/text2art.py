from code import interact
from task.ml.clipit import clipit

class Text2Art() :

    def __init__(self) :
        clipit.reset_settings()

    def do_init(self, prompts, output) :
        global settings
        quality = 'normal'
        aspect = 'widescreen'

        clipit.add_settings(prompts=prompts, output=output, quality=quality, aspect=aspect, iterations=1, save_every=1)
        settings = clipit.apply_settings()
        clipit.do_init(settings)

        return settings

    def do_run(self) :
        global settings
        clipit.do_run(settings)