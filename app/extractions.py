import io
import os
import random

import tempfile
from tempfile import NamedTemporaryFile

import textract

import fitz
from PIL import Image

import json

from pydub import AudioSegment
import wave
import shutil

import regex as re

FULL_BLOCK = '\u2588'

def do_extract_text(file, redaction):
    text_result = ''
    if file.name.split('.')[-1].lower() == 'mp3':
        sound = AudioSegment.from_mp3(file.name)
        tmp_wav = NamedTemporaryFile(suffix='.wav', buffering=0)
        sound.export(tmp_wav.name, format="wav")
        text_result = do_extract_from_wav(tmp_wav)
    elif file.name.split('.')[-1].lower() == 'wav':
        text_result = do_extract_from_wav(file)
    else :
        text = textract.process(file.name)
        text_result = text.decode('utf-8')
    if redaction:
        text_result = do_redaction(text_result, redaction)
    return text_result

def do_extract_pdf_images(file):
    file_list = []
    pdf_file = fitz.open(file)
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        for image_index, img in enumerate(page.get_images(), start=1):
            xref = img[0]
            image = pdf_file.extract_image(xref)
            image_bytes = image['image']
            image_ext = image['ext']
            with NamedTemporaryFile(delete=False, buffering=0) as image_file:
                image_file.write(image_bytes)
                file_list.append(image_file.name.replace("/", "$") + '.' + image_ext)
    return file_list

def do_extract_from_wav(wav_file):
    result_text = ''
    chunk_files = split_wav_file(wav_file.name)
    for chunk_file in chunk_files:
        text = textract.process(chunk_file)
        result_text = result_text + text.decode('utf-8') + ' '
        os.remove(chunk_file)
    return result_text

def split_wav_file(input_file_path):
    max_size_bytes = 5 * 1024 * 1024
    output_directory = tempfile.gettempdir()
    with wave.open(input_file_path, 'rb') as input_wav:
        sample_width = input_wav.getsampwidth()
        frame_rate = input_wav.getframerate()
        num_channels = input_wav.getnchannels()
        max_frames_per_split = max_size_bytes // (sample_width * num_channels)
        current_split_num = random.randint(0, max_size_bytes)
        current_frame_num = 0
        output_file_paths = []
        while True:
            frames_to_read = min(max_frames_per_split, input_wav.getnframes() - current_frame_num)
            frames = input_wav.readframes(frames_to_read)
            if not frames:
                break
            output_file_path = os.path.join(output_directory, f'split_{current_split_num}.wav')
            output_file_paths.append(output_file_path)
            with wave.open(output_file_path, 'wb') as output_wav:
                output_wav.setnchannels(num_channels)
                output_wav.setsampwidth(sample_width)
                output_wav.setframerate(frame_rate)
                output_wav.writeframes(frames)
            current_frame_num += frames_to_read
            current_split_num += random.randint(0, max_size_bytes)
    return output_file_paths

def do_redaction(text, redaction):
    redacted_text = text
    redaction_tag = json.loads(redaction)
    tag_id = list(redaction_tag)[0]
    phrases = redaction_tag[tag_id]
    for phrase in phrases:
        reasons = phrases[phrase]
        for reason in reasons:
            reason_num = reason
            reason_reason = reasons[reason]
        phrase_splits = phrase.split()
        redacted_text = redact_text(redacted_text, phrase_splits)    
    return redacted_text

def redact_text(text, phrases_to_redact):
    redacted_text = text
    for phrase in phrases_to_redact:
        redacted_text = redacted_text.replace(phrase, FULL_BLOCK * len(phrase))
    return redacted_text
