#
# SPDX-License-Identifier: Unlicense
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

from typing import List, Dict

# -----------------------------------------------------------------------------
# COPY CONFIG SCRIPT ARGUMENTS
# -----------------------------------------------------------------------------

# Directory with the files to be overwritten
dir_overwrite: str = "build-config-plugins"

# Name of the files to be overwritten
file_names_list: List[str] = ["settings.gradle.kts", "gradle.properties"]

# Dictionary with the needles for each file:
# needles_dict = { file_name: needle }
# A needle should be in ascii and should not be made with only whitespaces
needles_dict: Dict[str, str] = {}

# If the needle_dict doesn't have the needle for the file then use this one:
default_needle: str = "build-config-plugins-needle"

# Timeout in seconds for the prompt, -1 to be unlimited and 0 to allways cancel
timeout: int = 5
