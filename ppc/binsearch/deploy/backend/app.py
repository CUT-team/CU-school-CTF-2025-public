import base64
import io
import os
import platform
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, jsonify, session, render_template_string, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

FLAG = os.environ.get("FLAG")
MAX_ROUNDS = 100
NUMBER_RANGE = 100
MAX_ATTEMPTS = 15

analogs_bolshe = [
    "больше", "превышает", "выше", "превосходит", "более",
    "значительнее", "сильнее", "крупнее", "многочисленнее", "превыше",
    "свыше", "обильнее", "масштабнее", "объемнее", "длиннее",
    "шире", "тяжелее", "весомее", "numerous", "larger",
    "greater", "bigger", "more than", "exceeds", "surpasses",
    "tops", "outweighs", "outnumbers", "superior to", "in excess of",
    "over", "above", "beyond", "additional to", "extra to",
    "overruns", "beats", "outdoes", "outperforms", "outstrips",
    "outranks", "transcends", "dominates", "dwarfs", "overshadows",
    "eclipses", "superior compared to", "higher than", "steeper than", "loftier than",
    "heavier than", "weightier than", "bulkier than", "größer als", "plus grand que",
    "mayor que", "maior que", "più grande di", "větší než", "større end",
    "groter dan", "μεγαλύτερο από", "większy niż", "больший чем", "大于",
    "より大きい", "보다 크다", "أكبر من", "גדול יותר", "बड़ा है",
    "перевешивает", "преобладает над", "доминирует над", "превалирует над", "опережает",
    "возвышается над", "превосходит по значению", "выигрывает у", "обгоняет", "затмевает",
    "усиливает", "intensifies", "magnifies", "amplifies", "augments",
    "возрастает над", "усугубляет", "увеличивает по сравнению с", "расширяет против", "множит относительно",
    "мощнее", "обширнее", "пространнее", "растянутее", "массивнее",
    "громоздче", "тучнее", "полнее", "габаритнее", "внушительнее"
]

noto_jp = [ "大于", "より大きい", "小于", "より小さい"]

noto_kr = ["보다 크다", "보다 작다"]

cjk_fonts = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Light.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Thin.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-DemiLight.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
]

noto_ar = ["أكبر من", "أصغر من"]

ar_fonts = [
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabicUI-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabicUI-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabicUI-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabicUI-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoKufiArabic-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabicUI-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-CondensedMedium.ttf"
]

noto_heb = ["גדול יותר", "קטן יותר"]

heb_fonts = [
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoRashiHebrew-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansHebrew-SemiCondensedBlack.ttf"
]

noto_dev = ["बड़ा है", "छोटा है"]

dev_fonts = [
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-ExtraCondensedBlack.ttf"
]

noto_other = ["μικρότερο από"]

noto_fonts = [
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedExtraLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ThinItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedThinItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedExtraBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-LightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedExtraLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedMediumItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedThinItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedExtraLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedExtraBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Thin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedBlackItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedSemiBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedMediumItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBlackItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedSemiBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBlackItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedMediumItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBlack.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedThin.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedSemiBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedSemiBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-MediumItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedLightItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Condensed.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedExtraLight.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedThinItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Light.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-CondensedExtraBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiBoldItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedMedium.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-BlackItalic.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedItalic.ttf"
]

analogs_menshe = [
    "меньше", "уступает", "ниже", "не достигает", "менее",
    "незначительнее", "слабее", "мельче", "малочисленнее", "ниже",
    "снизу", "скуднее", "компактнее", "теснее", "короче",
    "уже", "легче", "невесомее", "smaller", "lesser",
    "tinier", "less than", "falls below", "inferior to", "not as high as",
    "doesn't reach", "underruns", "understeps", "subordinate to", "deficient to",
    "under", "below", "beneath", "short of", "insufficient to",
    "underperforms", "trails", "lags behind", "ne dostigaet", "doesn't dostigaet",
    "ranks below", "falls short of", "yields to", "shrinks beside", "fades against",
    "diminishes against", "inferior compared to", "lower than", "flatter than", "shallower than",
    "lighter than", "slimmer than", "thinner than", "kleiner als", "plus petit que",
    "menor que", "menor que", "più piccolo di", "menší než", "mindre end",
    "kleiner dan", "μικρότερο από", "mniejszy niż", "меньший чем", "小于",
    "より小さい", "보다 작다", "أصغر من", "קטן יותר", "छोटा है",
    "проигрывает", "уступает", "подчиняется", "уменьшается перед", "отстает от",
    "не дотягивает до", "проваливается перед", "не выдерживает сравнения с", "тускнеет рядом с", "отступает перед",
    "сокращается", "diminishes", "reduces", "contracts", "decreases",
    "убывает по сравнению с", "ослабевает напротив", "умаляется против", "сжимается в сравнении с",
    "делится относительно",
    "слабее", "миниатюрнее", "тоньше", "изящнее", "деликатнее",
    "стройнее", "мягче", "неполнее", "скромнее", "невзрачнее"
]


