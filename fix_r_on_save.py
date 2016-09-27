import sublime, sublime_plugin
import re


# bad_equals_spacing = r '[^ =    ] =   |    = [ ^= ]'

# bad_comma s = ,(?! )

def checkScope(self):
    my_scopes = ["source.r.embedded.knitr", "source.r"]
    cursor = self.view.sel()[0].begin()
    curr_scope = self.view.scope_name(cursor).split(' ')
    scopy = list(set(my_scopes) & set(curr_scope))
    return (scopy)

def do_replace(self, edit, regex, rep):
    str_matches = self.view.find_all(regex)
    for b in reversed(str_matches):
        beg = sublime.Region.begin(b)
        synt = self.view.scope_name(beg).split()
        current_text = self.view.substr(b)
        print(current_text)
        if "source.r.embedded.knitr" in synt:
            self.view.replace(edit, b, rep)
        elif "source.r" in synt:
            self.view.replace(edit, b, rep)

def regex_replace1(self, edit, regex, rep):
    str_matches = self.view.find_all(regex)
    for b in reversed(str_matches):
        beg = sublime.Region.begin(b)
        synt = self.view.scope_name(beg).split()
        current_text = self.view.substr(b)
        new_text = re.sub(r'(?<=[\'], [\'])(.+?)[\']\s[\']', r"\1', '", current_text)
        if "source.r.embedded.knitr" in synt:
            self.view.replace(edit, b, new_text)
        elif "source.r" in synt:
            self.view.replace(edit, b, new_text)

def regex_replace2(self, edit, regex, rep):
    str_matches = self.view.find_all(regex)
    for b in reversed(str_matches):
        beg = sublime.Region.begin(b)
        synt = self.view.scope_name(beg).split()
        current_text = self.view.substr(b)
        print(current_text)
        new_text = re.sub(r'[\']\s[\'](.+?)', r"', '\1", current_text)
        if "source.r.embedded.knitr" in synt:
            self.view.replace(edit, b, new_text)
        elif "source.r" in synt:
            self.view.replace(edit, b, new_text)

def equals_replace(self, edit, regex, rep):
    str_matches = self.view.find_all(regex)
    sing_strings = self.view.find_by_selector('string.quoted.single.r')
    doub_strings = self.view.find_by_selector('string.quoted.double.r')
    stringys = sing_strings + doub_strings
    for b in reversed(str_matches):
        beg = sublime.Region.begin(b)
        synt = self.view.scope_name(beg).split()
        instr = [i.contains(beg) for i in stringys]
        if sum(instr)>0:
            return
        elif "source.r.embedded.knitr" in synt:
            self.view.replace(edit, b, rep)
        elif "source.r" in synt:
            self.view.replace(edit, b, rep)

class TrimTrailingWhiteSpaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        rscope = checkScope(self)
        if len(rscope)>0:
            equals_replace(self, edit, "((?<=[^= <>\!\?*])=(?=[^=<>\!*])|(?<=[^=<>\!\?*])=(?=[^= <>\!*]))", ' = ')
            do_replace(self, edit, "(?<!\{[0-9]),(?![ \"])", ', ')
            do_replace(self, edit, ";(?![ \'\"])", '; ')
            do_replace(self, edit, "\!=(?! )|(?<! )\!=", ' != ')
            do_replace(self, edit, "==(?! )|(?<! )==", ' == ')
            do_replace(self, edit, "(?<![ %-]|tr|td|table|th)>(?![ %=]|tr|td|table|th)", ' > ')
            do_replace(self, edit, "(?<! |tr|td|table|th)<(?![ \-=\/]|tr|td|table|th)", ' < ')
            do_replace(self, edit, "(?<=\S)  ", ' ')
            #do_replace(self, edit, "(?<!(= ))[\'\"]\s[\'\"]", '\', \'') # old missing comma code
            regex_replace1(self, edit, r"(?<=[\'\"], [\'\"]).+?[\'\"]\s[\'\"]", "\1', '") # new missing comma code
            regex_replace2(self, edit, r"[\'\"]\s[\'\"].+?(?=[\'\"], [\'\"])", "\1', '") # new missing comma code

                
                

class TrimTrailingWhiteSpace(sublime_plugin.EventListener):
     def on_pre_save(self, view):
         view.run_command("trim_trailing_white_space")

