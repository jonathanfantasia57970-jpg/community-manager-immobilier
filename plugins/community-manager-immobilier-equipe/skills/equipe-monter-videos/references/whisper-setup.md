# Local Whisper transcription

Use Faster-Whisper, which runs the Whisper model locally on CPU. It is already supported by `caption.py` and `silence.py`; do not replace their transcription implementation or use a paid API.

## Install or restore

Use the same Python interpreter for installation and the skill scripts. In the managed Work runtime, the main Python installation is read-only and the user site is enabled. Install the tested dependency set into the user site:

```bash
python3 -m pip install --user -r <skill-dir>/references/whisper-requirements.txt
```

This recipe was tested on Linux with Python 3.12. On another environment, check whether the user site is enabled; use its documented writable environment or a virtual environment instead of trying to modify a read-only runtime. If using a virtual environment, run the skill scripts with that environment's Python.

Keep `av==15.1.0` with Faster-Whisper 1.2.1. PyAV 19.0.2 installed successfully but failed at transcription with `open() got an unexpected keyword argument 'metadata_errors'`; version 15.1.0 passed the end-to-end test. `socksio` supplies the dependency needed by the runtime's configured SOCKS proxy; preserve the existing proxy configuration.

## Download and verify the model

Load the multilingual model once with the installed Python:

```python
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=2)
assert model.model.is_multilingual
```

The first run downloads public model files from the model publisher's Hugging Face repository `Systran/faster-whisper-base` (about 150 MB). Later runs can use the cache without a connection. Do not request a paid API key. If the download is blocked, report that the package is installed but the model is not ready. Packages and model caches can disappear after an execution environment reset; restore them as needed rather than promising permanent installation.

## Use and verify

For known French speech:

```bash
python3 <skill-dir>/scripts/caption.py input.mp4 --transcribe --engine faster-whisper --model base --language fr -o captioned.mp4 --json-brief
```

For another known language use its actual code; omit `--language` to let the multilingual engine detect it. Do not translate unless requested. Larger multilingual models can be selected when accuracy justifies their extra download, memory and computation.

Verify the generated SRT against the audio and check caption rendering using `look.py`. Check cue timing and pronunciation-dependent names; automatic transcription is not a guarantee of correct wording or exact word boundaries.

## Installation evidence

On 2026-10-26 the `base` multilingual model loaded on CPU with INT8. An offline end-to-end test passed through the unmodified skill `caption.py`: synthetic English speech -> Faster-Whisper transcript -> SRT -> H.264/AAC video. The recognized words matched the supplied test sentence and the rendered captions were inspected. This validates integration; French accuracy on real user footage still needs review per video.

Primary project: https://github.com/SYSTRAN/faster-whisper
