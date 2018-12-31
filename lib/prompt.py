""" A Prompt is a way to get inputs from the user and make outputs, with more features such as input validation. """
import sys
import collections
import re

ITERABLES = [list, set, tuple, frozenset]

def split_by_newline(string, strip):
    strings = []
    for split_string in re.split(r"\n", string):
        if strip:
            split_string = split_string.strip()
        strings.append(split_string)
    return strings

def it(*li):
    # returns a func that itself returns each element of li each time it is called, in order, one each time
    def gen_func():
        for el in li:
            yield el
    gen = gen_func()
    def it_func(*args, **kwargs): # both of which are purposefully ignored
        return next(gen)
    return it_func

def prepare_new_validator(new_validator):
    if isinstance(new_validator, list):
        list_of_valid_inputs = new_validator
        def validator(val):
            if not val in list_of_valid_inputs:
                raise ValueError
        return validator
    elif isinstance(new_validator, collections.Callable):
        return new_validator
    else:
        raise TypeError('validator should be a list or callable')

class Prompt:
    def __init__(self, strip=True, request_type=str, validator=lambda x: True, tries=99, converter=None, input_prefix='', output_prefix='', warn_prefix=''):
        # init
        self.strip = strip
        self.request_type = request_type
        self.validator = prepare_new_validator(validator)
        self.tries = tries
        self.converter = converter
        self.input_prefix = input_prefix
        self.output_prefix = output_prefix
        self.warn_prefix = warn_prefix

    def _exit_converter(self, in_str):
        s = in_str.lower()
        return s in ['exit', 'quit']

    def _bool_converter(self, in_str):
        s = in_str.lower()
        if s in ['y', 'yes', '1', 'true']:
            return True
        elif s in ['n', 'no', '0', 'false']:
            return False
        else:
            return in_str

    def _iterable_converter(self, in_str, request_type, strip):
        if in_str:
            strings = split_by_newline(in_str, strip)
        else: # empty string
            strings = ''
        return request_type(strings)

    def _generic_class_converter(self, in_var, request_type):
        try:
            return request_type(in_var)
        except:
            return in_var

    def _converter(self, in_str, request_type, strip):
        # strip whitespace
        if strip:
            in_str = in_str.strip()
        # convert
        dic = {
            bool: self._bool_converter,
        }
        if request_type in dic.keys():
            return dic[request_type](in_str)
        elif request_type in ITERABLES:
            return self._iterable_converter(in_str, request_type, strip)
        else:
            return self._generic_class_converter(in_str, request_type)

    def warn(self, string):
        string_pretty = '{}{}'.format(self.warn_prefix, string)
        print(string_pretty)

    def output(self, string):
        string_pretty = '{}{}'.format(self.output_prefix, string)
        print(string_pretty)

    def input(self, string='Enter user input.', strip=None, request_type=None, validator=None, tries=None, converter=None, default='', password=False, options=None):
        # set defaults (self can't be in above thing)
        if strip is None:
            strip = self.strip
        if request_type is None:
            request_type = self.request_type
        if validator is None:
            validator = self.validator
        else:
            validator = prepare_new_validator(validator)
        if tries is None:
            tries = self.tries
        if converter is None:
            converter = self.converter

        # signal for if input was good or not:
        proceed = 0
        # prompt the user for some input
        for _ in range(tries):
            self.output(string)
            # get user input
            is_multiline = request_type in ITERABLES
            if is_multiline:
                print('Hit ENTER after each entry.  Hit ESC then ENTER when finished.')
            in_str = input(self.input_prefix)
            # see if we should quit
            if self._exit_converter(in_str):
                print("exiting")
                break
            # the next few steps are in a TRY block...
            try:
                # convert input and check type
                converted_input = self._converter(in_str, request_type, strip)
                if not isinstance(converted_input, request_type):
                    self.warn('Invalid input: your input is not of type "{}"'.format(request_type))
                    continue
                # run user inputted converter if there is one
                if converter is not None:
                    converted_input = converter(converted_input)
                # validate
                validator(converted_input)
            except Exception as error_message:
                self.warn('Invalid input: {}'.format(error_message))
                continue
            # if we got this far, then everything is good
            proceed = 1
            break
        if not proceed:
            raise Exception('Too many bad inputs.')
        return converted_input

