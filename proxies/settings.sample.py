BOT_NAME = 'proxies'

SPIDER_MODULES = ['proxies.spiders']
NEWSPIDER_MODULE = 'proxies.spiders'

ITEM_PIPELINES = [
    'proxies.pipelines.ProxiesPipeline'
]
