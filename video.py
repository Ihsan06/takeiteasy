from moviepy.editor import *

def create_video_with_quote(quote, output_path):
    clip = TextClip(quote, fontsize=70, color='white', size=(720, 480))
    clip = clip.set_duration(10).set_position('center').set_bg_color('black')

    clip.write_videofile(output_path, fps=24)
