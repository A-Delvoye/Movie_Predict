# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoviescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        duration = adapter.get('duration')[0]
        duration = duration.strip('min')
        hour, sep, minutes = duration.partition('h ')
        duration = int(hour)*60+int(minutes)
        adapter['duration']= duration

        trailer_view = adapter.get('trailer_views')
        print(trailer_view)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~')
        trailer_view=trailer_view.strip(' vues')
        head, sep, tail= trailer_view.partition('\u202f')
        print(head)
        print('#######################')
        print(tail)
        adapter['trailer_views']=int(head+tail)

        return item

