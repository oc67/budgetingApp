from django.db import models

# Create your models here.
class Notifications(models.Model):
    
    notification_ID=models.AutoField(primary_key=True)

    #all_notifications=[("Welcome to the app!","Welcome to the app!"),
   #                     ("A user has sent you one budget","A user has sent you one budget"),
    #                   ]
    notification_text=models.CharField(max_length=500,#choices=all_notifications,
                                       null=False,blank=False)
    
    notification_time=models.TimeField(null=False,blank=False)
    notification_viewer=models.ForeignKey("accounts.CustomUser",null=False,blank=False,
                                   on_delete=models.CASCADE)
    

    def __str__(self):
        return self.notification_text