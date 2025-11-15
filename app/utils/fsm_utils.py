from typing import Dict, Optional, Callable, List
import asyncio

from aiogram.fsm.context import FSMContext


def make_update_progress(loop, state: FSMContext) -> Callable:
    """Возвращает функцию для отслеживания прогресса скачивания.

    Args:
        loop (_type_): цикл событий
        state (FSMContext): состояние В FSM для обновление прогресса
    """

    def update_progress(gen_description: bool = None) -> True:
        data: Dict = asyncio.run_coroutine_threadsafe(state.get_data(), loop).result()

        asyncio.run_coroutine_threadsafe(
            state.update_data(counter_progress=data.get("counter_progress", 0) + 1),
            loop,
        ).result()
        # Дополнительная опция для необходимого состояния
        if gen_description:
            asyncio.run_coroutine_threadsafe(
                state.update_data(gen_description=gen_description),
                loop,
            ).result()

        return True

    return update_progress


def make_cancel_chek(loop, state: FSMContext):
    """Возвращает функцию для отмены скачивания.

    Args:
        loop (_type_): цикл событий
        state (FSMContext): состояние В FSM для обновление прогресса
    """

    def cancell_chek():
        data: Dict = asyncio.run_coroutine_threadsafe(state.get_data(), loop).result()
        return data.get("cancel", None)

    return cancell_chek


def chek_cancel(
    cancel_chek: Callable,
    selenium_driver=None,
) -> Optional[List]:
    """Функция для проверки состояния отмены.

    Args:
        selenium_driver (_type_): веб драйвер для selenium
        cancel_chek (_type_): функция для проверки отмена скачивания

    Returns:
        _type_: Возвращает либо пустой список либо None
    """
    if cancel_chek():
        if selenium_driver:
            selenium_driver.quit()
        return []
