import argparse, threading, os, urllib
from newspaper import Article


# [START tts_synthesize_text_file]
def synthesize_text_file(text_file, out_file):
    url = text_file

    article = Article(url)
    article.download()
    article.parse()

    out_dir = '/tmp/' + out_file
    os.mkdir(out_dir)
    threads = []
    for i in range(0, max(100000, len(article.text)), 3000):
        text = article.text[i:i+3000]
        sub_out_file = '%s/%d.mp3' % (out_dir, i)

        thread = threading.Thread(target=threaded_func, args=(text, sub_out_file))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    os.popen('cat %s/* > %s' % (out_dir, out_file)).read()

def threaded_func(text, out_file):
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=1.2)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open(out_file, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

# [END tts_synthesize_text_file]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--text',
                       help='The text file from which to synthesize speech.')
    parser.add_argument('--out',
                       help='The text file from which to synthesize speech.')

    args = parser.parse_args()

    synthesize_text_file(args.text, args.out)
