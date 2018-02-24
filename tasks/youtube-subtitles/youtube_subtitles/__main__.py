import sys

from youtube_subtitles.generation import generate_video


def main():
    if len(sys.argv) != 5:
        print('Usage: {} <text_input_path> <flag> <video_output_path> <subtitles_output_path>'
              .format(sys.argv[0]), file=sys.stderr)
    text_path, flag, video_path, subtitles_path = sys.argv[1:]
    generate_video(text_path, flag, video_path, subtitles_path)
    print('Successfully generated {} and {}'.format(video_path, subtitles_path))


if __name__ == '__main__':
    main()
