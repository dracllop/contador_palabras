"""
Pruebas de integración para la clase Aplicacion
"""
import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from contador import Aplicacion


class TestAplicacion:
    """Clase de pruebas para Aplicacion"""
    
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.app = Aplicacion()
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
    
    @pytest.mark.integration
    def test_inicializacion_aplicacion(self):
        """Prueba inicialización de la aplicación"""
        app = Aplicacion()
        
        assert app.interfaz is not None
        assert hasattr(app.interfaz, 'mostrar_bienvenida')
        assert hasattr(app.interfaz, 'solicitar_ruta_archivo')
        assert hasattr(app.interfaz, 'procesar_archivo')
        assert hasattr(app.interfaz, 'preguntar_continuar')
        assert hasattr(app.interfaz, 'mostrar_despedida')
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['salir'])
    def test_ejecutar_salir_inmediato(self, mock_input, capsys):
        """Prueba ejecución de aplicación saliendo inmediatamente"""
        self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Gracias por usar el contador de palabras" in output
        assert mock_input.call_count == 1
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['quit'])
    def test_ejecutar_quit_inmediato(self, mock_input, capsys):
        """Prueba ejecución de aplicación con 'quit'"""
        self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Gracias por usar el contador de palabras" in output
        assert mock_input.call_count == 1
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['exit'])
    def test_ejecutar_exit_inmediato(self, mock_input, capsys):
        """Prueba ejecución de aplicación con 'exit'"""
        self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Gracias por usar el contador de palabras" in output
        assert mock_input.call_count == 1
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['q'])
    def test_ejecutar_q_inmediato(self, mock_input, capsys):
        """Prueba ejecución de aplicación con 'q'"""
        self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Gracias por usar el contador de palabras" in output
        assert mock_input.call_count == 1
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['archivo.txt', 'n'])
    def test_ejecutar_procesar_un_archivo(self, mock_input, capsys):
        """Prueba ejecución procesando un archivo y luego saliendo"""
        archivo = self._crear_archivo_prueba("archivo.txt", "Hola mundo")
        
        # Mock para que la ruta sea la del archivo de prueba
        with patch.object(self.app.interfaz, 'solicitar_ruta_archivo', return_value=archivo):
            with patch.object(self.app.interfaz, 'preguntar_continuar', return_value=False):
                self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 2" in output
        assert "Gracias por usar el contador de palabras" in output
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['archivo1.txt', 's', 'archivo2.txt', 'n'])
    def test_ejecutar_procesar_dos_archivos(self, mock_input, capsys):
        """Prueba ejecución procesando dos archivos"""
        archivo1 = self._crear_archivo_prueba("archivo1.txt", "Primer archivo")
        archivo2 = self._crear_archivo_prueba("archivo2.txt", "Segundo archivo con más palabras")
        
        # Mock para simular la entrada de archivos
        def mock_solicitar_ruta():
            if mock_input.call_count <= 2:
                return archivo1
            else:
                return archivo2
        
        def mock_preguntar_continuar():
            if mock_input.call_count <= 3:
                return True
            else:
                return False
        
        with patch.object(self.app.interfaz, 'solicitar_ruta_archivo', side_effect=[archivo1, archivo2]):
            with patch.object(self.app.interfaz, 'preguntar_continuar', side_effect=[True, False]):
                self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 2" in output  # Primer archivo
        assert "El número total de palabras es: 5" in output  # Segundo archivo
        assert "Gracias por usar el contador de palabras" in output
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['archivo_inexistente.txt', 'n'])
    def test_ejecutar_archivo_inexistente(self, mock_input, capsys):
        """Prueba ejecución con archivo inexistente"""
        archivo_inexistente = os.path.join(self.temp_dir, "no_existe.txt")
        
        with patch.object(self.app.interfaz, 'solicitar_ruta_archivo', return_value=archivo_inexistente):
            with patch.object(self.app.interfaz, 'preguntar_continuar', return_value=False):
                self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "No se encontró" in output
        assert "Gracias por usar el contador de palabras" in output
    
    @pytest.mark.integration
    @patch('builtins.input', side_effect=['archivo.txt', 's', 'archivo.txt', 'n'])
    def test_ejecutar_mismo_archivo_dos_veces(self, mock_input, capsys):
        """Prueba ejecución procesando el mismo archivo dos veces"""
        archivo = self._crear_archivo_prueba("archivo.txt", "Mismo contenido")
        
        with patch.object(self.app.interfaz, 'solicitar_ruta_archivo', return_value=archivo):
            with patch.object(self.app.interfaz, 'preguntar_continuar', side_effect=[True, False]):
                self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 2" in output
        # Debe aparecer dos veces (una por cada procesamiento)
        assert output.count("El número total de palabras es: 2") == 2
        assert "Gracias por usar el contador de palabras" in output
    
    @pytest.mark.integration
    def test_ejecutar_con_archivo_vacio(self, capsys):
        """Prueba ejecución con archivo vacío"""
        archivo = self._crear_archivo_prueba("vacio.txt", "")
        
        with patch('builtins.input', side_effect=['vacio.txt', 'n']):
            with patch.object(self.app.interfaz, 'solicitar_ruta_archivo', return_value=archivo):
                with patch.object(self.app.interfaz, 'preguntar_continuar', return_value=False):
                    self.app.ejecutar()
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "CONTADOR DE PALABRAS" in output
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 0" in output
        assert "El archivo está vacío" in output
        assert "Gracias por usar el contador de palabras" in output
