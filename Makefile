DEVELOPMENT_TARGET=~/Documents/gamecube/ttyd-mod-pack
RAW_ROM_FOLDER=raw_rom

all: build

build:
	mkdir -p ${DEVELOPMENT_TARGET}
	cp -a ${RAW_ROM_FOLDER}/* ${DEVELOPMENT_TARGET}

clean:
	rm -rf ${DEVELOPMENT_TARGET}

rebuild: clean build