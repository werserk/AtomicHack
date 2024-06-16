import logging
import time

import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from app.web.utils import get_processor

logger = logging.getLogger(__name__)


class VideoCallback:
    def __init__(self):
        self.processor = get_processor()

    def __call__(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        start_time = time.time()
        predictions = self.processor(image)
        logger.info(f"Processed image in {time.time() - start_time:.2f} seconds")
        annotated_image = self.processor.annotate_image(image, predictions)
        return av.VideoFrame.from_ndarray(annotated_image, format="bgr24")


def capture_video_page():
    st.header("Съёмка видео")
    st.markdown(
        "Используйте камеру для захвата видео. Видео будет обработано в реальном времени."
    )

    video_frame_callback = VideoCallback()

    ctx = webrtc_streamer(
        key="defect-detection",
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=False,
        mode=WebRtcMode.SENDRECV,
    )
