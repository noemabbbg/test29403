import os
import ffmpeg



input_folder = './Cyberpunk Edgerunners - AniLibria.TV [WEBRip 1080p HEVC]'
output_folder = './preobr'

# Создаем выходную папку, если она не существует
os.makedirs(output_folder, exist_ok=True)

# Проходим по всем файлам входной папки
for file_name in os.listdir(input_folder):
    if file_name.endswith('.mkv'):
        input_file = os.path.join(input_folder, file_name)
        output_file = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.mp4')

        # Преобразование формата с использованием ffmpeg
        ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)

print("Преобразование завершено.")
