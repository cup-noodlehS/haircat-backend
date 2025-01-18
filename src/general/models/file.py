from django.db import models

class File(models.Model):
    '''
    **Fields:**
    - name: CharField to store the name of the file.
    - url: URLField to store the URL where the file is located.
    - created_at: DateTimeField to store when the file was created.
    - removed: BooleanField to indicate whether the file has been removed.
    '''

    name = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
