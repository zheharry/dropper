#!/usr/bin/env python
# encoding: utf-8
"""
command.py

Created by Olli Wang (olliwang@ollix.com) on 2011-04-25.
Copyright (c) 2011 Ollix. All rights reserved.
"""

import sys

import dropbox.auth
import dropbox.client
from oauth import oauth
import oparse.command
import oparse.parser


class DropperCommand(oparse.command.Command):
    """
    The command for uploading file to Dropbox.

    A config file must be provide in the format of
        [auth]
        consumer_key = CONSUMER_KEY
        consumer_secret = CONSUMER_SECRET
        # Fill this once you get the access token
        access_token =
        # The path to put uploaded file
        path =
    """
    usage = '%prog CONFIG_FILE UPLOAD_FILE'

    parser = oparse.parser.OptionParser()
    parser.add_option('--root', action='store', default='dropbox',
                      help='the root of Dropbox operations')

    port = 80
    api_host = 'api.dropbox.com'
    content_host = 'api-content.dropbox.com'
    # Auth
    request_token_url = 'https://api.dropbox.com/0/oauth/request_token'
    access_token_url = 'https://api.dropbox.com/0/oauth/access_token'
    authorization_url = 'https://www.dropbox.com/0/oauth/authorize'
    trusted_access_token_url = 'https://api.dropbox.com/0/token'
    verifier = None

    def command(self, args, options):
        try:
            config_file = args[1]
        except IndexError:
            print 'Config file is not provided'
            return

        try:
            upload_file = args[2]
        except IndexError:
            print 'The file to upload is not provided'
            return

        config = {'server': 'api.dropbox.com',
                  'port': self.port,
                  'request_token_url': self.request_token_url,
                  'access_token_url': self.access_token_url,
                  'authorization_url': self.authorization_url,
                  'trusted_access_token_url': self.trusted_access_token_url,
                  'root': options['root'],
                  'verifier': self.verifier}
        config.update(dropbox.auth.Authenticator.load_config(config_file))
        auth = dropbox.auth.Authenticator(config)

        if not config['access_token']:
            request_token = auth.obtain_request_token()
            url = auth.build_authorize_url(request_token)
            print 'Authorize backsql to access your Dropbox at \n%s' % url

            raw_input('Press enter key while you are done...')

            try:
                access_token = auth.obtain_access_token(request_token,
                                                        self.verifier)
            except AssertionError:
                print "Failed to connect to Dropbox."
                return
            else:
                print 'Connected to Dropbox successfully!'

            print 'Got access token. Copy it to your config file: \n%s' % \
                   access_token.to_string()
            return

        access_token = oauth.OAuthToken.from_string(config['access_token'])
        client = dropbox.client.DropboxClient(self.api_host, self.content_host,
                                              self.port, auth, access_token)
        f = open(upload_file, 'r')
        result = client.put_file(options['root'], config['path'], f).data
        f.close()

        if result is None:
            print 'Unknown error'
        elif 'error' in result:
            print 'Error: %s' % result['error']
        else:
            print 'Uploaded successfully.'

if __name__ == '__main__':
    command = DropperCommand()
    command(*sys.argv)
