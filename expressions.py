tab = '    '

class NonTerminal:
    def yaml(self):
        ''':returned type str: A str YAML representation of the respective object'''
        raise NotImplementedError

    def messages(self):
        ''':returned type list(str): A YAML representation of the respective object splitted in lines.'''
        # The amount of tabs of each line will depend on the depth of the line.
        raise NotImplementedError

class SimpleValue(NonTerminal):
    def __init__(self, value):
        self._value = value

    def is_compose_value(self):
        return False

    def value(self):
        return self._value

    def yaml(self):
        return self._value

class String(SimpleValue):
    # It just exists due to the behaviour of a '-' at the beginning
    def __init__(self, value):
        value = value.replace('"', '');
        if len(value) and ('\\n' in value or '-' == value[0]):
            self._value = '"{}"'.format(value)
        else:
            self._value = '{}'.format(value)

    def value(self):
        return self._value

    def __eq__(self, string):
        return self._value == string.value()

    def __str__(self):
        return self._value

    def __hash__(self):
        return hash(self._value)
        

class ComposeValue(NonTerminal):
    # A value which derives in either an Object or an Array
    def __init__(self, value):
        self._messages = value.messages()

    def is_compose_value(self):
        return True
        
    def messages(self):
        return self._messages

    def yaml(self):
        _yaml = ''

        for line in self._messages:
            _yaml += '{}\n'.format(line) 

        return _yaml

class Element(NonTerminal):
    def __init__(self, value):
        if value.is_compose_value():
            # I should add the tab at the start of all the messages
            self._messages = ['-'] + list(map(lambda x: '{}{}'.format(tab, x), value.messages()))
        
        else:
            self._messages = ['- {}'.format(value.value())]

    def concat_element(self, element):
        self._messages += element.messages()

    def messages(self):
        return self._messages

class Array(NonTerminal):
    def __init__(self, element):
        self._element = element.messages()

    def messages(self):
        return self._element

    def value(self):
        return ComposeValue(self)

class Pair(NonTerminal):
    def __init__(self, string, value):
        self._key = string # needed to check unique keys

        if value.is_compose_value():
            self._messages = ['{}:'.format(string.value())] + list(map(lambda x: '{}{}'.format(tab, x), value.messages()))
        else:
            self._messages = ['{}: {}'.format(string.value(), value.value())]

    def messages(self):
        return self._messages

    def key(self):
        return self._key

class Member(NonTerminal): 
    def __init__(self, pair):
        self._keys = {pair.key()}
        self._messages = pair.messages()

    def concat_member(self, member):
        # Members are concatenated so in each time we have to check that the keys are unique

        if not self._keys.isdisjoint(member.keys()):
            repeted_keys = [str(key) for key in self._keys & member.keys()]
            raise Exception("Repeted keys {} on same JSON Object.".format(repeted_keys))

        self._keys |= member.keys()
        self._messages += member.messages()

    def messages(self):
        return self._messages

    def keys(self):
        return self._keys

class Object(NonTerminal):
    def __init__(self, members):
        self._members = members.messages()

    def messages(self):
        return self._members

    def value(self):
        return ComposeValue(self)

class EmptyObject(NonTerminal):
    def messages(self):
        return ['{}']
        
    def value(self):
        return SimpleValue('{}')

class EmptyArray(NonTerminal):
    def messages(self):
        return ['[]']
    def value(self):
        return SimpleValue('[]')
