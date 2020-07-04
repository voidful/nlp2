import inspect
import inquirer


def function_get_all_arg(func):
    if len(inspect.getfullargspec(func).args) > 0:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        return inspect.getfullargspec(func).args[arg_len - def_len:]
    else:
        return []


def function_check_wrong_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in input_arg if arg not in all_arg]


def function_check_missing_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in all_arg if arg not in input_arg]


def function_argument_panel(func, inputted_arg={}, disable_input_panel=False, func_parent=None,
                            show_func_name=False):
    """use inquirer panel to let user input function parameter or just use default value"""
    fname = func.__name__
    if len(inspect.getfullargspec(func).args) > 0 and 'defaults' in inspect.getfullargspec(func):
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        arg_w_def = zip(inspect.getfullargspec(func).args[arg_len - def_len:],
                        inspect.getfullargspec(func).defaults)
        # merge two dict
        def_arg = dict(arg_w_def)
        function_def_arg = {**def_arg, **inputted_arg}
        if not disable_input_panel:
            inquirer_list = []
            for k, v in def_arg.items():
                if v is not None:
                    msg = fname + " " + k if show_func_name else k
                    if callable(v):
                        inquirer_list.append(inquirer.List(k, message=msg, choices=v(func_parent)))
                    elif isinstance(v, list):
                        inquirer_list.append(inquirer.List(k, message=msg, choices=v))
                    elif isinstance(v, bool):
                        inquirer_list.append(inquirer.List(k, message=msg, choices=[True, False]))
                    else:
                        if isinstance(v, float) and 0 < v < 1:  # probability
                            msg += " (between 0-1)"
                        elif isinstance(v, float) or isinstance(v, int):  # number
                            msg += " (number)"
                        inquirer_list.append(inquirer.Text(k, message=msg, default=v))
            predict_parameter = inquirer.prompt(inquirer_list)
            function_def_arg.update(predict_parameter)
        return function_def_arg
    else:
        return inputted_arg
