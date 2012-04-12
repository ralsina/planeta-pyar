# -*- coding: utf-8 -*-
import rawdoglib.plugins

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

class MakoPlugin:
    def __init__(self):
        self.lookup = TemplateLookup(directories=['.'], output_encoding='utf-8', encoding_errors='replace')

    def fill_template(self,template, bits, result):
        self.lookup.put_string('actual',template)
        t=self.lookup.get_template('actual')
        try:
            bits2 = {}
            for key, value in bits.items():
                bits2[str(key)] = value
            r=t.render_unicode(**bits2)
        except:
            r=exceptions.html_error_template().render()
        result.value=r
        return False

p = MakoPlugin()
rawdoglib.plugins.attach_hook("fill_template", p.fill_template)
