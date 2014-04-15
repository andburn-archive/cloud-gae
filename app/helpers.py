import ConfigParser


class Configuration(object):

    DEFAULT_SECTION = 'Default'
    APP_SECTION = 'AppEngine'

    def __init__(self, filename):
        super(Configuration, self).__init__()
        # set default config
        self.name = 'Default App'
        self.appid = 'default'
        self.apphost = 'localhost'
        # set config from file
        self.setup(filename)
    # end - init

    def setup(self, filename):
        # read config file
        config = ConfigParser.RawConfigParser()
        config.readfp(open(filename))

        # set variables from file
        self.name = config.get(self.DEFAULT_SECTION, 'Name')
        self.appid = config.get(self.APP_SECTION, 'AppId')
        self.apphost = config.get(self.APP_SECTION, 'AppHost')
    # end - setup

# end - Config