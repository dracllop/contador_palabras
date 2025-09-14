"""
Pruebas unitarias para la clase InterfazUsuario
"""
import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from contador import InterfazUsuario


class TestInterfazUsuario:
    """Clase de pruebas para InterfazUsuario"""
    
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.interfaz = InterfazUsuario()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Limpieza después de cada prueba"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _crear_archivo_prueba(self, nombre, contenido):
        """Método auxiliar para crear archivos de prueba"""
        ruta = os.path.join(self.temp_dir, nombre)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return ruta
    
    @pytest.mark.unit
    def test_mostrar_bienvenida(self, capsys):
        """Prueba mostrar mensaje de bienvenida"""
        self.interfaz.mostrar_bienvenida()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "archivos de texto (.txt)" in output
        assert "Ejemplos de rutas válidas:" in output
        assert "salir" in output or "quit" in output
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='archivo.txt')
    def test_solicitar_ruta_archivo(self, mock_input):
        """Prueba solicitar ruta de archivo al usuario"""
        ruta = self.interfaz.solicitar_ruta_archivo()
        
        assert ruta == 'archivo.txt'
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='s')
    def test_validar_extension_archivo_txt(self, mock_input):
        """Prueba validación de extensión .txt"""
        resultado = self.interfaz.validar_extension_archivo('archivo.txt')
        
        assert resultado is True
        mock_input.assert_not_called()  # No debería preguntar si es .txt
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='s')
    def test_validar_extension_archivo_no_txt_aceptar(self, mock_input):
        """Prueba validación de extensión no .txt aceptando continuar"""
        resultado = self.interfaz.validar_extension_archivo('archivo.pdf')
        
        assert resultado is True
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='n')
    def test_validar_extension_archivo_no_txt_rechazar(self, mock_input):
        """Prueba validación de extensión no .txt rechazando continuar"""
        resultado = self.interfaz.validar_extension_archivo('archivo.pdf')
        
        assert resultado is False
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='si')
    def test_validar_extension_archivo_respuestas_variadas(self, mock_input):
        """Prueba validación con diferentes respuestas afirmativas"""
        resultado = self.interfaz.validar_extension_archivo('archivo.pdf')
        
        assert resultado is True
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    def test_procesar_archivo_exitoso(self, capsys):
        """Prueba procesamiento exitoso de archivo"""
        contenido = "Hola mundo prueba"
        archivo = self._crear_archivo_prueba("test.txt", contenido)
        
        resultado = self.interfaz.procesar_archivo(archivo)
        
        assert resultado is True
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 3" in output
    
    @pytest.mark.unit
    def test_procesar_archivo_inexistente(self, capsys):
        """Prueba procesamiento de archivo inexistente"""
        archivo_inexistente = os.path.join(self.temp_dir, "no_existe.txt")
        
        resultado = self.interfaz.procesar_archivo(archivo_inexistente)
        
        assert resultado is False
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "No se encontró" in output
    
    @pytest.mark.unit
    def test_procesar_archivo_carpeta(self, capsys):
        """Prueba procesamiento de carpeta en lugar de archivo"""
        resultado = self.interfaz.procesar_archivo(self.temp_dir)
        
        assert resultado is False
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "es una carpeta, no un archivo" in output
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='n')
    def test_procesar_archivo_extension_no_txt_rechazar(self, mock_input, capsys):
        """Prueba procesamiento de archivo sin extensión .txt rechazando"""
        contenido = "contenido"
        archivo = self._crear_archivo_prueba("test.pdf", contenido)
        
        resultado = self.interfaz.procesar_archivo(archivo)
        
        assert resultado is False
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='s')
    def test_procesar_archivo_extension_no_txt_aceptar(self, mock_input, capsys):
        """Prueba procesamiento de archivo sin extensión .txt aceptando"""
        contenido = "Hola mundo"
        archivo = self._crear_archivo_prueba("test.pdf", contenido)
        
        resultado = self.interfaz.procesar_archivo(archivo)
        
        assert resultado is True
        mock_input.assert_called_once()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Archivo procesado exitosamente" in output
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='s')
    def test_preguntar_continuar_si(self, mock_input):
        """Prueba pregunta de continuar con respuesta afirmativa"""
        resultado = self.interfaz.preguntar_continuar()
        
        assert resultado is True
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='n')
    def test_preguntar_continuar_no(self, mock_input):
        """Prueba pregunta de continuar con respuesta negativa"""
        resultado = self.interfaz.preguntar_continuar()
        
        assert resultado is False
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    @patch('builtins.input', return_value='si')
    def test_preguntar_continuar_respuestas_variadas(self, mock_input):
        """Prueba pregunta de continuar con diferentes respuestas afirmativas"""
        resultado = self.interfaz.preguntar_continuar()
        
        assert resultado is True
        mock_input.assert_called_once()
    
    @pytest.mark.unit
    def test_mostrar_despedida(self, capsys):
        """Prueba mostrar mensaje de despedida"""
        self.interfaz.mostrar_despedida()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Gracias por usar el contador de palabras" in output
    
    @pytest.mark.unit
    def test_inicializacion_interfaz(self):
        """Prueba inicialización de la interfaz de usuario"""
        interfaz = InterfazUsuario()
        
        assert interfaz.validador is not None
        assert interfaz.contador is not None
        assert hasattr(interfaz.validador, 'validar_ruta_archivo')
        assert hasattr(interfaz.contador, 'procesar_archivo')
    
    @pytest.mark.unit
    def test_procesar_archivo_vacio(self, capsys):
        """Prueba procesamiento de archivo vacío"""
        archivo = self._crear_archivo_prueba("vacio.txt", "")
        
        resultado = self.interfaz.procesar_archivo(archivo)
        
        assert resultado is True
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 0" in output
        assert "El archivo está vacío" in output
