#!/usr/bin/env python

import subprocess, re, sys

class MediaInfo:
    def __init__(self, **kwargs):
        if not kwargs['filename']:
            print("please assgin filename")
            sys.exit(1)

        self.filename = kwargs['filename']

        self.mediainfo()
        #self.general()
        #self.video()
        self.audio()

    def mediainfo(self):
        cmd = "mediainfo -f " + self.filename
        p = subprocess.check_output(cmd, shell=True)
        mediainfo = p.decode()
        self.mediainfo = mediainfo

    def general(self):
        gen = re.search("(^General\n.*?\n\n)", self.mediainfo, re.S)
        if gen is None:
            print("media file error")
            sys.exit(1)

        gen_info = gen.group(1)

        container_pattern = re.compile("Format\s*:\s*([\w\_\-\\\/\. ]+)\n")
        container = self.regex(container_pattern, gen_info)
        self.container = re.sub(r"\s+", "", container)

        length_pattern = re.compile("Duration\s*:\s*(\d+)\.?\d*\n")
        self.length = self.regex(length_pattern, gen_info)

        bitrate_pattern = re.compile("Overall bit rate\s*:\s*(\d+)\n")
        self.bitrate = self.regex(bitrate_pattern, gen_info)

        title_pattern = re.compile("Title\s*:\s*(.+)\n")
        self.title = self.regex(title_pattern, gen_info)

        album_pattern = re.compile("Album\s*:\s*(.+)\n")
        self.album = self.regex(album_pattern, gen_info)

        track_name_pattern = re.compile("Track name\s*:\s*(.+)\n")
        self.track_name = self.regex(track_name_pattern, gen_info)

        performer_pattern = re.compile("Performer\s*:\s*(.+)\n")
        self.performer = self.regex(performer_pattern, gen_info)

    def video(self):
        video = re.search("(Video[\s\#\d]*\n.*?\n\n)", self.mediainfo, re.S)
        if video is None:
            return

        video_info = video.group(1)

        video_codec_pattern = re.compile("Codec\s*:\s*([\w\_\-\\\/ ]+)\n")
        video_codec = self.regex(video_codec_pattern, video_info)

        video_format_pattern = re.compile("Format\s*:\s*([\w\_\-\\\/ ]+)\n")
        video_format = self.regex(video_format_pattern, video_info)

        video_format_profile_pattern = re.compile("Codec profile\s*:\s*([\w\_\-\\\/\@\. ]+)\n")
        video_format_profile = self.regex(video_format_profile_pattern, video_info)

        if video_codec:
            video_codec = re.sub(r"\s+", "", video_codec)

        if video_format:
            video_format = re.sub(r"\s+", "", video_format)

        if video_format_profile:
            video_format_profile = re.sub(r"\s+", "", video_format_profile)


        video_duration_pattern = re.compile("Duration\s*:\s*(\d+)\.?\d*\n")
        self.video_duration = self.regex(video_duration_pattern, video_info)

        video_bitrate_pattern = re.compile("Bit rate\s*:\s*(\d+)\n")
        self.video_bitrate = self.regex(video_bitrate_pattern, video_info)

        width_pattern = re.compile("Width\s*:\s*(\d+)\n")
        self.width = self.regex(width_pattern, video_info)

        height_pattern = re.compile("Height\s*:\s*(\d+)\n")
        self.height = self.regex(height_pattern, video_info)

        fps_pattern = re.compile("frame rate\s*:\s*([\d\.]+)\s*fps\n")
        self.fps = self.regex(fps_pattern, video_info)

        fps_mode_pattern = re.compile("Frame rate mode\s*:\s*([\w\.]+)\n")
        fps_mode = self.regex(fps_mode_pattern, video_info)

        dar_pattern = re.compile("Display aspect ratio\s*:\s*([\d\.]+)\n")
        dar = self.regex(dar_pattern, video_info)

        #frame_count = int( fps * video_duration / 1000)

        #if fps and video_duration and frame_count is None:
        #    fps = str(frame_count / video_duration * 1000)[:6]

        #$frame_count = int($fps * $video_length / 1000)

        #         if (    $fps and $video_length and (!$frame_count or $frame_count <= 0));
                      #$fps = substr($frame_count / $video_length * 1000, 0, 6)
        #   if ((!$fps or $fps <= 0) and $video_length and $frame_count);
        #                $video_length = substr($frame_count / $fps * 1000, 0, 6)
        #   if (    $fps and (!$video_length or $video_length <= 0) and $frame_count);
                     # $video_length = $length
        #   if (!$video_length and $length and $video_info);
                     # ($rotation) = $video_info =~ /Rotation\s*:\s*([\d\.]+)\n/i;
        # $rotation = 0 unless $rotation;

    def audio(self):
        audio = re.search("(Audio[\s\#\d]*\n.*?\n\n)", self.mediainfo, re.S)
        if audio is None:
            return

        audio_info = audio.group(1)
        print(audio_info)

        audio_codec_pattern = re.compile("Codec\s*:\s*([\w\_\-\\\/ ]+)\n")
        audio_codec = self.regex(audio_codec_pattern, audio_info)

        audio_format_pattern = re.compile("Format\s*:\s*([\w\_\-\\\/ ]+)\n")
        audio_format = self.regex(audio_format_pattern, audio_info)

        if audio_codec:
            self.audio_codec = re.sub(r"\s+", "", audio_codec)

        if audio_format:
            self.audio_format = re.sub(r"\s+", "", audio_format)

        audio_duration_pattern = re.compile("Duration\s*:\s*(\d+)\.?\d*\n")
        self.audio_duration = self.regex(audio_duration_pattern, audio_info)

        audio_bitrate_pattern = re.compile("Bit rate\s*:\s*(\d+)\n")
        self.audio_bitrate = self.regex(audio_bitrate_pattern, audio_info)

        audio_rate_pattern = re.compile("Sampling rate\s*:\s*(\d+)\n")
        self.audio_rate = self.regex(audio_rate_pattern, audio_info)

        audio_language_pattern = re.compile("Language\s*:\s*(\w+)\n")
        self.audio_language = self.regex(audio_language_pattern, audio_info)


        #$audio_length = $video_length
        #  if (    (!$audio_length or $audio_length <= 0)
        #      and $video_length
        #      and $audio_info);
        #($audio_language) = $audio_info =~ /Language\s*:\s*(\w+)\n/;

    def regex(self, pattern, string):
        result = re.search(pattern, string)
        if result is None:
            return None

        return result.group(1)


