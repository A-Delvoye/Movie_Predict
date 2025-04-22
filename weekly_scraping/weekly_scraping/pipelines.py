from itemadapter import ItemAdapter

class MoviescraperPipeline:
    
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)


        trailer_views = adapter.get('trailer_views')
        if trailer_views:
            trailer_views = trailer_views.strip(' vues')  
            trailer_views = trailer_views.replace('\u202f', '')
            try:
                trailer_views = int(trailer_views) 
            except ValueError:
                trailer_views = 0 
        else:
            trailer_views = 0 

        adapter['trailer_views'] = trailer_views

        duration = adapter.get('duration')
        if duration:
            duration = duration.strip('min')  
            hour, sep, minutes = duration.partition('h ')  
            try:
                duration = int(hour) * 60 + int(minutes) 
            except ValueError:
                duration = 0  
        else:
            duration = 0  

        adapter['duration'] = duration


        return item
