from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from task.consumers import BackgroundTaskConsumer

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'background_tasks': BackgroundTaskConsumer,
    })
})