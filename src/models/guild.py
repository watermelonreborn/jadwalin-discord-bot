class Guild():
    def __init__(self, id):
        self.id = id
        self.text_channel_id = None

    def __init__(self, id, text_channel_id):
        self.id = id
        self.text_channel_id = text_channel_id

    def get_id(self):
        return self.id

    def get_text_channel_id(self):
        return self.text_channel_id

    def set_text_channel_id(self, text_channel_id):
        self.text_channel_id = text_channel_id
        return self.text_channel_id