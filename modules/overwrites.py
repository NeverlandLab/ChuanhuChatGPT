from __future__ import annotations
from loguru import logger

from typing import List, Tuple
from gradio_client import utils as client_utils
from gradio import utils
import inspect

from modules.presets import *
from modules.index_func import *



def add_classes_to_gradio_component(comp):
    """
    this adds gradio-* to the component for css styling (ie gradio-button to gr.Button), as well as some others
    code from stable-diffusion-webui <AUTOMATIC1111/stable-diffusion-webui>
    """

    comp.elem_classes = [f"gradio-{comp.get_block_name()}", *(comp.elem_classes or [])]

    if getattr(comp, 'multiselect', False):
        comp.elem_classes.append('multiselect')


def IOComponent_init(self, *args, **kwargs):
    res = original_IOComponent_init(self, *args, **kwargs)
    add_classes_to_gradio_component(self)

    return res

original_IOComponent_init = gr.components.IOComponent.__init__
gr.components.IOComponent.__init__ = IOComponent_init


def BlockContext_init(self, *args, **kwargs):
    res = original_BlockContext_init(self, *args, **kwargs)
    add_classes_to_gradio_component(self)

    return res

original_BlockContext_init = gr.blocks.BlockContext.__init__
gr.blocks.BlockContext.__init__ = BlockContext_init
