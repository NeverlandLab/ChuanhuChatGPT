import re
import gradio as gr

from typing import Dict, List, Tuple
from gradio_client import utils as client_utils
from gradio import utils


class Chatbot:
    def setup_ui(self):
        gr.Chatbot.postprocess = self.postprocess

    def postprocess_chat_messages(
        self, chat_message: str | tuple | list | None, role: str
    ) -> str | dict | None:
        if chat_message is None:
            return None
        else:
            if isinstance(chat_message, (tuple, list)):
                if len(chat_message) > 0 and "text" in chat_message[0]:
                    chat_message = chat_message[0]["text"]
                else:
                    file_uri = chat_message[0]
                    if utils.validate_url(file_uri):
                        filepath = file_uri
                    else:
                        filepath = self.make_temp_copy_if_needed(file_uri)

                    mime_type = client_utils.get_mimetype(filepath)
                    return {
                        "name": filepath,
                        "mime_type": mime_type,
                        "alt_text": chat_message[1] if len(chat_message) > 1 else None,
                        "data": None,  # These last two fields are filled in by the frontend
                        "is_file": True,
                    }
            if isinstance(chat_message, str):
                if role == "bot":
                    chat_message = self.convert_bot_before_marked(chat_message)
                elif role == "user":
                    chat_message = self.convert_user_before_marked(chat_message)
                return chat_message
            else:
                raise ValueError(
                    f"Invalid message for Chatbot component: {chat_message}"
                )

    def convert_bot_before_marked(self, chat_message):
        """
        注意不能给输出加缩进, 否则会被marked解析成代码块
        """
        if '<div class="md-message">' in chat_message:
            return chat_message
        else:
            raw = f'<div class="raw-message hideM">{self.clip_rawtext(chat_message)}</div>'

            code_block_pattern = re.compile(r"```(.*?)(?:```|$)", re.DOTALL)
            code_blocks = code_block_pattern.findall(chat_message)
            non_code_parts = code_block_pattern.split(chat_message)[::2]
            result = []
            for non_code, code in zip(non_code_parts, code_blocks + [""]):
                if non_code.strip():
                    result.append(non_code)
                if code.strip():
                    code = f"\n```{code}\n```"
                    result.append(code)
            result = "".join(result)
            md = f'<div class="md-message">\n\n{result}\n</div>'
            return raw + md

    def clip_rawtext(self, chat_message, need_escape=True):
        # first, clip hr line
        hr_pattern = r'\n\n<hr class="append-display no-in-raw" />(.*?)'
        hr_match = re.search(hr_pattern, chat_message, re.DOTALL)
        message_clipped = chat_message[: hr_match.start()] if hr_match else chat_message
        # second, avoid agent-prefix being escaped
        agent_prefix_pattern = r"(<!-- S O PREFIX -->.*?<!-- E O PREFIX -->)"
        # agent_matches = re.findall(agent_prefix_pattern, message_clipped)
        agent_parts = re.split(agent_prefix_pattern, message_clipped, flags=re.DOTALL)
        final_message = ""
        for i, part in enumerate(agent_parts):
            if i % 2 == 0:
                if part != "" and part != "\n":
                    final_message += (
                        f'<pre class="fake-pre">{self.escape_markdown(part)}</pre>'
                        if need_escape
                        else f'<pre class="fake-pre">{part}</pre>'
                    )
            else:
                part = part.replace(' data-fancybox="gallery"', "")
                final_message += part
        return final_message

    def convert_user_before_marked(self, chat_message):
        if '<div class="user-message">' in chat_message:
            return chat_message
        else:
            return (
                f'<div class="user-message">{self.escape_markdown(chat_message)}</div>'
            )

    def escape_markdown(self, text):
        """
        Escape Markdown special characters to HTML-safe equivalents.
        """
        escape_chars = {
            # ' ': '&nbsp;',
            "_": "&#95;",
            "*": "&#42;",
            "[": "&#91;",
            "]": "&#93;",
            "(": "&#40;",
            ")": "&#41;",
            "{": "&#123;",
            "}": "&#125;",
            "#": "&#35;",
            "+": "&#43;",
            "-": "&#45;",
            ".": "&#46;",
            "!": "&#33;",
            "`": "&#96;",
            ">": "&#62;",
            "<": "&#60;",
            "|": "&#124;",
            "$": "&#36;",
            ":": "&#58;",
            "\n": "<br>",
        }
        text = text.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")
        return "".join(escape_chars.get(c, c) for c in text)

    def postprocess(
        self,
        y: List[List[str | Tuple[str] | Tuple[str, str] | None] | Tuple],
    ) -> List[List[str | Dict | None]]:
        if y is None:
            return []
        processed_messages = []
        for message_pair in y:
            assert isinstance(
                message_pair, (tuple, list)
            ), f"Expected a list of lists or list of tuples. Received: {message_pair}"
            assert (
                len(message_pair) == 2
            ), f"Expected a list of lists of length 2 or list of tuples of length 2. Received: {message_pair}"

            processed_messages.append(
                [
                    self.postprocess_chat_messages(message_pair[0], "user"),
                    self.postprocess_chat_messages(message_pair[1], "bot"),
                ]
            )
        return processed_messages
