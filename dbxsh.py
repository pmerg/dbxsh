#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage:
  dbxcli ls [-lR] <path>
  dbxcli mkdir <path>
  dbxcli rm <path>
  dbxcli cp <from_path> <to_path>
  dbxcli mv <from_path> <to_path>
  dbxcli meta <path>
  dbxcli [options] clear
  dbxcli [options] new <slug> [<ext>]
  dbxcli [options] render [--posts] [--static] [--rss] [--sitemap]
  dbxcli [options] update
  dbxcli [options] mentions [--twitter]
  dbxcli [options] getenv <variable>
  dbxcli -h, --help
  dbxcli --version

Options:
  -p, --path=<path>        top directory of your blog. [default: .]
  -v, --verbose=<level>,   show messages, level=0..2, 0=silent. [default: 1]
"""

from docopt import docopt

import sys
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

__version__ = 0.1

class dbxSh():
	def __init__(self, token):
		self.dbx = dropbox.Dropbox(token)

	def get_metadata(self, path, include_media_info=False):
		return self.dbx.files_get_metadata(path, include_media_info)

	def mkdir(self, path):
		self.dbx.files_create_folder(path)

	def is_dir(self,path):
		if type(self.get_metadata(path)) == dropbox.files.FolderMetadata:
			return True
		else:
			return False

	def is_dir_empty(self,path):
		file_list = self.dbx.files_list_folder(path)
		if file_list.entries:
			return False
		else:
			return True

	def cp(self, from_path, to_path):
		return self.dbx.files_copy(from_path, to_path)

	def mv(self, from_path, to_path):
		return self.dbx.files_move(from_path, to_path)

	def rm(self, path):
		if self.is_dir(path) and not self.is_dir_empty(path):
			print 'Directory not empty: %s.' % path
			return False
		self.dbx.files_delete(path)
		return True

	def print_entry(self, entry, show_meta=False, show_path=False):
		if(show_path):
			filename=entry.path_display
		else:
			filename=entry.name
		if show_meta:
			if type(entry) == dropbox.files.FileMetadata :
				print '{} {:>10} {}'.format(entry.server_modified.strftime('%c'), entry.size, filename.encode('utf-8'))
			else:
				print '{:>35} {}'.format('<DIR>', filename.encode('utf-8'))
		else:
			print filename

	def ls(self, path, recursive=False, listing=False):
		if path=='/':
			path=''
		has_more = True
		cursor = False
		show_path = True if recursive else False
		show_meta = True if listing else False
		while has_more:
			if not cursor:
				file_list = self.dbx.files_list_folder(path, recursive)
			else:
				file_list = self.dbx.files_list_folder_continue(cursor)
			for entry in file_list.entries:
				self.print_entry(entry, show_meta=show_meta, show_path=show_path)
			has_more = file_list.has_more
			cursor = file_list.cursor

if __name__ == '__main__':
	args = docopt(__doc__, version=__version__)
	DBX_TOKEN = os.environ.get('DBXSH_TOKEN')
	if not DBX_TOKEN:
		print """$DBXSH_TOKEN is not set.
1. Visit https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/ to learn how to generate an access token for your account
2. export DBXSH_TOKEN=<access token>
"""
		sys.exit(1)

	dbx_shell = dbxSh(DBX_TOKEN)

	if args['ls']:
		recursive = args['-R']
		listing = args['-l']
		dbx_shell.ls(path=args['<path>'], recursive=recursive, listing=listing)
	if args['mkdir']:
		dbx_shell.mkdir(path=args['<path>'])
	if args['rm']:
		dbx_shell.rm(path=args['<path>'])
	if args['meta']:
		print dbx_shell.get_metadata(path=args['<path>'])
	if args['cp']:
		print dbx_shell.cp(from_path=args['<from_path>'], to_path=args['<to_path>'])
	if args['mv']:
		print dbx_shell.mv(from_path=args['<from_path>'], to_path=args['<to_path>'])
