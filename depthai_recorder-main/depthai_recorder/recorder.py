import logging
import multiprocessing as mp
import random
import string
import subprocess
import time
import pathlib
# set logging level debug
from typing import Optional


class Recorder:
    def __init__(self, output_path='out', camera_focus: Optional[int] = None, convert_to_mp4: bool = True):
        # Initialize video recording
        self.is_recording = False
        self.process = None
        self.start_event = None
        self.stop_event = None
        self.output_path = output_path
        self.camera_focus = camera_focus
        self.convert_to_mp4 = convert_to_mp4
        self.rec_id_queue = mp.Queue()
        self.init_video_recording()

    def init_video_recording(self):
        """Initialize video recording."""
        self.start_event = mp.Event()
        self.stop_event = mp.Event()

        # Set the target function for the subprocess
        target = self.run_subprocess

        # Create a separate process for running the subprocess
        process = mp.Process(target=target, args=(self.rec_id_queue, self.start_event, self.stop_event,
                                                  self.output_path, self.camera_focus, self.convert_to_mp4))
        # Store the process if needed for later use
        self.process = process

        # start the process
        process.start()
        # wait for the process to start
        time.sleep(3)

    def run_subprocess(self, rec_id_queue, start_event, stop_event, output_path, camera_focus, convert_to_mp4):
        """Subprocess target function."""
        import depthai as dai
        import os

        # Create DepthAI pipeline
        pipeline = dai.Pipeline()

        # Define sources and outputs
        cam_rgb = pipeline.create(dai.node.ColorCamera)
        cam_left = pipeline.create(dai.node.MonoCamera)
        cam_right = pipeline.create(dai.node.MonoCamera)

        # set the focus of the camera
        if camera_focus:
            cam_rgb.initialControl.setManualFocus(camera_focus)

        video_rgb = pipeline.create(dai.node.VideoEncoder)
        video_l = pipeline.create(dai.node.VideoEncoder)
        video_r = pipeline.create(dai.node.VideoEncoder)
        video_rgb_out = pipeline.create(dai.node.XLinkOut)
        video_l_out = pipeline.create(dai.node.XLinkOut)
        video_r_out = pipeline.create(dai.node.XLinkOut)

        video_rgb_out.setStreamName('video_rgb')
        video_l_out.setStreamName('video_l')
        video_r_out.setStreamName('video_r')

        # Set properties of camera and video encoder
        cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        cam_left.setBoardSocket(dai.CameraBoardSocket.LEFT)
        cam_right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        video_rgb.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H264_HIGH)
        video_r.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H264_HIGH)
        video_l.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H264_HIGH)

        # Link nodes together
        cam_rgb.video.link(video_rgb.input)
        cam_left.out.link(video_l.input)
        cam_right.out.link(video_r.input)

        video_rgb.bitstream.link(video_rgb_out.input)
        video_l.bitstream.link(video_l_out.input)
        video_r.bitstream.link(video_r_out.input)

        # Connect to DepthAI device and start pipeline
        with dai.Device(pipeline) as device:
            video_rgb_queue = device.getOutputQueue(name='video_rgb', maxSize=5, blocking=False)
            video_l_queue = device.getOutputQueue(name='video_l', maxSize=5, blocking=False)
            video_r_queue = device.getOutputQueue(name='video_r', maxSize=5, blocking=False)
            recording = False
            start_timestamp = None
            time_offset = None
            all_finalized = True

            # Define the queues as a dictionary
            queues = {
                'video_rgb': {'queue': video_rgb_queue, 'videoFile': None, 'fileName': 'color', 'finalized': True},
                'video_l': {'queue': video_l_queue, 'videoFile': None, 'fileName': 'left', 'finalized': True},
                'video_r': {'queue': video_r_queue, 'videoFile': None, 'fileName': 'right', 'finalized': True}
            }

            while True:
                if start_event.is_set():
                    if not recording:
                        logging.info("Starting recording")
                        recording = True
                        folder_name, start_timestamp = rec_id_queue.get()
                        # Create 'out' directory if it doesn't exist
                        os.makedirs(pathlib.Path(output_path, folder_name), exist_ok=True)
                        for stream in queues:
                            file_name = queues[stream]['fileName']
                            video_file = open(pathlib.Path(output_path, folder_name, f"{file_name}.mp4v", 'wb'))
                            queues[stream]['videoFile'] = video_file
                        logging.info(f'Started saving frames to {output_path}/{folder_name}')
                        logging.info(f'Start timestamp: {start_timestamp}')
                        dai_timestamp = dai.Clock.now().total_seconds()
                        time_offset = dai_timestamp - start_timestamp
                        frame_count = 0

                if stop_event.is_set():
                    if all_finalized:
                        logging.info("Stopping recording")
                        stop_event.clear()
                    end_timestamp = time.time()
                    logging.info("Received stop message")
                    recording = False
                    all_finalized = False
                    for stream in queues:
                        # set finalized to False, to allow the last frames to be saved
                        queues[stream]['finalized'] = False
                    start_event.clear()

                # Retrieve and save video frames if saving is enabled
                if recording or not all_finalized:
                    for stream in queues:
                        queue = queues[stream]['queue']
                        video_file = queues[stream]['videoFile']
                        finalized = queues[stream]['finalized']
                        file_name = queues[stream]['fileName']

                        if queue.has():
                            video_frame = queue.get()
                            logging.info(f'Got frame {video_frame.getSequenceNum()}')
                            data = video_frame.getData()

                            # Check frame timestamp
                            timestamp = video_frame.getTimestamp()
                            # Check if it's older than the start timestamp
                            logging.info(
                                f' for videoFile {file_name} Frame timestamp: {timestamp.total_seconds()} Offsetted '
                                f'timestamp: {timestamp.total_seconds() - time_offset} startTimestamp: '
                                f'{start_timestamp}')
                            if timestamp.total_seconds() - time_offset < start_timestamp:
                                logging.info("Skipping frame")
                                continue
                            if video_file is not None:
                                if not finalized:
                                    if timestamp.total_seconds() - time_offset > end_timestamp:
                                        logging.info(f"Finalizing stream{stream}")
                                        queues[stream]['finalized'] = True
                                        # if all queues are finalized, finalize the video
                                        if all(queues[stream]['finalized'] for stream in queues):
                                            all_finalized = True
                                        video_file.close()
                                        logging.info("Stopped saving frames")
                                        if convert_to_mp4:
                                            logging.info("Converting to mp4")
                                            input = pathlib.Path(output_path, folder_name, f"{file_name}.mp4v")
                                            output = pathlib.Path(output_path, folder_name, f"{file_name}.mp4")
                                            subprocess.run(
                                                ['ffmpeg', '-framerate', '30', '-i',
                                                 input, '-c', 'copy', output])
                                        if all_finalized:
                                            logging.info("All queues finalized, stopping")
                                            break
                                        continue

                            video_file.write(data)
                            logging.info('Wrote frame ')
                            frame_count += 1
                time.sleep(0.01)

    def start_video_recording(self, rec_id=None):
        if not rec_id:
            rec_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not self.is_recording:
            logging.info(f"Starting: {rec_id}")
            self.rec_id_queue.put((rec_id, time.time()))
            self.is_recording = True
            self.start_event.set()

    def stop_video_recording(self):
        if self.is_recording:
            logging.info(f"Stopping")
            self.is_recording = False
            self.stop_event.set()


if __name__ == '__main__':
    # Example usage
    recorder = Recorder(convert_to_mp4=True, camera_focus=50)  # Initialize the Recorder instance
    time.sleep(5)
    recorder.start_video_recording()  # Start video recording
    time.sleep(5)  # Recording for 10 seconds
    recorder.stop_video_recording()  # Stop video recording
    time.sleep(1)
    recorder.start_video_recording()  # Start video recording
    time.sleep(5)  # Recording for 10 seconds
    recorder.stop_video_recording()  # Stop video recording
    time.sleep(5)

    time.sleep(10)
    recorder.process.terminate()  # Terminate the subprocess
    recorder.process.join()  # Wait for the subprocess to finish
