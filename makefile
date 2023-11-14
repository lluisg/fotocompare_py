PYTHON = python
PIP = pip
VENV_DIR = envfotocomp

# ------- prepare the virtual enviroment --------
venv-prepare: venv-creates venv-requirements

venv-create:
	$(PYTHON) -m venv $(VENV_DIR)

venv-requirements:
	$(PIP) install -r requirements.txt


ORIGINAL_FOLDER_PATH = 
IMGS_PATH_DICT = 'paths_images.json'
RESIZED_FOLDER = 
SIGNATURE_DICT = 'signatures_images.json'
RESULTS_LSH = 'results_images_lsh.json'
RESULTS_HISTOGRAM = 'results_images_histogram.json'
RESULTS_MSE = 'results_images_mse.json'
THRESHOLD_LSH = 0.6
HASH_SIZE_LSH = 16
THRESHOLD_HISTO = 0.90
THRESHOLD_MSE = 0

# ------- steps of the program (ordered)  --------
get-imgs-paths:
	$(PYTHON) prepare_imgs_paths.py -i $(ORIGINAL_FOLDER_PATH) -o $(IMGS_PATH_DICT)

resize-imgs:
	$(PYTHON) resize_images.py -i $(ORIGINAL_FOLDER_PATH) -d $(IMGS_PATH_DICT) -o $(RESIZED_FOLDER) -r 800

prepare-lsh:
	$(PYTHON) prepare_lsh.py -i $(IMGS_PATH_DICT) -o $(RESULTS_LSH) -s $(HASH_SIZE_LSH) -t $(THRESHOLD_LSH) -a "aux_lsh_results.json"

prepare-histo:
	$(PYTHON) prepare_methods.py -i $(IMGS_PATH_DICT) -o $(RESULTS_HISTOGRAM) -l $(RESULTS_LSH) -t $(THRESHOLD_HISTO) -m histogram  -a "aux_histo_results.json"

prepare-name:
	$(PYTHON) prepare_methods.py -i $(IMGS_PATH_DICT) -o $(RESULTS_HISTOGRAM) -l $(RESULTS_LSH) -m name  -a "aux_name_results.json"

prepare-mse:
	$(PYTHON) prepare_methods.py -i $(IMGS_PATH_DICT) -o $(RESULTS_MSE) -l $(RESULTS_LSH) -t $(THRESHOLD_MSE) -m mse  -a "aux_mse_results.json"

separate-folders-lsh:
	$(PYTHON) separate_into_folders.py -i $(RESULTS_LSH)

separate-folders-histo:
	$(PYTHON) separate_into_folders.py -i $(RESULTS_HISTOGRAM)

separate-folders-mse:
	$(PYTHON) separate_into_folders.py -i $(RESULTS_MSE)


all-steps-lsh: get-imgs-paths resize-imgs prepare-lsh prepare-name separate-folders-lsh

all-steps-histo: get-imgs-paths resize-imgs prepare-lsh prepare-histo separate-folders-histo

all-steps-mse: get-imgs-paths resize-imgs prepare-lsh prepare-mse
