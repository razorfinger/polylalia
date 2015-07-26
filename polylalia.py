#!/usr/bin/env python

import argparse
import os
import sys
import time
import yandex_translate

class PolylaliaException(Exception):
    pass

class Polylalia(object):

    translator = None
    directions = None

    def __init__(self, config):
        if config.api_key is None:
            raise PolylaliaException('An API key is required.')
        routemap = [config.begin_lang] + config.intermediate_langs.split(',') + [config.end_lang]
        self.delay = int(config.request_delay)
        self.route = self._get_language_routes(routemap)
        self.translator = yandex_translate.YandexTranslate(config.api_key)
        self._sanity_check_language_choices(routemap)
        self._sanity_check_route(self.route)

    def transform(self, text):
        orig_text = text
        for direction in self.route:
            result = self.translator.translate(text, direction)
            if result['code'] == 200 and len(result['text']):
                text = ' '.join(result['text']).strip()
            else:
                raise PolylaliaException('Translation from Yandex failed.', result)
            time.sleep(self.delay)
        if text is orig_text:
            raise PolylaliaException('Text matches exactly after transform! This is bad.')
        return text

    def get_available_transforms(self):
        if self.directions is None:
            self.directions = self.translator.directions
        return self.directions

    def _get_translation(self, plaintext, translation_direction):
        return self.translator.translate(plaintext, translation_direction)

    def _get_language_routes(self, lang_list):
        routes = []
        listlen = len(lang_list)
        for i in xrange(listlen):
            if (i+1) < listlen:
                routes.append(lang_list[i] + '-' + lang_list[i+1])
        return routes

    def _sanity_check_language_choices(self, choices):
        allowed_dirs = self.get_available_transforms()
        langs = []
        for d in allowed_dirs:
            langs += d.split('-')
        langs = set(langs)
        for choice in choices:
            if choice not in langs:
                raise PolylaliaException("Language with prefix %s is not a valid option." % choice)

    def _sanity_check_route(self, proposed_dirs):
        allowed_dirs = self.get_available_transforms()
        for proposal in proposed_dirs:
            if proposal not in allowed_dirs:
                lang = proposal.split('-')
                raise PolylaliaException("Cannot make translation from %s to %s." % (lang[0], lang[1]))


def main():
    parser = argparse.ArgumentParser(description='An antistylometric language mixer based on Yandex translate API.')
    parser.add_argument('--display-options', action='store_true', default=False, help='Display available translation mixes.')
    parser.add_argument('--begin-lang', default='en', help='Beginning language.')
    parser.add_argument('--end-lang', default='en', help='Ending language.')
    parser.add_argument('--intermediate-langs', default='sk,en,fi', help='Intermediate languages to route through.')
    parser.add_argument('--api-key', help='Yandex translate api key.')
    parser.add_argument('--request-delay', default=1, help='Number of seconds to delay in between translation requests.')
    parser.add_argument('--output', help='File to output to. Defaults to stdout.')
    parser.add_argument('infile', nargs='?', help='Input file. use - for stdin.')
    args = parser.parse_args()

    if args.api_key is None and os.path.isfile('.yandex_api_key'):
        args.api_key = open('.yandex_api_key', 'r').read().strip()

    if args.display_options is True:
        poly = Polylalia(args)
        dirs = poly.get_available_transforms()
        s = ''
        if len(dirs):
            for d in dirs:
                s += d + ','
            s = s[0:len(s)-1]
        print "Available translation routes: %s" % s
        sys.exit(0)
    else:
        if args.infile is '-':
            fh = sys.stdin
        elif os.path.isfile(args.infile):
            fh = open(args.infile, 'r')
        else:
            raise PolylaliaException("Could not find a file %s to input." % args.infile)
        contents = fh.read().decode('utf8')
        poly = Polylalia(args)
        mixed_content = unicode(poly.transform(contents))
        if len(args.output):
            with open(args.output, 'w') as f:
                f.write(mixed_content.encode('utf8'))
        else:
            print mixed_content
        sys.exit(0)

if __name__ == '__main__':
    main()
