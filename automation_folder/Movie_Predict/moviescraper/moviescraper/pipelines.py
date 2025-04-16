# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoviescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        duration = adapter.get('duration')
        if duration!="":
            duration = duration.strip('min')
            hour, sep, minutes = duration.partition('h ')
            duration = int(hour)*60+int(minutes)
            adapter['duration']= duration
        
        release_date = adapter.get('release_date')
        try: 
            release_date.strip()
            adapter['release_date']=release_date.strip()
        except:
            pass

        trailer_view = adapter.get('trailer_views')
        trailer_view=trailer_view.strip(' vues')
        trailer_view=trailer_view.replace('\u202f', '')
        adapter['trailer_views']=trailer_view
        return item

