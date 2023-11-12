PYTHON = python
PIP = pip
VENV_DIR = envfotocomp

# ------- prepare the virtual enviroment --------
venv-prepare: venv-create venv-activate venv-requirements

venv-create:
	$(PYTHON) -m venv $(VENV_DIR)

venv-requirements:
	$(PIP) install -r requirements.txt


ORIGINAL_FOLDER_PATH = "C:\Users\Lluis\Pictures"
IMGS_PATH_DICT = 'paths_images.json'
RESIZED_FOLDER = "C:\Users\Lluis\Desktop\Projects\fotocompare_py\Pictures_resized"
SIGNATURE_DICT = 'signatures_images.json'
RESULTS_LSH = 'results_images_lsh.json'
RESULTS_HISTOGRAM = 'results_images_histogram.json'
THRESHOLD_LSH = 0.6
THRESHOLD_HISTO = 0.75
HASH_SIZE_LSH = 16

IMGS_PATH_DICT_FOTOS = 'paths_images_fotos.json'
ORIGINAL_FOLDER_PATH_FOTOS = "C:\Users\Lluis\Desktop\Projects\fotocompare_py\fotos"
RESIZED_FOLDER_FOTOS = "C:\Users\Lluis\Desktop\Projects\fotocompare_py\fotos_resized"
SIGNATURE_DICT_FOTOS = 'signatures_images_fotos.json'
RESULTS_LSH_FOTOS = 'results_images_lsh_fotos.json'
RESULTS_HISTOGRAM_FOTOS = 'results_images_histogram_fotos.json'

# ------- steps of the program (ordered)  --------
get-imgs-paths:
	$(PYTHON) prepare_imgs_paths.py -i $(ORIGINAL_FOLDER_PATH) -o $(IMGS_PATH_DICT)
# $(PYTHON) prepare_imgs_paths.py -i $(ORIGINAL_FOLDER_PATH_FOTOS) -o $(IMGS_PATH_DICT_FOTOS)

resize-imgs:
	$(PYTHON) resize_images.py -i $(ORIGINAL_FOLDER_PATH) -d $(IMGS_PATH_DICT) -o $(RESIZED_FOLDER) -r 800
# $(PYTHON) resize_images.py -i $(ORIGINAL_FOLDER_PATH_FOTOS) -d $(IMGS_PATH_DICT_FOTOS) -o $(RESIZED_FOLDER_FOTOS) -r 800

prepare-lsh:
	$(PYTHON) prepare_lsh.py -i $(IMGS_PATH_DICT) -o $(RESULTS_LSH) -s $(HASH_SIZE_LSH) -t $(THRESHOLD_LSH)
# $(PYTHON) prepare_lsh.py -i $(IMGS_PATH_DICT_FOTOS) -o $(RESULTS_LSH_FOTOS) -s $(HASH_SIZE_LSH) -t $(THRESHOLD_LSH)

prepare-histo:
	$(PYTHON) prepare_histogram.py -i $(IMGS_PATH_DICT) -o $(RESULTS_HISTOGRAM) -l $(RESULTS_LSH) -t $(THRESHOLD_HISTO)
# $(PYTHON) prepare_histogram.py -i $(IMGS_PATH_DICT_FOTOS) -o $(RESULTS_HISTOGRAM_FOTOS) -l $(RESULTS_LSH_FOTOS) -t $(THRESHOLD_HISTO)
# $(PYTHON) prepare_histogram.py -i $(IMGS_PATH_DICT) -o $(RESULTS_HISTOGRAM) -t $(THRESHOLD_HISTO)
# $(PYTHON) prepare_histogram.py -i $(IMGS_PATH_DICT_FOTOS) -o $(RESULTS_HISTOGRAM_FOTOS) -t $(THRESHOLD_HISTO)

separate-folders:
# $(PYTHON) separate_into_folders.py -i $(RESULTS_LSH)
	$(PYTHON) separate_into_folders.py -i $(RESULTS_LSH_FOTOS)

all-steps: get-imgs-paths resize-imgs prepare-lsh separate-folders
