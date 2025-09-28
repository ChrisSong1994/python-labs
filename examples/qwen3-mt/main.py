import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["API_KEY"]

print("API_KEY",API_KEY)
print("环境变量加载成功，启动应用...")

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=API_KEY,  # 请确保已设置环境变量，或直接填入你的 API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 支持的语言选项
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "English",
    "Chinese": "Chinese",
    "Traditional Chinese": "Traditional Chinese",
    "Russian": "Russian",
    "Japanese": "Japanese",
    "Korean": "Korean",
    "Spanish": "Spanish",
    "French": "French",
    "Portuguese": "Portuguese",
    "German": "German",
    "Italian": "Italian",
    "Thai": "Thai",
    "Vietnamese": "Vietnamese",
    "Indonesian": "Indonesian",
    "Malay": "Malay",
    "Arabic": "Arabic",
    "Hindi": "Hindi",
    "Hebrew": "Hebrew",
    "Burmese": "Burmese",
    "Tamil": "Tamil",
    "Urdu": "Urdu",
    "Bengali": "Bengali",
    "Polish": "Polish",
    "Dutch": "Dutch",
    "Romanian": "Romanian",
    "Turkish": "Turkish",
    "Khmer": "Khmer",
    "Lao": "Lao",
    "Cantonese": "Cantonese",
    "Czech": "Czech",
    "Greek": "Greek",
    "Swedish": "Swedish",
    "Hungarian": "Hungarian",
    "Danish": "Danish",
    "Finnish": "Finnish",
    "Ukrainian": "Ukrainian",
    "Bulgarian": "Bulgarian",
    "Serbian": "Serbian",
    "Telugu": "Telugu",
    "Afrikaans": "Afrikaans",
    "Armenian": "Armenian",
    "Assamese": "Assamese",
    "Asturian": "Asturian",
    "Basque": "Basque",
    "Belarusian": "Belarusian",
    "Bosnian": "Bosnian",
    "Catalan": "Catalan",
    "Cebuano": "Cebuano",
    "Croatian": "Croatian",
    "Egyptian Arabic": "Egyptian Arabic",
    "Estonian": "Estonian",
    "Galician": "Galician",
    "Georgian": "Georgian",
    "Gujarati": "Gujarati",
    "Icelandic": "Icelandic",
    "Javanese": "Javanese",
    "Kannada": "Kannada",
    "Kazakh": "Kazakh",
    "Latvian": "Latvian",
    "Lithuanian": "Lithuanian",
    "Luxembourgish": "Luxembourgish",
    "Macedonian": "Macedonian",
    "Maithili": "Maithili",
    "Maltese": "Maltese",
    "Marathi": "Marathi",
    "Mesopotamian Arabic": "Mesopotamian Arabic",
    "Moroccan Arabic": "Moroccan Arabic",
    "Najdi Arabic": "Najdi Arabic",
    "Nepali": "Nepali",
    "North Azerbaijani": "North Azerbaijani",
    "North Levantine Arabic": "North Levantine Arabic",
    "Northern Uzbek": "Northern Uzbek",
    "Norwegian Bokmål": "Norwegian Bokmål",
    "Norwegian Nynorsk": "Norwegian Nynorsk",
    "Occitan": "Occitan",
    "Odia": "Odia",
    "Pangasinan": "Pangasinan",
    "Sicilian": "Sicilian",
    "Sindhi": "Sindhi",
    "Sinhala": "Sinhala",
    "Slovak": "Slovak",
    "Slovenian": "Slovenian",
    "South Levantine Arabic": "South Levantine Arabic",
    "Swahili": "Swahili",
    "Tagalog": "Tagalog",
    "Ta’izzi-Adeni Arabic": "Ta’izzi-Adeni Arabic",
    "Tosk Albanian": "Tosk Albanian",
    "Tunisian Arabic": "Tunisian Arabic",
    "Venetian": "Venetian",
    "Waray": "Waray",
    "Welsh": "Welsh",
    "Western Persian": "Western Persian",
}


def translate_text(text, source_lang, target_lang):
    """
    调用阿里云百炼的翻译模型进行翻译
    """
    if not text.strip():
        return "请输入要翻译的文本"

    # 构造消息内容
    messages = [{"role": "user", "content": text}]

    # 构造翻译选项
    translation_options = {
        "source_lang": LANGUAGES.get(source_lang, "auto"),
        "target_lang": LANGUAGES.get(target_lang, "English"),
    }

    try:
        # 调用模型
        completion = client.chat.completions.create(
            model="qwen-mt-turbo",
            messages=messages,
            stream=True,
            max_tokens=2048,
            extra_body={"translation_options": translation_options},
        )
        response = ""
        for chunk in completion:
            response = chunk.choices[0].delta.content
            yield response
    except Exception as e:
        print(f"翻译出错: {str(e)}")
        yield f"翻译出错: {str(e)}"


# 创建 Gradio 界面
with gr.Blocks(title="Qwen3-MT Translator") as demo:
    gr.Markdown("# 🌍 Qwen3-MT Translator")
    gr.Markdown(
        'A real-time translation tool based on the Qwen3-MT model<br><a href="https://www.alibabacloud.com/help/en/model-studio/translation-abilities" target="_blank">Learn more about Qwen3-MT and API documentation</a>',
        elem_id="desc",
    )
    gr.Image(
        value="https://modelscope.oss-cn-beijing.aliyuncs.com/resource/Qwen3-MT.png",
        label="Qwen3-MT Supported Languages",
        show_label=False,
        show_download_button=False,
        interactive=False,
        height=60,
    )

    with gr.Row():
        with gr.Column():
            source_text = gr.Textbox(
                label="Input Text",
                placeholder="Please enter the text to translate...",
                lines=5,
            )
            with gr.Row():
                source_lang = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    value="Auto Detect",
                    label="Source Language",
                )
                target_lang = gr.Dropdown(
                    choices=list(LANGUAGES.keys())[1:],  # Exclude "Auto Detect"
                    value="English",
                    label="Target Language",
                )
            translate_btn = gr.Button("Translate", variant="primary")

        with gr.Column():
            target_text = gr.Textbox(
                label="Translation Result", interactive=False, lines=5
            )

    # 示例
    gr.Examples(
        examples=[
            ["你好，世界！", "Chinese", "English"],
            ["Hello, how are you today?", "English", "Chinese"],
            ["私は学生です。", "Japanese", "Chinese"],
            ["Bonjour, comment allez-vous?", "French", "English"],
        ],
        inputs=[source_text, source_lang, target_lang],
        outputs=target_text,
        fn=translate_text,
        cache_examples=True,
    )

    # 按钮点击事件
    translate_btn.click(
        fn=translate_text,
        inputs=[source_text, source_lang, target_lang],
        outputs=target_text,
    )

    # 支持回车键翻译
    source_text.submit(
        fn=translate_text,
        inputs=[source_text, source_lang, target_lang],
        outputs=target_text,
    )

# 启动应用
if __name__ == "__main__":
    demo.launch()
