import cv2
import os
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

class SmartMediaComposer:
    
    def __init__(self, input_video_path):
        self.input_video_path = input_video_path
        self.video_clips = []

    def scene_recognition(self):
        # Using OpenCV to segment scenes based on scene change detection
        video_capture = cv2.VideoCapture(self.input_video_path)
        success, prev_frame = video_capture.read()
        index = 0

        while success:
            success, curr_frame = video_capture.read()
            if not success:
                break
            # Convert to grayscale
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            # Compute the difference
            diff = cv2.absdiff(curr_gray, prev_gray)
            non_zero_count = np.count_nonzero(diff)

            if non_zero_count > 100000: # Threshold for scene change
                print(f"Scene change detected at frame {index}")
                self.video_clips.append(index)

            prev_frame = curr_frame
            index += 1
        
        video_capture.release()

    def create_clips(self):
        # Use MoviePy to extract clips from detected scene changes
        video = VideoFileClip(self.input_video_path)
        scene_start = 0  # Start time for the first scene
        for scene_end in self.video_clips:
            clip = video.subclip(scene_start / video.fps, scene_end / video.fps)
            self.video_clips.append(clip)
            scene_start = scene_end

    def apply_transitions(self):
        # Placeholder for transition application between clips
        edited_clips = []
        for i, clip in enumerate(self.video_clips[:-1]):
            transition = clip.crossfadeout(1)  # 1-second fade-out
            edited_clips.append(transition)
            edited_clips.append(self.video_clips[i+1].crossfadein(1))  # 1-second fade-in
        return concatenate_videoclips(edited_clips, method="compose")

    def edit_video(self):
        self.scene_recognition()
        self.create_clips()
        final_video = self.apply_transitions()
        final_video.write_videofile("edited_video.mp4")

if __name__ == "__main__":
    composer = SmartMediaComposer("input_video.mp4")
    composer.edit_video()
