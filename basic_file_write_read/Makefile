PYTHON=python3
PROTOC=../bin/protoc.exe
PROTO_PATH=./proto/
PYTHON_PROTO_PATH=./python/proto/

# Find all proto files
FILES=$(shell find ./proto/ -type f -iname \*.proto)
# Replace path to proto files with path to python proto files
PYTHON_TMP=$(addprefix $(PYTHON_PROTO_PATH), $(notdir $(FILES)))
# Replace .proto with _pb2.py
PYTHON_OUT=$(PYTHON_TMP:%.proto=%_pb2.py)

python: $(PYTHON_OUT)
	@touch $(PYTHON_PROTO_PATH)__init__.py

$(PYTHON_PROTO_PATH)%_pb2.py : $(PROTO_PATH)%.proto
	@$(PROTOC) $< --python_out=$(PYTHON_PROTO_PATH) --proto_path=$(PROTO_PATH)

install:
	$(PYTHON) -m pip install -r requirements.txt

write:
	$(PYTHON) ./python/write_basic.py ./python/addressbookfile

read:
	$(PYTHON) ./python/read_basic.py ./python/addressbookfile

clean:
	rm -rf ./python/__pycache__
	rm -f ./python/addressbookfile

all: python

.DEFAULT_GOAL=all
.PHONY: install write read clean
