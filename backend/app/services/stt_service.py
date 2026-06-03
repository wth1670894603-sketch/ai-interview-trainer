"""音声認識サービス — Whisper"""

import tempfile
import os
from pathlib import Path
from typing import Optional

from ..config import settings


class STTService:
    """音声→テキスト変換（faster-whisper）"""

    _model = None

    @classmethod
    def _get_model(cls):
        """Whisperモデルを遅延ロード"""
        if cls._model is None:
            try:
                from faster_whisper import WhisperModel

                model_size = settings.whisper_model_size
                # GPUが使える場合はGPU、なければCPU
                compute_type = "float16" if cls._has_gpu() else "int8"
                cls._model = WhisperModel(model_size, device="cuda" if cls._has_gpu() else "cpu",
                                          compute_type=compute_type)
            except ImportError:
                raise RuntimeError(
                    "faster-whisper がインストールされていません。"
                    "pip install faster-whisper を実行してください。"
                )
        return cls._model

    @staticmethod
    def _has_gpu() -> bool:
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    @classmethod
    async def transcribe(cls, audio_path: str, language: str = "ja") -> dict:
        """音声ファイルをテキストに変換"""
        model = cls._get_model()

        segments, info = model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        result = {
            "text": "",
            "segments": [],
            "language": info.language,
            "duration": info.duration,
        }

        full_text = []
        for seg in segments:
            full_text.append(seg.text)
            result["segments"].append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
            })

        result["text"] = "".join(full_text).strip()
        return result

    @staticmethod
    async def transcribe_fallback(text: str) -> dict:
        """Whisperなしのフォールバック（テキスト入力をそのまま）"""
        return {
            "text": text,
            "segments": [{"start": 0, "end": 0, "text": text}],
            "language": "ja",
            "duration": 0,
        }
