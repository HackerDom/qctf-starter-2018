from datetime import timedelta
import os
import shutil
import tempfile
import re
import random
import wave

import srt

from youtube_subtitles.voice import create_recording


SENTENCE_RE = re.compile(r'([^.!?\r\n]+(?:\r?\n[^.!?\r\n]+)*[.!?\r\n]+)\s*', re.MULTILINE)
FFMPEG_COMMAND_TEMPLATE = \
    'ffmpeg -y -f concat -safe 0 -i {tracklist_path} -filter_complex' \
    ' "[0:a]asplit=3[out1][a][b]; [a]showwaves=s=1280x120[waves];' \
    ' [b]showspectrum=s=1280x600[spectrum]; [waves][spectrum] vstack[out0]"' \
    ' -map "[out0]" -map "[out1]" -c:v libx264 -c:a aac {video_path}'


def parse_sentences(text):
    sentences = SENTENCE_RE.findall(text)
    return [sentence.replace('\n', ' ') for sentence in sentences]


def get_sentences_with_flag(text_path, flag):
    with open(text_path, encoding='utf-8') as f:
        sentences = parse_sentences(f.read())
    flag_sentence = 'If you were wondering, the flag is {}.'.format(flag)
    random_index = random.randint(
        3 * len(sentences) // 8,
        5 * len(sentences) // 8)
    random_index = min(max(random_index, 0), len(sentences) - 1)
    sentences.insert(random_index, flag_sentence)
    return sentences


def generate_recordings(tempdir, sentences):
    recording_paths = []
    recording_durations = []
    for i, sentence in enumerate(sentences):
        path = os.path.join(tempdir, '{}.wav'.format(i))
        create_recording(path, sentence)
        recording_paths.append(path)
        with wave.open(path) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            recording_durations.append(frames / rate)
    return recording_paths, recording_durations


def save_tracklist(recording_paths, tracklist_path):
    tracklist = '\n'.join(
        'file \'{}\''.format(path)
        for path in recording_paths)
    with open(tracklist_path, 'w', encoding='utf-8') as f:
        f.write(tracklist)


def generate_subtitles(sentences, durations_in_seconds):
    subtitles = []
    start = timedelta(seconds=0)
    for i, (sentence, duration) in enumerate(zip(sentences, durations_in_seconds)):
        end = start + timedelta(seconds=duration)
        subtitles.append(srt.Subtitle(index=i + 1, start=start, end=end, content=sentence))
        start = end
    return subtitles


def save_subtitles(filename, subtitles):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))


def generate_video(text_path, flag, video_path, subtitles_path):
    sentences = get_sentences_with_flag(text_path, flag)

    tempdir = tempfile.mkdtemp()
    try:
        recording_paths, recording_durations = generate_recordings(tempdir, sentences)
        tracklist_path = os.path.join(tempdir, 'tracklist.txt')
        save_tracklist(recording_paths, tracklist_path)

        subtitles = generate_subtitles(sentences, recording_durations)
        save_subtitles(subtitles_path, subtitles)

        return_code = os.system(FFMPEG_COMMAND_TEMPLATE.format(
            tracklist_path=tracklist_path, video_path=video_path))
        if return_code:
            os.remove(subtitles_path)
            raise ValueError('Video generation failed with return code {}'
                             .format(return_code))
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)
