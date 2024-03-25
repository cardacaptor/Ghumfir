from feed.models.post import *

uniqueCaptions = set()
for i in Post.objects.all():
    if(i.caption in uniqueCaptions):
        i.delete()
        continue
    uniqueCaptions.add(i.caption)