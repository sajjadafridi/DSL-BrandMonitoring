class User:
    def __init__(self):

        self.display_name = None
        self.display_picture = None
        self.follower_count=None
        self.following_count=None
        self.total_likes=None
        self.total_post= None
        self.user_id=None
        self.time=None
        self.location=None

    def set_display_name(self, display_name):
        self.display_name = display_name
    def set_display_picture(self, display_picture):
        self.display_picture = display_picture
    def set_time(self, time):
        self.time = time
    def set_follower_count(self, follower_count):
        self.follower_count=follower_count
    def set_following_count (self,following_count):
        self.following_count=following_count
    def set_total_likes(self,total_likes):
        self.total_likes=total_likes
    def set_total_post(self,total_post):
        self.total_post=total_post
    def set_user_id(self,user_id):
        self.user_id=user_id
    def set_location(self, location):
            self.location = location


    def get_display_name(self):
        return self.display_name
    def get_display_picture(self):
        return self.display_picture
    def get_follower_count(self):
        return self.follower_count
    def get_following_count(self) :
        return self.following_count
    def get_total_likes(self):
        return self.total_likes
    def get_total_post(self):
        return self.total_post
    def get_user_id(self):
        return  self.user_id
    def get_time (self):
        return self.time
    def get_location(self):
        return self.location
