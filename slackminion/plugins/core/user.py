from slackminion.plugin.base import BasePlugin


class UserManager(BasePlugin):
    """
    Loads and stores user information
    """
    def on_load(self):

        self._dont_save = True  # Don't save this plugin's state on shutdown
        self.users = {}
        self.admins = {}
        if 'bot_admins' in self._bot.config:
            self.admins = self._bot.config['bot_admins']
        setattr(self._bot, 'user_manager', self)

        super(UserManager, self).on_load()

    def get(self, userid):
        """Retrieve user by userid"""
        if userid in self.users:
            return self.users[userid]
        return None

    def get_by_username(self, username):
        """Retrieve user by username"""
        res = filter(lambda x: x.username == username, self.users.values())
        if len(res) > 0:
            return res[0]
        return None

    def set(self, user):
        """
        Adds a user object to the user manager

        user - a SlackUser object
        """

        self.log.info("Loading user information for %s/%s", user.userid, user.username)
        self.load_user_info(user)
        self.log.info("Loading user rights for %s/%s", user.userid, user.username)
        self.load_user_rights(user)
        self.log.info("Added user: %s/%s", user.userid, user.username)
        self.users[user.userid] = user
        return user

    def load_user_info(self, user):
        """Loads additional user information and stores in user object"""
        # We have no additional information to load, but a child plugin
        # might want to override this
        pass

    def load_user_rights(self, user):
        """Sets permissions on user object"""
        if user.username in self.admins:
            user.is_admin = True