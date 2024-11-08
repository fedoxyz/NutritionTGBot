from telegram.ext import ContextTypes

def get_user_data(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data

def set_user_data(context: ContextTypes.DEFAULT_TYPE, key, value):
    context.user_data[key] = value

def get_current_state(context: ContextTypes.DEFAULT_TYPE):
    return get_user_data(context).get('state', 0)

def set_current_state(context: ContextTypes.DEFAULT_TYPE, state):
    set_user_data(context, 'state', state)
