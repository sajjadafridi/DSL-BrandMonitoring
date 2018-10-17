# from SMM.models import *
# from SMM.PostMessage import Message
from datetime import datetime, timedelta


time_threshold = datetime.now() - timedelta(hours=5)
print(datetime.now().day)
print(time_threshold)


#
# class Influencer:
#     def get_interactions(self, keyword_id, time):
#         post_table = Post.objects.select_related('PostUser').filter(Keyword_id=keyword_id)
#         # post_table=Post.objects.filter(Keyword_id=alert_id)
#         for post in post_table:
#
#             message = Message()
#             message.set_ID(post.id)
#             message.set_statusID(post.StatusID)
#             message.set_Sentiment(post.Sentiment)
#             message.set_Content(post.Content)
#             message.set_CreatedAt(post.CreatedAt)
#             message.set_ResharerCount(post.ResharerCount)
#             message.set_DisplayName(post.PostUser.DisplayName)
#             message.set_DisplayPicture(post.PostUser.DisplayPicture)
#             message.set_UserID(post.PostUser.UserID)
#





