# pitch-please

Application to generate product pitches with AI

## Usage

1. Install dependencies for Python:

```
pip install -r requirements.txt
```

2. Add your OpenAI API key to `src/config.yaml` and update the product description and vibes.

3. Run `make_slides.py` modules:

```
python3 src/make_slides.py -c src/config.yaml
```

4. View results for your run in `results` subdirectory.