def generate_text_image(text):
    bg_color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while sum(abs(c1 - c2) for c1, c2 in zip(bg_color, text_color)) < 200:
        text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img_width = 400
    img_height = 100

    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_paths = []
        system = platform.system()
        font_size = random.randint(12, 24)

        if system == "Linux":
            output = subprocess.check_output(["fc-list", ":", "file"]).decode('utf-8', 'ignore')
            font_paths = [line.strip()[:-1] for line in output.split('\n') if line.strip()]
        elif system == "Darwin":
            for font_dir in ['/Library/Fonts', '/System/Library/Fonts', str(Path.home() / 'Library' / 'Fonts')]:
                if os.path.exists(font_dir):
                    for file in os.listdir(font_dir):
                        if file.lower().endswith(('.ttf', '.otf')):
                            font_paths.append(os.path.join(font_dir, file))
        random.shuffle(font_paths)
        for font_path in font_paths:
            try:
                if "Noto" in font_path:
                    continue
                font = ImageFont.truetype(font_path, font_size)
                break
            except IOError:
                continue

    except Exception:
        font = ImageFont.load_default()

    if text in noto_jp or text in noto_kr:
        font = ImageFont.truetype(random.choice(cjk_fonts), font_size)

    if text in noto_ar:
        font = ImageFont.truetype(random.choice(ar_fonts), font_size)

    if text in noto_heb:
        font = ImageFont.truetype(random.choice(heb_fonts), font_size)

    if text in noto_dev:
        font = ImageFont.truetype(random.choice(dev_fonts), font_size)

    if text in noto_other:
        font = ImageFont.truetype(random.choice(noto_fonts), font_size)

    if hasattr(draw, 'textsize'):
        text_width, text_height = draw.textsize(text, font=font)
    else:
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = 200, 30
    max_x = max(0, img_width - text_width * 2)
    max_y = max(0, img_height - text_height * 2)

    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    draw.text((x, y), text, fill=text_color, font=font)

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"

INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Guess Challenge</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        .button:hover {
            background-color: #45a049;
        }
        .message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .message.info {
            background-color: #d9edf7;
            color: #31708f;
        }
        .message.success {
            background-color: #dff0d8;
            color: #3c763d;
        }
        .message.error {
            background-color: #f2dede;
            color: #a94442;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 4px;
        }
        form {
            margin-top: 20px;
        }
        input[type="number"] {
            padding: 8px;
            margin-right: 10px;
            width: 100px;
        }
        .progress {
            margin-top: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        .hint-image {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Guess Challenge</h1>

        {% if error %}
        <div class="message error">{{ error }}</div>
        {% endif %}

        {% if message %}
        <div class="message info">{{ message }}</div>
        {% endif %}

        {% if success %}
        <div class="message success">{{ success }}</div>
        {% endif %}

        <div>
            <h2>Правила:</h2>
            <p>1. Компьютер загадывает число от 0 до 100.</p>
            <p>2. Вы должны угадать это число, делая предположения.</p>
            <p>3. После каждого предположения вы получите подсказку.</p>
            <p>4. Цель - угадать 100 чисел.</p>
        </div>

        {% if 'current_round' in session %}
        <div class="progress">
            <h3>Прогресс:</h3>
            <p>Текущий раунд: {{ session['current_round'] }} из {{ MAX_ROUNDS }}</p>
            <p>Пройдено раундов: {{ session['rounds_completed'] }}</p>
            <p>Попыток в текущем раунде: {{ session['attempts'] }}</p>
        </div>

        <form action="{{ url_for('make_guess') }}" method="post">
            <h3>Угадайте число:</h3>
            <input type="number" name="guess" min="0" max="{{ NUMBER_RANGE }}" required>
            <input type="submit" value="Отправить предположение" class="button">
        </form>
        {% else %}
        <form action="{{ url_for('start_game') }}" method="post">
            <input type="submit" value="Начать игру" class="button">
        </form>
        {% endif %}
        
        {% if hint %}
        <div class="message info">
            <h3>Результат:</h3>
            <p>Ваше предположение: {{ last_guess }}</p>
            <p>Подсказка: 
                {% if hint == 'correct' %}
                <strong>Верно!</strong>
                {% else %}
                Загаданное число 
                <br>
                <img src="{{ hint_image }}" alt="Подсказка" class="hint-image">
                {% endif %}
            </p>
        </div>
        {% endif %}
        
        {% if flag %}
        <div class="message success">
            <h3>Поздравляем! Вы выиграли!</h3>
            <p>Ваш флаг: <strong>{{ flag }}</strong></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    context = {
        'MAX_ROUNDS': MAX_ROUNDS,
        'NUMBER_RANGE': NUMBER_RANGE,
        'message': request.args.get('message'),
        'error': request.args.get('error'),
        'success': request.args.get('success'),
        'hint': session.get('hint'),
        'hint_image': session.get('hint_image'),
        'last_guess': session.get('last_guess'),
        'flag': session.get('flag')
    }
    return render_template_string(INDEX_TEMPLATE, **context)


@app.route('/start', methods=['POST'])
def start_game():
    session.clear()
    session['current_round'] = 1
    session['target_number'] = random.randint(0, NUMBER_RANGE)
    session['attempts'] = 0
    session['rounds_completed'] = 0

    message = f'Игра началась! Раунд 1 из {MAX_ROUNDS}. Угадайте число от 0 до {NUMBER_RANGE}.'
    return redirect(url_for('index', message=message))


@app.route('/guess', methods=['POST'])
def make_guess():
    if 'current_round' not in session:
        return redirect(url_for('index', error='Сначала начните игру!'))

    try:
        guess = int(request.form.get('guess', 0))
    except ValueError:
        return redirect(url_for('index', error='Введите корректное число!'))

    if guess < 0 or guess > NUMBER_RANGE:
        return redirect(url_for('index', error=f'Число должно быть в диапазоне от 0 до {NUMBER_RANGE}'))

    session['attempts'] += 1
    session['last_guess'] = guess

    if session['attempts'] > MAX_ATTEMPTS:
        session.clear()
        return redirect(url_for('index', error=f'Вы исчерпали {MAX_ATTEMPTS} попыток!'))

    if guess < session['target_number']:
        hint_text = random.choice(analogs_bolshe)
        session['hint'] = hint_text
        session['hint_image'] = generate_text_image(hint_text)
    elif guess > session['target_number']:
        hint_text = random.choice(analogs_menshe)
        session['hint'] = hint_text
        session['hint_image'] = generate_text_image(hint_text)
    else:
        session['hint'] = 'correct'
        session['rounds_completed'] += 1

        if session['rounds_completed'] >= MAX_ROUNDS:
            session['flag'] = FLAG
            return redirect(url_for('index', success=f'Поздравляем! Вы прошли все {MAX_ROUNDS} раундов!'))
        else:
            message = f'Верно! Переходим к раунду {session["current_round"] + 1}!'
            session['current_round'] += 1
            session['target_number'] = random.randint(0, NUMBER_RANGE)
            session['attempts'] = 0
            return redirect(url_for('index', message=message))

    return redirect(url_for('index'))


@app.route('/status', methods=['GET'])
def status():
    if 'current_round' not in session:
        return jsonify({'status': 'Игра не начата'}), 200

    return jsonify({
        'round': session['current_round'],
        'attempts': session['attempts'],
        'rounds_completed': session['rounds_completed'],
        'max_rounds': MAX_ROUNDS
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
