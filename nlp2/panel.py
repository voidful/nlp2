import inspect
import json


class Panel:
    def __init__(self):
        self.element_list = []
        self.key_list = []
        self.result_dict = {}

    def add_element(self, k, v, msg, default):
        if isinstance(v, list):
            inputted = ''
            while inputted not in [str(e) for e in v]:
                def_msg = ", [default=" + str(default) + "]: " if not isinstance(default, list) else " :"
                inputted = input(msg + ", input an item in the list " + str(v) + def_msg)
                if inputted == '':
                    inputted = str(default)
            if v == [True, False] or (v[0].lower == 'true' or v[0].lower == 'false'):
                inputted = json.loads(str(inputted).lower())
            self.element_list.append(inputted)
        else:
            if isinstance(v, float) and 0 < v < 1:  # probability
                inputed = input(msg + " (between 0-1), [default=" + str(default) + "]: ")
                invalue = float(inputed) if inputed and len(inputed.strip()) > 0 else v
            elif isinstance(v, float):  # number
                inputed = input(msg + " (float), [default=" + str(default) + "]: ")
                invalue = float(inputed) if inputed and len(inputed.strip()) > 0 else v
            elif isinstance(v, int):  # number
                inputed = input(msg + " (number), [default=" + str(default) + "]: ")
                invalue = int(inputed) if inputed and len(inputed.strip()) > 0 else v
            else:
                invalue = input(msg + ", [default=" + str(default) + "]: ")
            self.element_list.append(invalue)
        self.key_list.append(k)

    def get_result_dict(self):
        result_dict = dict(zip(self.key_list, self.element_list))
        return {k: v for k, v in result_dict.items() if
                v is not None and len(str(v)) > 0}  # only return non empty result


def function_get_all_arg(func):
    funt_args = []
    if len(inspect.getfullargspec(func).args) > 0:
        funt_args.extend(inspect.getfullargspec(func).args)
    if len(inspect.getfullargspec(func).kwonlyargs) > 0:
        funt_args.extend(inspect.getfullargspec(func).kwonlyargs)
    return funt_args

def function_get_all_arg_with_value(func):
    if len(inspect.getfullargspec(func).args) > 0:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        arg_w_def = dict(zip(inspect.getfullargspec(func).args[arg_len - def_len:],
                             inspect.getfullargspec(func).defaults))
        return arg_w_def
    else:
        return {}


def function_check_wrong_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in input_arg if arg not in all_arg]


def function_check_missing_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in all_arg if arg not in input_arg and arg != 'self']


def function_sep_suit_arg(func, input_arg):
    suit_arg = input_arg.copy()
    oth_arg = input_arg.copy()
    all_arg = function_get_all_arg(func)
    for k, v in list(suit_arg.items()):
        if k not in all_arg:
            suit_arg.pop(k)
        else:
            oth_arg.pop(k)
    return suit_arg, oth_arg


def function_argument_panel(func, inputted_arg={}, disable_input_panel=False, ignore_empty=False,
                            func_parent=None, show_func_name=False):
    """use inquirer panel to let user input function parameter or just use default value"""
    fname = func.__name__
    if len(inspect.getfullargspec(func).args) > 0 and inspect.getfullargspec(func).defaults is not None:
        def_arg = function_get_all_arg_with_value(func)
        function_def_arg = {**def_arg, **inputted_arg}
        # panel
        panel = Panel()
        for k, v in def_arg.items():
            if v is not None and (not isinstance(v, str) or len(v) > 0 or not ignore_empty):
                msg = fname + " " + k if show_func_name else k
                default_v = v
                if callable(v):
                    v = v(func_parent) if func_parent else v()
                    function_def_arg[k] = v[0]  # set default value
                    default_v = v[0]
                elif isinstance(v, bool):
                    v = [True, False]
                if not disable_input_panel:
                    panel.add_element(k, v, msg, default_v)

        if not disable_input_panel:
            function_def_arg.update(panel.get_result_dict())
        return function_def_arg
    else:
        return inputted_arg
