import sys
import os
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Configuraciones adicionales para pytest
import pytest
from unittest.mock import patch, MagicMock 