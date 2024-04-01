from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router

from .event_handler import add_event, edit_event, delete_event, list_events

from ..utils.permissions import is_admin

admin_router = Router()

class EventCreationState(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
    LINK = State()
    PHOTO_ID = State()
    STATUS = State()
    DATE = State()
    TO_CREATED = State()

class AdminMenuButtons:
    ADD_EVENT = 'Add Event'
    EDIT_EVENT = 'Edit Event'
    DELETE_EVENT = 'Delete Event'
    LIST_EVENTS = 'List Events'

async def admin_menu(message: types.Message):
    if is_admin(message.from_user):
        custom_keyboard = [
            [KeyboardButton(text=AdminMenuButtons.ADD_EVENT)],
            [KeyboardButton(text=AdminMenuButtons.EDIT_EVENT)],
            [KeyboardButton(text=AdminMenuButtons.DELETE_EVENT)],
            [KeyboardButton(text=AdminMenuButtons.LIST_EVENTS)]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True)
        await message.answer("Admin Menu:", reply_markup=reply_markup)
    else:
        await message.answer("You are not authorized to access this menu.")

@admin_router.message(AdminMenuButtons.ADD_EVENT)
async def handle_add_event(message: types.Message, state: FSMContext):
    await add_event(message, state)

@admin_router.message(AdminMenuButtons.EDIT_EVENT)
async def handle_edit_event(message: types.Message, state: FSMContext):
    await edit_event(message, state)

@admin_router.message(AdminMenuButtons.DELETE_EVENT)
async def handle_delete_event(message: types.Message, state: FSMContext):
    await delete_event(message, state)

@admin_router.message(AdminMenuButtons.LIST_EVENTS)
async def handle_list_events(message: types.Message):
    await list_events(message)

