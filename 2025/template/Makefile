CC = gcc
CFLAGS = -Wall -Wextra -std=c11
# LDFLAGS = 

INCLUDE_DIRS = library
OBJ_DIR = .build

MAIN_SRC = main.c
LIB_SRC = $(wildcard library/*.c)
SOURCES = $(MAIN_SRC) $(LIB_SRC)

OBJECTS = $(MAIN_SRC:%.c=$(OBJ_DIR)/%.o) \
		  $(LIB_SRC:%.c=$(OBJ_DIR)/%.o)

TARGET = main

all: $(TARGET)
	echo $(SOURCES)
	echo $(OBJECTS)

# Link object files to create the main target
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET) $(LDFL AGS)

# | $(OBJ_DIR) means that this target is a prerequisite,
# but it won't be rebuilt if it already exists.
# $< is equal to the first prerequisite, in this case main.c.
# $@ is equal to the target.
$(OBJ_DIR)/main.o: main.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -I $(INCLUDE_DIRS) -c $< -o $@

$(OBJ_DIR)/library/%.o: library/%.c | $(OBJ_DIR)/library
	$(CC) $(CFLAGS) -I $(INCLUDE_DIRS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(OBJ_DIR)/library:
	mkdir -p $(OBJ_DIR)/library

clean:
	rm -rf $(OBJ_DIR) $(TARGET)

rebuild:
	clean all

show:
	@echo "Sources " $(SOURCES)
	@echo "Objects " $(OBJECTS)

.PHONY:
	all clean rebuild show
