import json

class Message:

    def set_statusID(self,statusID):
        self.statusID=statusID
    def get_statusID(self):
        return self.statusID

    def set_ID(self, ID):
        self.ID =ID
    def get_ID(self):
        return self.ID

    def set_Sentiment(self,Sentiment):
        self.Sentiment =Sentiment
    def get_Sentiment(self):
        return self.Sentiment

    def set_Content(self, Content):
        self.Content = Content
    def get_Content(self):
        return self.Content

    def set_CreatedAt(self, CreatedAt):
        self.CreatedAt = CreatedAt
    def get_CreatedAt(self):
        return self.CreatedAt

    def set_ResharerCount(self, ResharerCount):
        self.ResharerCount = ResharerCount
    def get_ResharerCount(self):
        return self.ResharerCount

    def set_Source(self, Source):
        self.Source = Source
    def get_Source(self):
        return self.Source

    def set_DisplayName(self, DisplayName):
        self.DisplayName = DisplayName
    def get_DisplayName(self):
        return self.DisplayName

    def set_DisplayPicture(self, DisplayPicture):
        self.DisplayPicture = DisplayPicture
    def get_DisplayPicture(self):
        return self.DisplayName

    def set_UserID(self, UserID):
        self.UserID = UserID
    def get_UserID(self):
        return self.UserID

    def set_EscapedContent(self, EscapedContent):
        self.EscapedContent = EscapedContent
    def get_EscapedContent(self):
        return self.EscapedContent

    def toJSON(self):
        return json.dumps(vars(self))
        # return json.dumps(self, default=lambda o: o.__dict__,
        #                   sort_keys=True, indent=4)

    # @staticmethod
    # def toJSON(posts):
    #     return json.dumps(posts, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)